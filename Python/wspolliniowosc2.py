# -*- coding: utf-8 -*-
# Współliniowość trzech punktów v.2

def det(a, b, c):
	a = a+[1]
	b = b+[1]
	c = c+[1]
	return (a[0]*b[1]*c[2]+a[1]*b[2]*c[0]+a[2]*b[0]*c[1])-(a[2]*b[1]*c[0]+a[0]*b[2]*c[1]+a[1]*b[0]*c[2])

print(u"Podaj współrzędne punktu a:")
a = input()
print(u"Podaj współrzędne punktu b:")
b = input()
print(u"Podaj współrzędne punktu c:")
c = input()
det = det(list(map(int, a.split(','))), list(map(int, b.split(','))), list(map(int, c.split(','))))
print('det(a,b,c) = '+str(det))
if det == 0:
	print(u"Punkty a, b, c są współliniowe")
else:
	print(u"Punkty a, b, c nie są współliniowe")