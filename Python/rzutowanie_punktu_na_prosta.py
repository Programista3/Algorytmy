# -*- coding: utf-8 -*-
# Rzutowanie punktu na prostą

import numpy as np

def projection(p, p1, p2):
    u = float(np.dot([p[0]-p1[0], p[1]-p1[1]], [p2[0]-p1[0], p2[1]-p1[1]]))/float(np.dot([p1[0]-p2[0], p1[1]-p2[1]], [p1[0]-p2[0], p1[1]-p2[1]]))
    return np.add(p1, np.multiply(np.subtract(p2, p1).tolist(), u).tolist()).tolist()