import numpy as np
import cv2
import _conceptual as c
import _graph as graph
from _dimensions import *

## def color(space):
##     res = {}
##     current = space.field("current")
##     lab = cv2.cvtColor(current, cv2.COLOR_BGR2Lab)
##     l, a, b = cv2.split(lab)
##     res["lightness"] = c.Field(l - 0.5)
##     res["greenred"] = c.Field(a - 0.5)
##     res["blueyellow"] = c.Field(b - 0.5)
##     return res


def position(space):
    res = {}
    sz = space.size
    vertical = np.zeros(sz, np.float32)
    horizontal = np.zeros(sz, np.float32)
    h = sz[0]
    w = sz[1]

    for y in range(0, h):
        for x in range(0, w):
            horizontal[y, x] = x/(w*1.0)
            vertical[y, x] = y/(h*1.0)

    res["horizontal"] = c.Field(horizontal)
    res["vertical"] = c.Field(vertical)

    return res
