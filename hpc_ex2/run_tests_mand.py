from __future__ import annotations

import json
import os

from mand_helpers import MandRunner, coord_t, window_t, time_run, n_iter_t


WEAK_WINDOW_ITERS = 500
WEAK_ITER_WINDOW = (500, 500)
WEAK_ITER_SCALE_FACTOR = 80
WEAK_WINDOW_SCALE_FACTOR = 200
STRONG_ITERS = 800
STRONG_WINDOW = (2000, 2000)


def test_weak(n_processors, coord: coord_t, weak_window_iters: int,
              weak_iter_window: window_t, m: MandRunner):
    """
    Test weak scaling on the Mandelbrot algorithm.
    """
    resdic = {}
#    print("Testing weak window scaling")
#    resdic["weak_window_scaling"] = test_window_scaling_weak(
#        n_processors, coord, weak_window_iters, m
#    )
    print("Testing weak iter scaling")
    resdic["weak_iter_scaling"] = test_iter_scaling_weak(
        n_processors, coord, weak_iter_window, m
    )
#    print("Testing full weak scaling")
#    resdic["weak_scaling_full"] = test_full_scaling_weak(
#        n_processors, coord, m
#    )
    return resdic


def test_full_scaling_weak(n_processors, coord: coord_t, m: MandRunner,
                           iters_per_p: int = WEAK_ITER_SCALE_FACTOR,
                           pxls_per_p: int = WEAK_WINDOW_SCALE_FACTOR):
    times = {}
    for n_p in range(1, n_processors+1):
        os.environ["OMP_NUM_THREADS"] = str(n_p)
        ni_size = n_p * iters_per_p
        w_size = n_p * pxls_per_p
        times[n_p] = time_run(coord,
                              (w_size, w_size),
                              n_iter=ni_size,
                              m=m)
    return times


def test_iter_scaling_weak(n_processors: int, coord: coord_t,
                           weak_iter_window: window_t, m: MandRunner,
                           iters_per_p: int = WEAK_ITER_SCALE_FACTOR):
    times = {}
    for n_p in range(1, n_processors+1):
        os.environ["OMP_NUM_THREADS"] = str(n_p)
        ni_size = iters_per_p**n_p
        times[n_p] = time_run(coord, weak_iter_window,
                              n_iter=ni_size,
                              m=m)
    return times


def test_window_scaling_weak(n_processors,
                             coord: coord_t,
                             n_iter: n_iter_t,
                             m: MandRunner,
                             pxls_per_p: int = WEAK_WINDOW_SCALE_FACTOR):
    """
    Test weak scaling by increasing the window size proportional to the
    number of processors being used.
    """
    times = {}
    for n_p in range(1, n_processors+1):
        os.environ["OMP_NUM_THREADS"] = str(n_p)
        w_size = pxls_per_p*n_p
        times[n_p] = time_run(coord, (w_size, w_size), n_iter=n_iter,
                              m=m)
    return times


def test_strong(n_processors: int, coords: coord_t, window: window_t,
                n_iter: n_iter_t, m: MandRunner):
    print("Testing strong scaling")
    times = {}
    for n_p in range(1, n_processors+1):
        os.environ["OMP_NUM_THREADS"] = str(n_p)
        times[n_p] = time_run(coords, window=window, n_iter=n_iter, m=m)
    return times


def main():
    coords: coord_t = (-0.757, -0.0555, -0.747, -0.063)
    no_its = 1
    saveloc = "./the_results_of_mand.json"
    no_cpus = 6
    m = MandRunner(os.environ["MAND_LOC"])

    weak_results = [
        test_weak(no_cpus, coords, WEAK_WINDOW_ITERS, WEAK_ITER_WINDOW, m)
        for _ in range(no_its)
    ]
    strong_results = None
#    strong_results = [
#        test_strong(n_processors=no_cpus, coords=coords, window=STRONG_WINDOW,
#                    n_iter=STRONG_ITERS, m=m) for _ in range(no_its)
#    ]
    resdic = {
        "weak_scaling": weak_results,
        "strong_scaling": strong_results
    }

    with open(saveloc, 'w') as f:
        json.dump(resdic, f)


if __name__ == "__main__":
    main()
