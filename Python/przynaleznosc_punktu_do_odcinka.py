# -*- coding: utf-8 -*-
# Przynależność punktu do odcinka

def affiliation(start, end, point):
    a = start+[1]
    b = end+[1]
    c = point+[1]
    det = (a[0]*b[1]*c[2]+a[1]*b[2]*c[0]+a[2]*b[0]*c[1])-(a[2]*b[1]*c[0]+a[0]*b[2]*c[1]+a[1]*b[0]*c[2])
    if det == 0 and c[0] >= min(a[0], b[0]) and c[0] <= max(a[0], b[0]) and c[1] >= min(a[1], b[1]) and c[1] <= max(a[1], b[1]):
        return 1
    else:
        return 0