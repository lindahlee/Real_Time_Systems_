#!/usr/bin/env python3
import sys
import random
import math


def uunifast(num_tasks, total_util):
    utilizations = [] # stores the per task util 
    remaining = total_util # starts w the total util (ex:0.7)
    #bc unifast works by subtracting randon portions of remaining
    #until everything is allocated

    for k in range(1, num_tasks):#for first n-1 task, randomly decides
        #how much remaining utl they get
        x = random.random() # picks a random in (0,1)
        next_remaining = remaining * (x ** (1 / (num_tasks - k))) # universal
        # uunifast equation that shrinks remaining util in controlled way:
        # positive & no bias
        utilizations.append(remaining - next_remaining)# dif b/t old remain and new remain
        # is assihgned to curr task
        remaining = next_remaining # updates remaining for next task 

    utilizations.append(remaining)# any leftover util is assigned to last task,
    # which gaurentees sum of u_i = total_util
    return utilizations # returns list of per task utils [u_1,.., u_n]



def main(): # takes the  [u_1,.., u_n] and turns them into
    # actual periodic tasks (T, C, D) for 100 task sets
    if len(sys.argv) != 4: # requires 3 args : n U v
        print("Usage: python3 exerciseH.py n U v")
        sys.exit(1)

    num_tasks = int(sys.argv[1])
    total_util = float(sys.argv[2])
    mode = int(sys.argv[3])

    print("set,task,T,C,D")

    for set_id in range(1, 101): # generates 100 task sets
        utils = uunifast(num_tasks, total_util)# calls uunifast for each
        # set to get num_tasks utils that sum to U

        for task_id, u in enumerate(utils, start=1):# one task per util
            T = random.randint(100, 1000)
            C = int(u * T)# u = C/T
            if C < 1:
                C = 1
            if C > T:
                C = T # enforces bounds to keep tasks meaningful,
                # every task has positive C 

            if mode == 0:
                D = T
            else:
                D = random.randint(math.ceil(0.8 * T), T)

            print(f"{set_id},{task_id},{T},{C},{D}")


if __name__ == "__main__":
    main()

