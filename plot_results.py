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
        for alg, alg_res in op_res.items():
            for msg_size, msg_size_res in alg_res["msg_size"].items():
                fig, ax = plt.subplots()
                items = msg_size_res.items()
                x = [int(i[0]) for i in items]
                y = [i[1] for i in items]
                ax.plot(x, y, label=alg)
                ax.set_xlabel(alg_res['columns'][0])
                ax.set_ylabel(alg_res['columns'][1])
                ax.set_title(" ".join([operation, alg, str(msg_size)]))
                fig.legend()
                fig.show()


def calc_averages(results: dict):
    """
    Convert to operation -> alg -> message_size -> num_procs
    """
    averages = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(dict))))
    for operation, alg_res in results.items():
        for alg, processes_res in alg_res.items():
            alg = alg_map[alg]
            for no_procs, res in processes_res.items():
                columns = res[0][0]
                arrs = [np.array(i[1:]) for i in res]
                avg_arr = sum(arrs) / len(arrs)
                averages[operation][alg]["columns"] = columns

                for i in avg_arr:
                    size = np.round(i[0])
                    averages[operation][alg]["msg_size"][size][no_procs] = i[1]

    return averages


if __name__ == '__main__':
    main()
