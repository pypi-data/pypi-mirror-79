import json
import numpy as np
import scipy.stats




def normal(mean, stdDev,**kwds):

    return scipy.stats.norm(loc=mean, scale=stdDev)

def lognormal(mean, stdDev, **kwds):
    s = np.sqrt(np.log(stdDev**2/mean**2 + 1))
    mu = mean**2/np.sqrt(stdDev**2+mean**2)
    return scipy.stats.lognorm(s=s,scale=mu)

def gumbel(alphaparam=None, betaparam=None, mean=None, stdDev=None,**kwds):
    if mean is not None and stdDev is not None:
        scale = np.sqrt(6)/np.pi*stdDev
        return scipy.stats.gumbel_r(
            loc=mean-np.euler_gamma*scale,
            scale=scale
        )

mapping = {
    'gumbel': gumbel,
    'normal': normal,
    'lognormal': lognormal
}

def load_rv_from_dicts(s):
    return [
        mapping[d['distribution']](**d) for d in s
    ]
