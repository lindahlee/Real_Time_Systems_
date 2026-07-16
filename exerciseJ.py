#!/usr/bin/env python3
import sys
import csv
import math

# opens and reads csv file
def load_task_sets(filename):
    sets = {}
    with open(filename, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sid = int(row["set"])
            task = {
                "task": int(row["task"]),
                "T": int(row["T"]),
                "C": int(row["C"]),
                "D": int(row["D"]),
            }
            sets.setdefault(sid, []).append(task)
    # sort tasks by task index
    for sid in sets:
        sets[sid].sort(key=lambda t: t["task"]) 
    return sets


def priority_key(job, policy, preemptive):
    if policy == "FCFS":
        return (job["release"], job["task"])#earlier release is higher priority
    elif policy == "SJF":
        if preemptive:
            return (job["remaining"], job["task"])# priority based on job
            # with the smallest remaining time
        else:
            return (job["C"], job["task"])
    elif policy == "RM":
        return (job["T"], job["task"]) #higher priority for smaller pd
    elif policy == "EDF":
        return (job["deadline"], job["task"])
    else: # this returns the final tuple (priority_value, job_id)
        return (0, job["task"]) # fall back case

# core simulations for one single task set
def simulate(tasks, policy, preemptive):
    next_release = {t["task"]: 0 for t in tasks} # all tasks release at time 0 
    ready_jobs = [] # empty list for ready jobs waiting 
    current_job = None # makes sure no job is executing on CPU at the very start

    for time in range(100_001):
        # release jobs
        for tsk in tasks:
            tid = tsk["task"]
            T = tsk["T"]
            C = tsk["C"]
            D = tsk["D"]
            while next_release[tid] == time:
                job = {
                    "task": tid,
                    "T": T,
                    "C": C,
                    "D": D,
                    "release": time,
                    "deadline": time + D,
                    "remaining": C,
                }
                ready_jobs.append(job)# puts the newly releases job in ready queue
                next_release[tid] += T # schedules next release by one pd in future

        # deadline check 
        all_active = ready_jobs + ([current_job] if current_job is not None else [])
        for job in all_active:
            if time == job["deadline"] and job["remaining"] > 0: # we reached the exact
                # chance to finish and job is not yet done so display a deadline miss
                return job["task"], time

        # chose which job to run
        if preemptive:
            pool = [j for j in ready_jobs if j["remaining"] > 0]
            if current_job is not None and current_job["remaining"] > 0:
                pool.append(current_job)
            if pool:
                best = min(pool, key=lambda j: priority_key(j, policy, preemptive))
                if best is not current_job:
                    if best in ready_jobs:
                        ready_jobs.remove(best)
                    if current_job is not None and current_job["remaining"] > 0 and current_job not in ready_jobs:
                        ready_jobs.append(current_job)
                    current_job = best
        else:
            if current_job is None or current_job["remaining"] <= 0:
                runnable = [j for j in ready_jobs if j["remaining"] > 0]
                if runnable:
                    best = min(runnable, key=lambda j: priority_key(j, policy, preemptive))
                    ready_jobs.remove(best)
                    current_job = best

        # execute one time unit
        if current_job is not None:
            current_job["remaining"] -= 1
            if current_job["remaining"] <= 0:
                current_job = None

    # no deadline miss within 100000
    return 0, None


def main():
    if len(sys.argv) != 4:
        print("Usage: python3 exerciseJ.py input.csv POLICY(FCFS|SJF|RM|EDF) p|np")
        sys.exit(1)

    filename = sys.argv[1]
    policy = sys.argv[2].upper()
    preemptive = (sys.argv[3].lower() == "p")

    sets = load_task_sets(filename)

    print("set,missed_task,miss_time")
    for sid in sorted(sets.keys()):
        missed_task, miss_time = simulate(sets[sid], policy, preemptive)
        if missed_task == 0:
            print(f"{sid},0,")
        else:
            print(f"{sid},{missed_task},{miss_time}")


if __name__ == "__main__":
    main()





