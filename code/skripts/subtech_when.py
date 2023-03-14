import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import glob
from pathlib import Path

# path
working_dir = Path().absolute().parent.parent/'files'
files = glob.glob(str(working_dir) + r'/subtech*.csv')

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

# participants & intensities
participants = ['P3', 'P5', 'P6', 'P7', 'P8', 'P12', 'P13', 'P14']
intensities = ['easy', 'medium', 'hard']

part_dict = {}
for participant in participants:
    int_dict = {}
    for intensity in intensities:
        print(participant + ' ' + intensity)
        trial = working_dir/('subtech_' + participant + '_' + intensity + '.csv')

        # read csv
        df = pd.read_csv(trial, sep=';')

        total_frames = df['last frame'].values[-1] - df['last frame'].values[0]

        # caculate times in respective gears (excluding start)
        techs_dict = {}
        techs_dict['Time [s]'] = total_frames/240

        for gear in df['sub-technique'].iloc[1:].unique():
            gear_frames=0
            for idx in df[df['sub-technique']==gear].index:
                gear_frames += df.loc[idx]['last frame'] - df.loc[idx-1]['last frame']
            techs_dict[gear + ' [%]'] = gear_frames/total_frames*100

        int_dict[intensity] = pd.Series(techs_dict)
    int_df = pd.DataFrame(int_dict).T
    part_dict[participant] = int_df

# create multiindex df with all data
part_df = pd.concat(part_dict, axis=0)
part_df.fillna(0, inplace=True)
part_df.to_csv(working_dir/'subtech_all.csv', index_label=['Participant', 'Intensity'])


