# -*- coding: utf-8 -*-
# Przynależność punktu do koła

def affiliation(O, r, point):
    a = max(O[0], point[0])-min(O[0], point[0])
    b = max(O[1], point[1])-min(O[1], point[1])
    c = (a**2+b**2)**0.5
    if c <= r:
        return 1
    else:
        return 0