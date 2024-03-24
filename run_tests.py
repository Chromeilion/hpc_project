from __future__ import annotations

import json
from collections import defaultdict
import subprocess
import argparse as ap
from pathlib import Path
from typing import Optional
import os


def parse_osu_output(output: bytes) -> list[list[str | float]]:
    output_str = output.decode("utf-8")
    output_lines = output_str.split("\n")
    parsed_list = []
    for no, i in enumerate(output_lines):
        if len(i) == 0:
            continue
        if i[0] == "#":
            if output_lines[no+1][0] != "#":
                split_line = [
                    j.strip() for j in i.split("  ") if j not in ["#", ""]
                ]
                split_line[0] = split_line[0][2:]
                parsed_list.append(split_line)
            continue
        split_line = [
            float(j.strip()) for j in i.split("  ") if j not in ["#", ""]
        ]
        parsed_list.append(split_line)

    return parsed_list


def main(osu_loc: Optional[str] = None, *_, **__):
    if osu_loc is None:
        osu_loc = (Path(os.getenv('OSU_COMPILED_PATH')) /
                   "libexec/osu-micro-benchmarks/mpi/collective")

    osu_path = Path(osu_loc)
    base_command = [
        "mpirun", "--map-by", "core", "--mca",
        "coll_tuned_use_dynamic_rules", "true", "--mca",
        "coll_tuned_bcast_algorithm"
    ]
    algorithms = ["0", "2", "3"]

    tasks = ["osu_bcast", "osu_scatter"]
    no_its = 1
    saveloc = "./the_results_of_osu.json"
    no_cpus = int(os.environ["SLURM_JOB_CPUS_PER_NODE"])

    resdic = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for task in tasks:
        for alg in algorithms:
            for no_processes in range(2, no_cpus+1):
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
    parser = ap.ArgumentParser()
    parser.add_argument("--osu-loc")
    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))
