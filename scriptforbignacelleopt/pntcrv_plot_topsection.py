# -*- coding: utf-8 -*-
__author__ = "BIGHENRIWang"
import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='foilontoNacsection.log',
                    filemode='w')
logger = logging.getLogger(__name__)



logger.info('assign the original good to-be-sub airfoil data, prepare it with columns separated by nothing but comma')
dat = pd.read_csv("syj.csv", sep=",")

line_x = dat['x']
line_y = dat['y']
line_z = dat['z']


#adaption to local section...

#exact local length
K = 5.6495224

Ax = 1.798490
Ay = 1.28520
Az = 0.0

Bx = 7.366000
By = 1.440269000000
Bz = 0.0

Cx = 1.716405
Cy = 1.390650000000
Cz = 0.0

#
# #local A point coordination
# Ax = 1.904129
# Ay = 1.427906
# Az = -0.03304653
#
# #local B point coordination
# Bx = 7.366
# By = 1.439885
# Bz = -0.03332581
#
# #local C point coordination
# Cx = 1.841189
# Cy = 1.535586
# Cz = -0.03554083


k_line_x = K * line_x
k_line_y = K * line_y
k_line_z = K * line_z


plt.figure(figsize=(9,5))
ax = plt.gca()
# ax.set_aspect('equal')

#plot A point
plt.scatter(Ax,Ay,label="A point", color="red", marker="p")

#plot B point
plt.scatter(Bx,By,label="B point", color="blue", marker="p")

#plot C point
plt.scatter(Cx,Cy,label="C point", color="black", marker="p")


logger.info("move to the B point")
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

for i in range(-1335000,-1333000):
    i = i / 10000
    # calculate intial angle phi for each position
    delta_y = k_line_y - By
    delta_x = k_line_x - Bx
    delta_dist = np.sqrt(delta_x * delta_x + delta_y * delta_y)
    phi = np.arctan(delta_y / delta_x)

    if not i == 0.0:
        theta = math.pi/i + math.pi
    else:
        theta = math.pi

    phi_new = phi - theta
    new_k_line_x = Bx + abs(delta_dist) * np.cos(phi_new)
    new_k_line_y = By + abs(delta_dist) * np.sin(phi_new)

    for index in range(pnt_num):
        dist = cal_dist(new_k_line_x[index], new_k_line_y[index], Ax, Ay)
        if dist < shortest_dist:
            shortest_dist = dist
            shortest_dist_index = index
            shortest_dist_x = new_k_line_x[index]
            shortest_dist_y = new_k_line_y[index]
            shortest_dist_i = i

logger.info("shortest distance:{}".format(shortest_dist) )
logger.info("shortest distance: the nearest point to B (x,y):{},{}".format(shortest_dist_x, shortest_dist_y) )
logger.info("shortest distance: rotating angle: pi / {}".format(shortest_dist_i) )
logger.info("shortest distance: index of the nearest point to B: {}".format(shortest_dist_index) )

delta_y = k_line_y - By
delta_x = k_line_x - Bx
phi = np.arctan(delta_y / delta_x)
theta = math.pi / shortest_dist_i + math.pi
phi_new = phi - theta
# new_k_line_x = Bx + abs(delta_x) * np.cos(phi_new)
# new_k_line_y = By + abs(delta_x) * np.sin(phi_new)
new_k_line_x[0] = Bx
new_k_line_y[0] = By
new_k_line_x[1:-1] = Bx + abs(delta_dist[1:-1]) * np.cos(phi_new[1:-1])
new_k_line_y[1:-1] = By + abs(delta_dist[1:-1]) * np.sin(phi_new[1:-1])
print(new_k_line_x[0])
print(new_k_line_y[0])

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
# print(result_df.info)
# result_df.to_csv("newfoilcrv_posn_complete.csv", sep=" ", header=True)


new_k_line_x = new_k_line_x.iloc[0:shortest_dist_index]
new_k_line_y = new_k_line_y.iloc[0:shortest_dist_index]

new_k_line_x.iloc[-1] = shortest_dist_x
new_k_line_y.iloc[-1] = shortest_dist_y
# print(new_k_line_x.size)
# print(new_k_line_y.size)
result_df = pd.concat([new_k_line_x, new_k_line_y], axis =1)
logger.debug(result_df.info)

new_k_line_x.iloc[-1] = Ax
new_k_line_y.iloc[-1] = Ay


result_df = pd.concat([new_k_line_x, new_k_line_y], axis =1)
logger.debug(result_df.info)

z_size = new_k_line_x.size
z_step = Bz - Az
z_step = z_step / (z_size - 1 )

new_k_line_z = []

for index in range(z_size):
    new_k_line_z.append( Bz - z_step * index)

print(new_k_line_z[0])
print(new_k_line_z[-1])
new_k_line_z = pd.Series(new_k_line_z, index=None)


print(new_k_line_x.size)
print(new_k_line_y.size)
print(new_k_line_z.size)

print(new_k_line_x[0])
print(new_k_line_y[0])
print(new_k_line_z[0])


result_df = pd.concat([new_k_line_x, new_k_line_z, new_k_line_y], axis =1)
logger.debug(result_df.info)
result_df.to_csv("newfoilcrv_posn_last_withz.csv", sep=" ", header=True, index=False )
