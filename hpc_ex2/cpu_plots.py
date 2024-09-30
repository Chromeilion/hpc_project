import matplotlib.pyplot as plt
import pickle
import numpy as np

with open("times_3.pkl", "rb") as f:
    data_3 = pickle.load(f)
with open("times_1.pkl", "rb") as f:
    data_1 = pickle.load(f)
with open("times_2.pkl", "rb") as f:
    data_2 = pickle.load(f)
with open("times_4.pkl", "rb") as f:
    data_4 = pickle.load(f)
with open("times_5.pkl", "rb") as f:
    data_5 = pickle.load(f)
with open("times_6.pkl", "rb") as f:
    data_6 = pickle.load(f)
with open("times_7.pkl", "rb") as f:
    data_7 = pickle.load(f)
with open("times_8.pkl", "rb") as f:
    data_8 = pickle.load(f)
with open("times_9.pkl", "rb") as f:
    data_9 = pickle.load(f)
with open("times_10.pkl", "rb") as f:
    data_10 = pickle.load(f)

fig, ax = plt.subplots()
ax.plot(data_1[0], data_1[1], label="1 Stage")
ax.plot(data_5[0], data_5[1], label="5 Stages")
ax.set_title("CPU Utilization Throughout Program Runtime")
ax.set_xlabel("Time (seconds)")
ax.set_ylabel("CPU Utilization (percentage)")
ax.legend()
fig.savefig("./runtime_cpu_comp.png")

all_d = [data_1, data_2, data_3, data_4, data_5, data_6, data_7, data_8, data_9, data_10]
total_times = [i[0][-1] for i in all_d]
fig, ax = plt.subplots()
ax.plot(list(range(1, len(all_d)+1)), total_times)
ax.xaxis.set_ticks(list(range(1, len(all_d)+1)))
ax.set_title("Number of Stages Effect on Total Runtime")
ax.set_xlabel("Number of Stages")
ax.set_ylabel("Runtime (seconds)")
fig.savefig("./runtime_comp.png")

n_points = 20
NO_T_STEPS = 5
T_MAX = 500
T_BASE = np.array([3 for _ in range(n_points)])

x = np.linspace(1, NO_T_STEPS, n_points)
y = T_BASE**(x-NO_T_STEPS)*T_MAX

T_BASE = np.array([3 for _ in range(NO_T_STEPS)])
x_l = np.linspace(1, 5, NO_T_STEPS)
y_l = T_BASE**(x_l-NO_T_STEPS)*T_MAX
x_l = list(range(1, NO_T_STEPS+1))

fig, ax = plt.subplots()
ax.plot(x, y, zorder=1)
ax.scatter(x_l, y_l.round(), color="r", zorder=2)
ax.set_title("Iteration Scaling")
ax.set_xlabel("Stage Number")
ax.xaxis.set_ticks(x_l)
ax.set_ylabel("Number of Iterations")
fig.savefig("./iter_scale.png")
