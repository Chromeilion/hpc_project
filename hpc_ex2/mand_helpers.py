import os
import subprocess
import time


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
        mand_r = subprocess.Popen(
            self._create_command(coords, window, n_iter),
            stdout=subprocess.PIPE,
            env=os.environ,
            text=True
        ).communicate()
        return mand_r

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
