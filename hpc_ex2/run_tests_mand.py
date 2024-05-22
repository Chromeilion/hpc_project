from __future__ import annotations

import json
from collections import defaultdict
import subprocess
import time
import os


def run(command: list[str]):
    start_t = time.time()
    result, _ = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        env=os.environ
    ).communicate()
    end_t = time.time() - start_t
    return result


def test_weak():
    ...


def test_strong():
    ...


def main():
    bin = os.environ["EX2C_loc"]
    strong_window = ["2000", "2000"]
    strong_iter = "1000"
    base_command = [
         "-0.757", "-0.0555", "-0.747", "-0.063"
    ]
    no_its = 4
    saveloc = "./the_results_of_osu.json"
    no_cpus = int(os.environ["SLURM_NTASKS_PER_NODE"])

    resdic = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for task in tasks:
        print(f"Doing task: {task}")
        for alg in algorithms:
            print(f"Testing algorithm: {alg}")
            for no_processes in range(2, no_cpus+1):
                print(f"No processes: {no_processes}")
                for _ in range(no_its):
                    command = base_command+[alg]+["-n", str(no_processes)]+[osu_path/task]
                    result, _ = subprocess.Popen(
                        command,
                        stdout=subprocess.PIPE,
                        env=os.environ
                    ).communicate()
                    resdic[task][alg][no_processes].append(parse_osu_output(result))

    with open(saveloc, 'w') as f:
        json.dump(resdic, f)


if __name__ == "__main__":
    main()
