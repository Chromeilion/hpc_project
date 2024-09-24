from mand_helpers import *
import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import tqdm


def calculate_coords(center: tuple[np.longdouble, np.longdouble], zoom: np.longdouble):
    window_size = np.longdouble(1)/(np.longdouble(2)**zoom)
    return (center[0]-window_size, center[1]-window_size,
            center[0]+window_size, center[1]+window_size)


def run_and_save(coords, window, iters, output_loc, m: MandRunner):
    run_out = m.run(coords, window, iters)
    data = np.array(
        [int(i) for i in run_out[0].split(" ") if i],
        dtype=np.ubyte
    )
    data.resize(window)
    data[data == 255] = 0
    # Get the color map by name:
    cm = plt.get_cmap('magma')
    # Apply the colormap like a function to any array:
    colored_data = cm(data)
    Image.fromarray(
        (colored_data[:, :, :3] * 255).astype(np.uint8)
    ).save(output_loc)


def create_video(savefolder, vid_out):
    command = f"ffmpeg -y -framerate 15 -pattern_type glob -i '{savefolder}/*.png' -c:v libx264 -pix_fmt yuv420p {vid_out}"
    res = subprocess.Popen(command, shell=True).communicate()
    return res


def render(midpoint, zoom, no_frames, window, iters, savefolder, m, vid_out):
    if no_frames == 1:
        zoom_steps = [np.longdouble(zoom)]
        iter_steps = [np.longdouble(iters)]
    else:
        zoom_steps = np.linspace(1, zoom, no_frames, dtype=np.longdouble)
        iter_steps = np.linspace(min(255, iters), iters, no_frames, dtype=int)
    for i, (zoom_step, iter_step) in tqdm.tqdm(enumerate(zip(zoom_steps, iter_steps)), total=no_frames):
        coords = calculate_coords(np.longdouble(midpoint), zoom_step)
        name = str(i).zfill(8)
        run_and_save(
            coords, window, int(iter_step), f"{savefolder}/{name}.png", m
        )
#    create_video(savefolder, vid_out)


def main():
    start = (np.longdouble(-0.77817645), np.longdouble(0.129919014))
    start = (np.longdouble(0.37894144929305185), np.longdouble(0.0911550893988533))
    zoom = 38
    frames = 1
    m = MandRunner(os.environ["MAND_LOC"])
    iters = 1000
    window = (1000, 1000)
    out_loc = "./frames"
    vid_out = "./video.mp4"

    if not os.path.exists(out_loc):
        os.mkdir(out_loc)
    import time
    s = time.time()
    render(start, zoom, frames, window, iters, out_loc, m, vid_out)
    print(time.time()-s)


if __name__ == "__main__":
    main()

