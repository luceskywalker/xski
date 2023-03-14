import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import glob
from pathlib import Path

# path
working_dir = Path().absolute().parent.parent/'files'
files = glob.glob(str(working_dir) + r'/subtech*.csv')
data_dir = Path(r'C:\Users\b1090197\Documents\Case Study Kit\Recordings')

subtechs = list(np.load('subtechs.npy', allow_pickle=False))

color_dict = {'dp': 'darkviolet',
              'diagonal': 'green',
              'glide': 'red',
              'fall': 'red'}
custom_lines = [Line2D([0], [0], color=color_dict['dp'], lw=4),
                Line2D([0], [0], color=color_dict['diagonal'], lw=4),
                Line2D([0], [0], color=color_dict['glide'], lw=4)]
# loop over all participants

for i, trial in enumerate(files):
    # get participant name and intensity
    participant = Path(trial).name.split('_')[1]
    intensity = Path(trial).name.split('_')[2][:-4]
    print(Path(trial).name[:-4])

    # read csv
    df = pd.read_csv(trial, sep=';')
    if i == 0:
        subtechs = list(df['sub-technique'])
    else:
        subtechs.extend(list(df['sub-technique']))

np.save('subtechs', list(set(subtechs)), allow_pickle=False)

    # while i < len(files)-1:
    #     continue
    #
    # gps = pd.read_excel(data_dir/participant/'MVNX'/(intensity + '_round.xlsx'), sheet_name='Global Position', index_col=0)
    # for k in range(len(df)-1):
    #     plt.plot(gps.iloc[df['last frame'].iloc[k]:df['last frame'].iloc[k+1],0], gps.iloc[df['last frame'].iloc[k]:df['last frame'].iloc[k+1],1], color = color_dict[df['sub-technique'].iloc[k+1]])
    # plt.legend(custom_lines, list(color_dict.keys())[:-1])
    # plt.title('Subtechnique Distribution - ' + participant + ' ' + intensity)
    # plt.show()



    # fig, ax = plt.subplots()
    # lines = ax.plot(data)
    # ax.legend(custom_lines, ['Cold', 'Medium', 'Hot'])







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
