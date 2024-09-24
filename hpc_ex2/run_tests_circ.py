import json
from typing import Optional
from pathlib import Path
from collections import defaultdict
import os
import subprocess


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
        "mpirun", "--map-by", "NODE", "--mca",
        "coll_tuned_use_dynamic_rules", "true", "--mca",
        "coll_tuned_allgather_algorithm", "4"
    ]
    base_command_custom = [
        "mpirun", "--map-by", "NODE"
    ]
    task = "osu_allgather"
    no_its = 4
    saveloc = "./the_results_of_osu_allgather.json"
    no_cpus = int(os.environ["SLURM_NTASKS_PER_NODE"])
    bin_loc = os.environ["TWOA_BIN"]

    resdic = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for no_processes in range(2, (no_cpus*2)+1, 2):
        for _ in range(no_its):
            command = (
                    base_command +
                    ["-n", str(no_processes)]+[osu_path/task]
            )
            result, _ = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                env=os.environ
            ).communicate()
            parsed = parse_osu_output(result)
            resdic["osu_benchmarks"][task][no_processes].append(parsed)

            command = (base_command_custom + ["-n", str(no_processes)] + [bin_loc])
            _ = subprocess.run(
                command,
                env=os.environ
            )
            with open("./time_taken.txt", "r") as f:
                time_taken = float(f.readline())
            resdic["custom_benchmarks"]["alltoall"][no_processes].append(time_taken)

    with open(saveloc, 'w') as f:
        json.dump(resdic, f)


if __name__ == "__main__":
    main()
