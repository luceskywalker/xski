import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path
import glob
from xski_utilites.signal import find_projection_index

# path
working_dir = Path().absolute().parent.parent/'files'
files = glob.glob(str(working_dir) + r'/subtech*.csv')
data_dir = Path(r'C:\Users\b1090197\Documents\Case Study Kit\Recordings')
section_path = r'C:\Users\b1090197\OneDrive\Documents\XSki\xski\files\sections2.csv'

sec = pd.read_csv(section_path, sep=';', decimal=',')

participants = ['P3', 'P5', 'P6', 'P7', 'P12', 'P13']
intensities = ['easy', 'medium', 'hard']


# init empty dicts
segments = ['seg1_flat', 'seg2_up', 'seg3_down', 'seg4_turn', 'seg5_up', 'seg6_down', 'seg7_flat']

segtime_dict = {
    'P3' : pd.DataFrame(index = segments),
    'P5' : pd.DataFrame(index = segments),
    'P6' : pd.DataFrame(index = segments),
    'P7' : pd.DataFrame(index = segments),
    'P12' : pd.DataFrame(index = segments),
    'P13' : pd.DataFrame(index = segments)
}
splits_dict = {
    'P3' : pd.DataFrame(index = segments),
    'P5' : pd.DataFrame(index = segments),
    'P6' : pd.DataFrame(index = segments),
    'P7' : pd.DataFrame(index = segments),
    'P12' : pd.DataFrame(index = segments),
    'P13' : pd.DataFrame(index = segments)
}

# start loop
for i, trial in enumerate(files):
    # get participant name and intensity
    participant = Path(trial).name.split('_')[1]
    intensity = Path(trial).name.split('_')[2][:-4]
    print(Path(trial).name[:-4])

    if participant == 'P14' or participant == 'P8':
        continue

    if participant == 'P5':
        zz = 2

    # read csv subtech data
    df = pd.read_csv(trial, sep=';')

    # read in gps data
    gps = pd.read_csv(data_dir/participant/'MVNX'/(intensity + '_round_gps.csv'), index_col=0)

    # get intersting window
    gps1 = gps.iloc[df['last frame'][0]:df['last frame'].values[-1],:]

    # get split indices
    projection_idx = {}
    projection_idx['start'] = gps1.index[0]
    for split_point in sec.index:
        long_p = sec.loc[split_point]['Longitude']
        lat_p = sec.loc[split_point]['Latitude']
        projection_idx[sec.loc[split_point]['Section']] = find_projection_index(gps1, long_p, lat_p)
    projection_idx['finish'] = gps1.index[-1]

    # get split times
    segment_time = np.diff(pd.Series(projection_idx))/240
    split_time = np.cumsum(segment_time)

    # convert to DataFrame and safe in dict
    segtime_dict[participant] = pd.concat([segtime_dict[participant], pd.DataFrame(segment_time, index= segments, columns=[intensity])], axis=1)
    splits_dict[participant] = pd.concat([splits_dict[participant], pd.DataFrame(split_time, index= segments, columns=[intensity])], axis=1)

# concat to multiindex df
segtime_df = pd.concat(segtime_dict, axis=1)
splits_df = pd.concat(splits_dict, axis=1)

# save
segtime_df.T.to_csv(working_dir/'segment_times_T.csv')
splits_df.T.to_csv(working_dir/'split_times_T.csv')
print('success')
