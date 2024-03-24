import matplotlib.pyplot as plt
import numpy as np
import json
from collections import defaultdict


alg_map = {
    "0": "ignore",
    "1": "linear",
    "2": "double ring",
    "3": "recursive doubling",
    "4": "bruck",
    "5": "two proc only",
    "6": "tree"
}


def main():
    saveloc = "./the_results_of_osu.json"
    with open(saveloc, "r") as f:
        res = json.load(f)

    avgs = calc_averages(res)

    for operation, op_res in avgs.items():
        fig, ax = plt.subplots()
        for alg, processes_res in op_res.items():
            alg = alg_map[alg]

            arrays = [np.array(i[1:]) for i in results]
            avg_res = sum(arrays)/len(arrays)
            ax.plot(avg_res[0, :], avg_res[1, :], label=alg)
        col_titles = results[0][0]
        ax.set_xlabel(col_titles[0])
        ax.set_ylabel(col_titles[1])
        ax.set_title(operation)
        fig.legend()
        fig.show()


def calc_averages(results: dict):
    averages = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for operation, alg_res in results.items():
        for alg, processes_res in alg_res.items():
            alg = alg_map[alg]

            all_procs = processes_res.keys()

            arrays = [np.array(i[1:]) for i in results]
            avg_res = sum(arrays)/len(arrays)

            averages[operation][alg].append((no_processes, avg_res[10, :]))
    return averages


if __name__ == '__main__':
    main()
