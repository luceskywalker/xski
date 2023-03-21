from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from scipy.signal import find_peaks
from xski_utilites.signal import low_pass_filter_series, find_projection_index
from xski_utilites.fill3d import fill_between_3d
from xski_utilites.bonus import get_mu_mixed



os.chdir(r'C:\Users\b1090197\Documents\Case Study Kit\Recordings\GPS RTK data')
subject = 13
file = "P"+ str(subject) + "_coord.xlsx"
df = pd.read_excel(file)

coordinates = pd.DataFrame()
coordinates['Longitude'] = (df["Longitude"] / 10000000)
coordinates['Latitude'] = (df["Latitude"] / 10000000)
coordinates['Height'] = ((df["Height"]/ 1000))

# filter and smooth path
c_filt = coordinates.apply(low_pass_filter_series, axis=0)

mu_mixed = get_mu_mixed()
runde = c_filt.loc[1235:1760]
m_mixed = mu_mixed[1235:1760]
# define x and y
x = runde['Longitude'].values
y = runde['Latitude'].values
# substract start frame (offset) and convert to m
x = (x - x[0]) * 111139
y = (y - y[0]) * 111139
# calculate distance between 2 consecutive points
dx = np.diff(x)
dy = np.diff(y)
# total distance
distance = np.cumsum(np.linalg.norm([dx, dy], axis=0))
runde = runde.iloc[:-1,:]

### debug points
# h = runde['Height'].values
# spoints = h[[204,246,270,336,365,403]]
# indexes = [runde[runde['Height']==x].index.values for x in spoints]
# a=12
# p, _ = find_peaks(h, height = 959)
# plt.plot(h)
# plt.plot(p, h[p], 'ro',  markersize=6)
# plt.show()
#
# h = -h
# p, _ = find_peaks(h)
# plt.plot(h)
# plt.plot(p, h[p], 'ro',  markersize=6)
# plt.show()


# split points
section_path = r'C:\Users\b1090197\OneDrive\Documents\XSki\xski\files\sections2.csv'
sec = pd.read_csv(section_path, sep=';', decimal=',')
# calculate projection
projection_idx = {}
for split_point in sec.index:
    long_p = sec.loc[split_point]['Longitude']
    lat_p = sec.loc[split_point]['Latitude']
    projection_idx[sec.loc[split_point]['Section']] = find_projection_index(runde, long_p, lat_p)


# color dict
colordict = {'flat 1':'grey',
             'uphill 1': 'red',
             'downhill 1':'green',
             'turn':'darkkhaki',
             'uphill 2':'red',
             'downhill 2':'green',
             'flat 2':'grey'}

i=0
fig, ax = plt.subplots()
fig.suptitle('Track Profile')
ax.plot(distance, runde['Height'], color='grey')

for idx, section in zip(projection_idx.values(), colordict.keys()):
    ax.plot(distance[idx], runde['Height'].iloc[idx], 'ko', markersize=6)
    ax.fill_between(distance[i:idx], runde['Height'].iloc[i:idx], 0, color=colordict[section], alpha=.5, label = section)
    i = idx
ax.fill_between(distance[idx:], runde['Height'].iloc[idx:], 0, color=colordict['flat 2'], alpha=.5, label = 'flat 2')
ax.set_ylim(min(runde['Height'].iloc[1:])-1, max(runde['Height'].iloc[1:])+1)
ax.set_xlim(0, max(distance))
ax.set_xlabel('Distance [m]')
ax.set_ylabel('Altitude [m]')
plt.legend()
plt.show()
#plt.plot(distance, runde['Height'].iloc[1:])
#plt.show()
# a=12

# # plt.figure()
# # ax = plt.axes(projection='3d')
# # ax.plot3D(c_filt['Longitude'], c_filt['Latitude'], c_filt['Height'])
#
# #
set1 = runde.values
set2 = np.hstack([runde.values[:,:2], np.ones([len(set1),1])*(min(runde['Height'])-.5)])
set1=set1.T
set2=set2.T

fig = plt.figure()
fig.suptitle('Track Profile')
ax = fig.add_subplot(111, projection='3d')

# this is new
# segs = np.concatenate([set1[:-1],set1[1:]],axis=1)
# lc = Line3DCollection([*set1, *set1], cmap=plt.get_cmap('jet'))
# line = ax.add_collection3d(lc)
# plt.show()
#
# lc.set_array(mu_mixed) # color the segments by our parameter
# ax = fig.add_subplot(111, projection='3d')
# line = ax.add_collection3d(lc)
# cmap = fig.colorbar(line, ax=ax)
# cmap.set_label(label='snow friction',size=15, labelpad=0)


ax.plot(*set1, lw=2, c='grey')
ax.plot(*set2, lw=2, c='grey')


i = 0
for idx, section in zip(projection_idx.values(), colordict.keys()):
    fill_between_3d(ax, *set1[:,i:idx], *set2[:,i:idx], c=colordict[section], alpha=.8)
    i = idx
fill_between_3d(ax, *set1[:,i:], *set2[:,i:], c=colordict['flat 2'], alpha=.8)
# ax.fill_between(distance[idx:], runde['Height'].iloc[idx:], 0, color=colordict['flat 2'], alpha=.5, label = 'flat 2')
#
#
# ax.plot(*set1, lw=4)
# ax.plot(*set2, lw=4)
# fill_between_3d(ax, *set1, *set2, mode = 1)
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_zlabel('Altitude [m]')
plt.show()

