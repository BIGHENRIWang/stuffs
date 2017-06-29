# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#
#labels='frogs','hogs','dogs','logs'
#sizes=15,20,45,10
#colors='yellowgreen','gold','lightskyblue','lightcoral'
#explode=0,0.1,0,0
#plt.pie(sizes,explode=explode,labels=labels,colors=colors,autopct='%1.1f%%',shadow=True,startangle=50)
#plt.axis('equal')
#plt.show()
#
#
#x = np.linspace(0, 10, 1000)
#y = np.sin(x)
#z = np.cos(x**2)
#
#plt.figure(figsize=(8,4))
#plt.plot(x,y,label="$sin(x)$",color="red",linewidth=2)
#plt.plot(x,z,"b--",label="$cos(x^2)$")
#plt.xlabel("Time(s)")
#plt.ylabel("Volt")
#plt.title("PyPlot First Example")
#plt.ylim(-1.2,1.2)
#plt.legend()
#plt.show()



dat = pd.read_csv("boe.csv", sep=",")

line_x = dat['x']
line_y = dat['y']
line_z = dat['z']

plt.figure(figsize=(9,5))
plt.plot(line_x, line_y, label="$boe crv$", color="gold", linewidth=2.5)
plt.xlabel("xposition")
plt.ylabel("yposition")
plt.title("Original boe curv")
plt.legend()
plt.show()






K = 5.6 
k_line_x = K * line_x 
k_line_y = K * line_y

plt.figure(figsize=(9,5))
plt.plot(k_line_x, k_line_y, label="$k_boe crv$", color="green", linewidth=2.5)
plt.scatter(k_line_x, k_line_y, marker='x', color='blue', alpha=0.7, label='pnts on crv')

plt.scatter(3.1,0,label="origin", color="red", marker="x")

plt.xlabel("xposition")
plt.ylabel("yposition")
plt.title("k- boe curv")
plt.legend()
plt.show()