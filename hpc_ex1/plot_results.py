import matplotlib.pyplot as plt
import numpy as np
import json
from collections import defaultdict
from pathlib import Path


alg_map_bcast = {
    "0": "ignore",
    "1": "basic linear",
    "2": "chain",
    "3": "pipeline",
    "4": "split binary tree",
    "5": "binary tree",
    "6": "binomial tree"
}
alg_map_gather = {
    "0": "ignore",
    "1": "basic linear",
    "2": "binomial",
    "3": "linear with synchronization"
}
alg_maps = {"osu_bcast": alg_map_bcast, "osu_gather": alg_map_gather,
            "naive model": {"1": "naive model"}}


def create_bcast(bb, lat):
    simple_model = defaultdict(lambda: defaultdict(dict))
    for n_proc in bb['basic linear'].keys():
        simple_model[n_proc]['columns'] = bb['basic linear'][n_proc]['columns']
        simple_model[n_proc]['msg_size'] = {}
        for msg_size, lat_ in lat['naive model'][2]['msg_size'].items():
            simple_model[n_proc]['msg_size'][msg_size] = lat_ * n_proc-1
    bb['naive model'] = simple_model
    return bb


def create_gather(gg, lat):
    simple_model = defaultdict(lambda: defaultdict(dict))
    for n_proc in gg['basic linear'].keys():
        simple_model[n_proc]['columns'] = gg['basic linear'][n_proc]['columns']
        simple_model[n_proc]['msg_size'] = {}
        for msg_size, lat_ in lat['naive model'][2]['msg_size'].items():
            simple_model[n_proc]['msg_size'][msg_size] = lat_ * n_proc-1
    gg['naive model'] = simple_model
    return gg


def main():
    saveloc = "./the_results_of_osu.json"
    with open(saveloc, "r") as f:
        res = json.load(f)
    for msg_size_idx in range(21):
        avgs = calc_averages(res)
        savepath = Path("../figs")
        savepath.mkdir(exist_ok=True)
        avgs = {'osu_bcast': create_bcast(avgs['osu_bcast'], avgs['naive model']),
                'osu_gather': create_gather(avgs['osu_gather'], avgs['naive model'])}
        for operation, op_res in avgs.items():
            bfig, bax = plt.subplots()
            bax.set_ylabel("Avg. Normalized Latency(us)")
            bax.set_xlabel("No. Processes")
            mfig, max = plt.subplots(figsize=(8, 5))
            max.set_ylabel("Avg. Latency(us)")
            max.set_xlabel("No. Processes")

            for alg, alg_res in op_res.items():
                fig, ax = plt.subplots()
                ax.set_xlabel(alg_res[2]['columns'][0])
                ax.set_ylabel(alg_res[2]['columns'][1])
                for n_p, n_p_res in list(alg_res.items())[::4]:
                    items = n_p_res["msg_size"].items()
                    x = [int(i[0]) for i in items]
                    y = [i[1] for i in items]
                    ax.plot(x, y, label=n_p)
                n_p, n_p_res = list(alg_res.items())[-1]
                items = n_p_res["msg_size"].items()
                x = [int(i[0]) for i in items]
                y = [i[1] for i in items]
                ax.plot(x, y, label=n_p)

                title = " ".join([operation, alg])
                ax.set_title(title)
                fig.legend(title="Num. Processes")
                fig.savefig(f"{savepath/title}.png")
                plt.close()

                all_proc = np.array(
                    [list(i["msg_size"].values()) for i in alg_res.values()]
                )
                max.plot(range(2, all_proc.shape[0]*2+1, 2), all_proc[:, msg_size_idx], label=alg)
                all_proc /= np.array(x)
                avg = np.sum(all_proc, axis=1) / all_proc.shape[0]
                bax.plot(range(2, all_proc.shape[0]*2+1, 2), avg, label=alg)


            title = " ".join([operation])
            bax.set_title(title)
            bfig.legend()
            bfig.savefig(f"{savepath/title}.png")
            plt.close()
            mfig.legend()
            title = " ".join([operation]) + f" Msg. Size {x[msg_size_idx]}"
            max.set_title(title)
            mfig.savefig(f"{savepath/title}.png")
            plt.close()


def calc_averages(results: dict):
    """
    Convert to operation -> alg -> message_size -> num_procs
    """
    averages = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(dict))))
    for operation, alg_res in results.items():
        for alg, processes_res in alg_res.items():
            alg = alg_maps[operation][alg]
            for no_procs, res in processes_res.items():
                try:
                    columns = res[0][0]
                except IndexError:
                    continue
                arrs = [np.array(i[1:]) for i in res]
                try:
                    avg_arr = sum(arrs) / len(arrs)
                except ValueError:
                    continue
                averages[operation][alg][int(no_procs)]["columns"] = columns

                for i in avg_arr:
                    size = np.round(i[0])
                    averages[operation][alg][int(no_procs)]["msg_size"][size] = i[1]

    return averages


if __name__ == '__main__':
    main()
