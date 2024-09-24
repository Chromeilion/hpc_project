import json
import matplotlib.pyplot as plt
from pathlib import Path


def main():
    saveloc = "./the_results_of_osu_allgather.json"
    with open(saveloc, "r") as f:
        resdic = json.load(f)

    osu = resdic["osu_benchmarks"]["osu_allgather"]
    custom = resdic["custom_benchmarks"]["alltoall"]

    osu_avgs = []
    c_avgs = []
    for no_processors in custom.keys():
        res_o = 0
        res_c = sum(custom[no_processors]) / len(custom[no_processors])
        for it in range(len(osu[no_processors])):
            res_o += osu[no_processors][it][6][1]
        res_o /= len(osu[no_processors])
        osu_avgs.append(res_o)
        c_avgs.append(res_c*1e+6)

    x = list(custom.keys())
    fig, ax = plt.subplots()
    ax.set_yscale('log')
    ax.plot(x, c_avgs, label="Custom")
    ax.plot(x, osu_avgs, label="MPI")
    ax.set_ylabel("Latency (us)")
    ax.set_xlabel("Number of Processes")
    ax.set_title("Ring Broadcast Algorithm Performance")
    fig.legend(loc="center right")
    Path("figs/").mkdir(exist_ok=True)
    fig.savefig("figs/c_fig.png")

    fig, ax = plt.subplots()
    ax.plot(x, c_avgs)
    ax.set_ylabel("Latency (us)")
    ax.set_xlabel("Number of Processes")
    ax.set_title("Custom Ring Broadcast Algorithm Performance")
    fig.savefig("figs/c_fig_solo.png")


if __name__ == "__main__":
    main()
