import csv
import glob

def sched_ratio(filename):
    total = 0
    schedulable = 0
    with open(filename, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            if row["missed_task"] == "0":
                schedulable += 1
    ratio = 100.0 * schedulable / total if total > 0 else 0.0
    return schedulable, total, ratio

for fname in sorted(glob.glob("J_*.csv")):
    ok, total, ratio = sched_ratio(fname)
    print(f"{fname}: {ok}/{total} sets schedulable ({ratio:.1f}%)")

