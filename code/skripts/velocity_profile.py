import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import glob
from pathlib import Path
from xski_utilites.signal import get_normalization_idx

# path
working_dir = Path().absolute().parent.parent/'files'
files = glob.glob(str(working_dir) + r'/subtech*.csv')
data_dir = Path(r'C:\Users\b1090197\Documents\Case Study Kit\Recordings')

# init empty dicts
v_dict = {
    'P3' : pd.DataFrame(index = range(101)),
    'P5' : pd.DataFrame(index = range(101)),
    'P6' : pd.DataFrame(index = range(101)),
    'P7' : pd.DataFrame(index = range(101)),
    'P12' : pd.DataFrame(index = range(101)),
    'P13' : pd.DataFrame(index = range(101))
}
p_dict = {
    'P3' : pd.DataFrame(index = range(101)),
    'P5' : pd.DataFrame(index = range(101)),
    'P6' : pd.DataFrame(index = range(101)),
    'P7' : pd.DataFrame(index = range(101)),
    'P12' : pd.DataFrame(index = range(101)),
    'P13' : pd.DataFrame(index = range(101))

}

# loop over all participants
for i, trial in enumerate(files):
    # get participant name and intensity
    participant = Path(trial).name.split('_')[1]
    intensity = Path(trial).name.split('_')[2][:-4]
    print(Path(trial).name[:-4])

    # read csv with times and subtechs
    df = pd.read_csv(trial, sep=';')

    # get gps data
    if participant == 'P14' or participant == 'P8':
        continue
    gps = pd.read_csv(data_dir/participant/'MVNX'/(intensity + '_round_gps.csv'), index_col=0)

    # mean distance
    # get intersting window
    gps = gps.iloc[df['last frame'][0]:df['last frame'].values[-1],:]

    # define x and y
    x = gps.values[:, 1]
    y = gps.values[:, 0]
    # substract start frame (offset) and convert to m
    x = (x - x[0]) * 111139
    y = (y - y[0]) * 111139
    # calculate distance between 2 consecutive points
    dx = np.diff(x)
    dy = np.diff(y)
    # total distance
    distance = np.cumsum(np.linalg.norm([dx, dy], axis=0))

    # velocity
    v = np.diff(distance) * 240  # correct for sampling rate
    v = v[np.argwhere(v > 0)]  # not continuous sampling
    velocity = v / round((len(distance) / len(v)))  # in m/s
    velocity *= 3.6  # convert to km/h

    # normalize to 101 points
    v_normalized=velocity[get_normalization_idx(velocity,101)]
    p_normalized=distance[get_normalization_idx(distance,101)]

    v_dict[participant] = pd.concat([v_dict[participant], pd.DataFrame(v_normalized, columns=[intensity])], axis=1)
    p_dict[participant] = pd.concat([p_dict[participant], pd.DataFrame(p_normalized, columns=[intensity])], axis=1)

v_df = pd.concat(v_dict, axis=1)
p_df = pd.concat(p_dict, axis=1)
v_df.to_csv(working_dir/'position_data.csv')
p_df.to_csv(working_dir/'velocity_data.csv')



