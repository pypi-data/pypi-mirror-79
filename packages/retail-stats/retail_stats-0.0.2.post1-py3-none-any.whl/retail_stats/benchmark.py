import timeit

import numpy as np

runs = [1000, 10000, 100000]

setup = [f"""
import numpy as np
from retail_stats.elasticity import calculate_cross_elasticity

np.random.seed(42)

a = np.random.random({run})
b = np.random.random({run})
c = np.random.random({run})
d = np.random.random({run})
""" for run in runs]

run_data = np.array([timeit.Timer('calculate_cross_elasticity(a, b, c, d)',
                                  setup=s).repeat(10, 1000) for s in setup])

mean_run_times = np.mean(run_data, axis=1)
vals = [{"Number of Products": i, "Time in Seconds": j}
        for i, j in zip(runs, mean_run_times)]

print(vals)
