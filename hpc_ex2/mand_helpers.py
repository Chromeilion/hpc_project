import os
import subprocess
import time
from subprocess import TimeoutExpired
import pickle
import psutil
import matplotlib.pyplot as plt


coord_t = tuple[float, float, float, float]
window_t = tuple[int, int]
n_iter_t = int


class MandRunner:
    def __init__(self, loc: os.PathLike | str):
        self.loc = loc

    def run(self,
            coords: coord_t,
            window: window_t,
            n_iter: n_iter_t
            ):
        start = time.time()
        mand_r = subprocess.Popen(
            self._create_command(coords, window, n_iter),
            stdout=subprocess.PIPE,
            env=os.environ,
            text=True
        )
#        cpu = []
#        times = []
#        while mand_r.poll() is None:
#            cpu.append(psutil.cpu_percent())
#            times.append(time.time()-start)
#            try:
#                mand_r = mand_r.communicate(input=None, timeout=0.05)
#                break
#            except TimeoutExpired:
#                continue
#        with open("times.pkl", "wb") as f:
#            pickle.dump([times, cpu], f)
        return mand_r.communicate()

    def _create_command(self,
                        coords: coord_t, window: window_t, n_iter: n_iter_t):
        return [
            str(i) for i in tuple([self.loc]) + window + coords +
            tuple([n_iter])
        ]


def time_run(coords: coord_t, window: window_t, n_iter: n_iter_t, m: MandRunner):
    start_t = time.time()
    result, _ = m.run(coords, window, n_iter)
    t = time.time() - start_t
    return t
