# -*- coding: utf-8 -*-
# Rzutowanie punktu na prostą

import numpy as np

def projection(p, p1, p2):
    u = float(np.dot(np.subtract(p, p1).tolist(), np.subtract(p2, p1).tolist()))/float(np.dot(np.subtract(p1, p2).tolist(), np.subtract(p1, p2).tolist()))
    return np.add(p1, np.multiply(np.subtract(p2, p1).tolist(), u).tolist()).tolist()