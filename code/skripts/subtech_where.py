import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import glob
from pathlib import Path
from xski_utilites.signal import find_projection_index
from matplotlib.ticker import FormatStrFormatter


# path
working_dir = Path().absolute().parent.parent/'files'
files = glob.glob(str(working_dir) + r'/subtech*.csv')
data_dir = Path(r'C:\Users\b1090197\Documents\Case Study Kit\Recordings')
section_path = r'C:\Users\b1090197\OneDrive\Documents\XSki\xski\files\sections2.csv'
sec = pd.read_csv(section_path, sep=';', decimal=',')

# load list of all subtechniques
# subtechs = list(np.load('subtechs.npy', allow_pickle=False))

# create color dict for respective sub-tech
color_dict = {'glide': 'red',
              'dp': 'darkmagenta',
              'dp-kick': 'blue',
              'diagonal': 'aqua',
              'heringbone': 'green',
              'dp-skate': 'gold',
              'v1-skate': 'sandybrown',
              'skate': 'orange',
              'fall': 'black'}

# loop over all participants
d=[]
for i, trial in enumerate(files):
    # get participant name and intensity
    participant = Path(trial).name.split('_')[1]
    intensity = Path(trial).name.split('_')[2][:-4]
    print(Path(trial).name[:-4])

    # read csv
    df = pd.read_csv(trial, sep=';')

    # if i == 0:
    #     subtechs = list(df['sub-technique'])
    # else:
    #     subtechs.extend(list(df['sub-technique']))

# np.save('subtechs', list(set(subtechs)), allow_pickle=False)

    if participant == 'P14' or participant == 'P8':
        continue
    gps = pd.read_csv(data_dir/participant/'MVNX'/(intensity + '_round_gps.csv'), index_col=0)

    # mean distance
    # get intersting window
    gps1 = gps.iloc[df['last frame'][0]:df['last frame'].values[-1],:]

    # define x and y
    x = gps1.values[:, 1]
    y = gps1.values[:,0]
    # substract start frame (offset) and convert to m
    x = (x - x[0]) * 111139
    y = (y - y[0]) * 111139
    # calculate distance between 2 consecutive points
    dx = np.diff(x)
    dy = np.diff(y)
    # total distance
    distance = np.cumsum(np.linalg.norm([dx, dy], axis=0))

    # velocity
    v = np.diff(distance)*240                           # correct for sampling rate
    v = v[np.argwhere(v > 0)]                           # not continuous sampling
    velocity = v / round((len(distance)/len(v)))        # in m/s
    velocity *= 3.6                                     # convert to km/h


    # calculate projection of split points
    projections = pd.DataFrame(index = sec.index, columns=['Longitude', 'Latitude'])
    for split_point in sec.index:
        long_p = sec.loc[split_point]['Longitude']
        lat_p = sec.loc[split_point]['Latitude']
        projections.loc[split_point] = gps.loc[find_projection_index(gps, long_p, lat_p)].iloc[:2]

    # get uphill technique
    # tech_up=[]
    # for split_point in [0,3]:
    #     long_s = sec.loc[split_point]['Longitude']
    #     lat_s = sec.loc[split_point]['Latitude']
    #     start = find_projection_index(gps, long_s, long_s)
    #     long_f = sec.loc[split_point+1]['Longitude']
    #     lat_f = sec.loc[split_point+1]['Latitude']
    #     finish = find_projection_index(gps, long_f, long_f)



    # for k in range(len(df)-1):
    #     # plot segment in color corresponding to subtechnique from color dict
    #     plt.plot(gps.iloc[df['last frame'].iloc[k]:df['last frame'].iloc[k+1],1], gps.iloc[df['last frame'].iloc[k]:df['last frame'].iloc[k+1],0], color = color_dict[df['sub-technique'].iloc[k+1]], lw=4)
    #

    fig, ax = plt.subplots()
    fig.suptitle('Subtechnique Distribution - ' + participant + ' ' + intensity)
    for k in range(len(df)-1):
        # plot segment in color corresponding to subtechnique from color dict
        ax.plot(gps.iloc[df['last frame'].iloc[k]:df['last frame'].iloc[k+1],1], gps.iloc[df['last frame'].iloc[k]:df['last frame'].iloc[k+1],0], color = color_dict[df['sub-technique'].iloc[k+1]], lw=4)
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    # custum legend
    custom_lines = []
    for subtec in df['sub-technique'].iloc[1:].unique():
        custom_lines.append(Line2D([0], [0], color=color_dict[subtec], lw=4))
        #
        # [Line2D([0], [0], color=color_dict['dp'], lw=4),
        #             Line2D([0], [0], color=color_dict['diagonal'], lw=4),
        #             Line2D([0], [0], color=color_dict['glide'], lw=4)]
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.legend(custom_lines, df['sub-technique'].iloc[1:].unique())
    # plt.title('Subtechnique Distribution - ' + participant + ' ' + intensity)

    # plot section points
    # for point in sec.index:
    #     marker = 'ko'
    #     plt.plot(sec.loc[point]['Longitude'], sec.loc[point]['Latitude'], marker, markersize=8)
    for split in projections.index:
        marker = 'bo'
        plt.plot(projections.loc[split]['Longitude'], projections.loc[split]['Latitude'], marker, markersize=8)
    plt.show()

    #
    # fig, ax = plt.subplots()
    # lines = ax.plot(data)
    # ax.legend(custom_lines, ['Cold', 'Medium', 'Hot'])
    #



# distance
# x = gps.values[:,1]
# x=(x-x[0]) * 111139
# dx = np.diff(x)
# distance = np.cumsum(np.linalg.norm([dx,dy], axis=0))
#
#
#


    # # substract offset
    # df['last frame'] = df['last frame'] - df['last frame'].loc[0]
    #
    # # calculate relative technique distribution (relative to total time)
    # df['relative1'] = df['last frame']*100//df['last frame'].iloc[-1]
    # df['relative2'] = df['last frame'] / df['last frame'].iloc[-1]
    # df['relative3'] = round(df['last frame'] * 100 / df['last frame'].iloc[-1])
    #
    # # collect all sub-techniques
    # if i == 0:
    #     subtechs = list(df['sub-technique'])
    # else:
    #     subtechs.extend(list(df['sub-technique']))
    # a=12
    #
