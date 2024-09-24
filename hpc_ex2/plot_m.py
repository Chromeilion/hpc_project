import matplotlib.pyplot as plt
import json
from collections import defaultdict
import numpy as np
from pathlib import Path


def weak_plots(resdic, savepath):
    weak = resdic["weak_scaling"]
    n_iters = len(weak)
    nprocs = len(weak[0]['weak_window_scaling'])
    procs_arr = np.array([int(i) for i in weak[0]['weak_window_scaling'].keys()])
    avg_dict = defaultdict(lambda: np.zeros(shape=nprocs))
    for i in weak:
        for test_key, test_vals in i.items():
            vals = list(test_vals.values())
            avg_dict[test_key] += np.array(vals)
    for key, val in avg_dict.items():
        avg_dict[key] /= n_iters

    for title, vals in avg_dict.items():
        fig, ax = plt.subplots()
        ax.plot(procs_arr, vals)
        ax.set_xlabel("Num. Processors")
        ax.set_ylabel("Runtime (Seconds)")
        ax.set_title(title)
        fig.savefig(savepath/title)


def strong_plots(resdic, savepath):
    strong = resdic["strong_scaling"]
    n_iters = len(strong)
    nprocs = len(strong[0])
    procs_arr = np.array([int(i) for i in strong[0].keys()])
    avg_arr = np.zeros(shape=nprocs)
    for i in strong:
        vals = list(i.values())
        avg_arr += np.array(vals)
    avg_arr /= n_iters

    title = "Strong Scaling"
    fig, ax = plt.subplots()
    ax.plot(procs_arr, vals)
    ax.set_xlabel("Num. Processors")
    ax.set_ylabel("Runtime (Seconds)")
    ax.set_title(title)
    fig.savefig(savepath/title)

def create_plots(resdic: dict):
    savepath = Path("figs/")
    savepath.mkdir(exist_ok=True)
    weak_plots(resdic, savepath)
    strong_plots(resdic, savepath)


def main():
    saveloc = "./the_results_of_mand.json"
    with open(saveloc, "r") as f:
        resdic = json.load(f)

    create_plots(resdic)


if __name__ == '__main__':
    main()