# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
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



dat = pd.read_csv("boe.csv", sep=",")

line_x = dat['x']
line_y = dat['y']
line_z = dat['z']

# plt.figure(figsize=(9,5))
# plt.plot(line_x, line_y, label="$boe crv$", color="gold", linewidth=2.5)
# plt.xlabel("xposition")
# plt.ylabel("yposition")
# plt.title("Original boe curv")
# plt.legend()
# plt.show()

#adaption to local section...

#exact local length
K = 5.6

#local A point coordination
Ax = 1.904129
Ay = 1.427906
Az = -0.03304653

#local B point coordination
Bx = 7.366
By = 1.439885
Bz = -0.03332581

k_line_x = K * line_x 
k_line_y = K * line_y
k_line_z = K * line_z

print('the minimum index')
print(k_line_x.idxmin())
print(k_line_x.iloc[k_line_x.idxmin()])
print(k_line_y.iloc[k_line_y.idxmin()])
print(k_line_z.iloc[k_line_z.idxmin()])

leftest_x = k_line_x.iloc[k_line_x.idxmin()]
leftest_y = k_line_y.iloc[k_line_x.idxmin()]
leftest_z = k_line_z.iloc[k_line_x.idxmin()]




plt.figure(figsize=(9,5))
ax = plt.gca()
# ax.set_aspect('equal')


#plot A point
plt.scatter(Ax,Ay,label="A point", color="red", marker="p")

#plot B point
plt.scatter(Bx,By,label="B point", color="blue", marker="p")

#move to the B point

translation_x = Bx - k_line_x.iloc[0]
translation_y = By - k_line_y.iloc[0]

k_line_x = k_line_x + translation_x
k_line_y = k_line_y + translation_y


original_k_line_x = k_line_x
original_k_line_y = k_line_y






#here you input the desired angle changement
pnt_num = k_line_x.size

def cal_dist(x1,y1,x2,y2):
    delta_x = x1 - x2
    delta_y = y1-y2
    delta_dist = np.sqrt(delta_x * delta_x + delta_y * delta_y)
    return delta_dist



shortest_dist = 10
shortest_dist_index = 0
shortest_dist_x = 0
shortest_dist_y = 0
shortest_dist_i =10

for i in range(200,250,1):

    # calculate intial angle phi for each position
    delta_y = k_line_y - By
    delta_x = k_line_x - Bx
    delta_dist = np.sqrt(delta_x * delta_x + delta_y * delta_y)
    phi = np.arctan(delta_y / delta_x)

    theta = math.pi/i + math.pi

    phi_new = phi - theta
    new_k_line_x = Bx + abs(delta_x) * np.cos(phi_new)
    new_k_line_y = By + abs(delta_x) * np.sin(phi_new)


    for index in range(pnt_num):
        dist = cal_dist(new_k_line_x[index], new_k_line_y[index], Ax, Ay)
        if dist < shortest_dist:
            shortest_dist = dist
            shortest_dist_index = index
            shortest_dist_x = new_k_line_x[index]
            shortest_dist_y = new_k_line_y[index]
            shortest_dist_i = i
    else:
        print('maybe there is something wrong in this theta angle!')

print("shortest distance, etc.:")
print(shortest_dist)
print(shortest_dist_x)
print(shortest_dist_y)
print(shortest_dist_i)
print(shortest_dist_index)

delta_y = k_line_y - By
delta_x = k_line_x - Bx
phi = np.arctan(delta_y / delta_x)
theta = math.pi / shortest_dist_i + math.pi
phi_new = phi - theta
new_k_line_x = Bx + abs(delta_x) * np.cos(phi_new)
new_k_line_y = By + abs(delta_x) * np.sin(phi_new)
#
# new_crv = pd.concat(new_k_line_x, new_k_line_y)
# new_crv.to_csv("result.csv")
#


# print(result_df)

#plot k'ed airfoil boe
plt.scatter(original_k_line_x, original_k_line_y, marker='x', color='green', alpha=0.7, label='original airfoil curve')
plt.scatter(new_k_line_x, new_k_line_y, marker='x', color='blue', alpha=0.7, label='rotated airfoil curve')
plt.scatter(shortest_dist_x, shortest_dist_y, marker='>', color='red', alpha=0.7, label='the nearest pnt')

plt.xlabel("xposition")
plt.ylabel("yposition")
plt.title("crvs and pnts")
plt.legend()
# plt.show()
plt.savefig("the picture.pdf")

result_df = pd.concat([new_k_line_x, new_k_line_y], axis =1)
print(result_df.info)
result_df.to_csv("newfoilcrv_posn_complete.csv", sep=" ", header=True)



new_k_line_x = new_k_line_x.iloc[0:shortest_dist_index]
new_k_line_y = new_k_line_y.iloc[0:shortest_dist_index]
new_k_line_x.iloc[-1] = shortest_dist_x
new_k_line_y.iloc[-1] = shortest_dist_y
print(new_k_line_x.size)
print(new_k_line_y.size)
result_df = pd.concat([new_k_line_x, new_k_line_y], axis =1)
print(result_df.info)
result_df.to_csv("newfoilcrv_posn_medium.csv", sep=" ", header=True)


new_k_line_x.iloc[-1] = Ax
new_k_line_y.iloc[-1] = Ay
result_df = pd.concat([new_k_line_x, new_k_line_y], axis =1)
print(result_df.info)
result_df.to_csv("newfoilcrv_posn_last.csv", sep=" ", header=True)

