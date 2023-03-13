import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
from pathlib import Path

# path
working_dir = Path().absolute().parent.parent/'files'
files = glob.glob(str(working_dir) + r'/subtech*.csv')

# loop over all participants
for i, trial in enumerate(files):
    # get participant name and intensity
    participant = Path(trial).name.split('_')[1]
    intensity = Path(trial).name.split('_')[2][:-4]

    # read csv
    df = pd.read_csv(trial, sep=';')

    # substract offset
    df['last frame'] = df['last frame'] - df['last frame'].loc[0]

    # calculate relative technique distribution (relative to total time)
    df['relative1'] = df['last frame']*100//df['last frame'].iloc[-1]
    df['relative2'] = df['last frame'] / df['last frame'].iloc[-1]
    df['relative3'] = round(df['last frame'] * 100 / df['last frame'].iloc[-1])

    # collect all sub-techniques
    if i == 0:
        subtechs = list(df['sub-technique'])
    else:
        subtechs.extend(list(df['sub-technique']))
    a=12

