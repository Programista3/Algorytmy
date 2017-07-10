# -*- coding: utf-8 -*-
# Współliniowość trzech punktów

print(u"Podaj współrzędne punktu a:")
a = raw_input()
print(u"Podaj współrzędne punktu b:")
b = raw_input()
print(u"Podaj współrzędne punktu c:")
c = raw_input()
punkty = [map(int, a.split(','))+[1], map(int, b.split(','))+[1], map(int, c.split(','))+[1]]
det = (punkty[0][0]*punkty[1][1]*punkty[2][2]+punkty[0][1]*punkty[1][2]*punkty[2][0]+punkty[0][2]*punkty[1][0]*punkty[2][1])-(punkty[0][2]*punkty[1][1]*punkty[2][0]+punkty[0][0]*punkty[1][2]*punkty[2][1]+punkty[0][1]*punkty[1][0]*punkty[2][2])
print('det(a,b,c) = '+str(det))
if det == 0:
	print(u"Punkty a, b, c są współliniowe")
else:
	print(u"Punkty a, b, c nie są współliniowe")