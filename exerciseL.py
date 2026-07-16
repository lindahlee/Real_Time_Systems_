#!/usr/bin/env python3
import sys
import csv
import math


def load_sets(path):
    sets = {}
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sid = int(row["set"])
            T = int(row["T"])
            C = int(row["C"])
            D = int(row["D"])
            sets.setdefault(sid, []).append((T, C, D))
    return sets


def edf_util(tasks):
    if any(D != T for (T, C, D) in tasks):
        return False
    U = sum(C / T for (T, C, D) in tasks) 
    return U <= 1.0 + 1e-12 

def rta_fp(tasks, order_key):
    ts = sorted(tasks, key=order_key) #sorts by priority where Rm is Ti and DM is Di
    for i, (Ti, Ci, Di) in enumerate(ts):
        R = Ci
        while True:
            W = Ci
            for j in range(i):
                Tj, Cj, Dj = ts[j]
                W += math.ceil(R / Tj) * Cj
            if W == R:
                break
            if W > Di:
                return False
            R = W
        if R > Di:
            return False
    return True


def edf_demand(tasks):
    if any(D > T for (T, C, D) in tasks):
        return False
    U = sum(C / T for (T, C, D) in tasks)
    if U >= 1.0:
        return False

    num = sum((T - D) * (C / T) for (T, C, D) in tasks)
    denom = 1.0 - U
    if denom <= 0:
        return False
    Ls = num / denom

    Lmax = max(D for (T, C, D) in tasks)
    Lmax = max(Lmax, int(math.ceil(Ls)))

    for (Ti, Ci, Di) in tasks:
        k = 0
        while True:
            L = Di + k * Ti
            if L > Lmax:
                break
            demand = 0
            for (Tj, Cj, Dj) in tasks:
                if L >= Dj:
                    demand += (math.floor((L - Dj) / Tj) + 1) * Cj
            if demand > L:
                return False
            k += 1

    return True


def main():
    if len(sys.argv) != 4:
        print("Usage: python3 exerciseL.py input.csv POLICY(EDF|RM|DM) ANALYSIS(UTIL|DEMAND|RTA)")
        sys.exit(1)

    path = sys.argv[1]
    policy = sys.argv[2].upper()
    method = sys.argv[3].upper()

    sets = load_sets(path)

    print("set,result")
    for sid in sorted(sets):
        tasks = sets[sid]
        if policy == "EDF" and method == "UTIL":
            ok = edf_util(tasks)
        elif policy == "EDF" and method == "DEMAND":
            ok = edf_demand(tasks)
        elif policy == "RM" and method == "RTA":
            ok = rta_fp(tasks, order_key=lambda t: t[0])
        elif policy == "DM" and method == "RTA":
            ok = rta_fp(tasks, order_key=lambda t: t[2])
        else:
            ok = False
        print(f"{sid},{'P' if ok else 'F'}")


if __name__ == "__main__":
    main()


