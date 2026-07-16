import csv
import glob

PASS_COLUMNS = ["feasible", "schedulable", "pass", "result"]

PASS_VALUES = {"1", "y", "yes", "true", "t", "pass", "ok", "p"}

def count_passes(filename):
    with open(filename, newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames

        pass_col = None
        for cand in PASS_COLUMNS:
            if cand in fieldnames:
                pass_col = cand
                break

        if pass_col is None:
            print(f"{filename}: couldnt find a pass/fail column. "
                  f"Available columns = {fieldnames}")
            return None, None, None

        total = 0
        passed = 0
        for row in reader:
            total += 1
            val = row[pass_col].strip().lower()
            if val in PASS_VALUES:
                passed += 1

        ratio = 100.0 * passed / total if total > 0 else 0.0
        return passed, total, ratio


def main():
    files = sorted(glob.glob("L_*.csv"))
    if not files:
        print("No L_*.csv files found in this folder.")
        return

    for fname in files:
        passed, total, ratio = count_passes(fname)
        if total is not None:
            print(f"{fname}: {passed}/{total} sets pass ({ratio:.1f}%)")


if __name__ == "__main__":
    main()

