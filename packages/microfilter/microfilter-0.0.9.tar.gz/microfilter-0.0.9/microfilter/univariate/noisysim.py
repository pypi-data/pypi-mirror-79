
import numpy as np
from scipy.stats import skewnorm
import random
import time


def sim_data(chronological=True):
    a = random.choice([2., 3., 4.])
    ys = skewnorm.rvs(a, size=1000)
    outliers = [ random.choice([-1.,1.])*10. if np.random.rand()<0.05 else 0. for _ in ys]
    xs = np.cumsum(0.1*np.random.randn(1000))
    zs = [x + y*random.choice([-1.,1.]) + o for x, y, o in zip(xs, ys, outliers)]
    return zs if chronological else list(reversed(zs))


def sim_lagged_values_and_times():
    lagged_values = sim_data(chronological=False)
    lagged_times = [ time.time()-k for k,_ in enumerate(lagged_values)]
    return lagged_values, lagged_times
