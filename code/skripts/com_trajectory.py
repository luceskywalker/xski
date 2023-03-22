import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from xski_utilites.signal import get_normalization_idx
import mvnx
idx = pd.IndexSlice


working_dir = Path().absolute().parent.parent/'files'
fp = working_dir/'cycle_temp_params.csv'
df = pd.read_csv(fp, index_col=[1,2], header=[0])
df.index.rename("participant", level=0, inplace=True)
df.index.rename("intensity", level=1, inplace=True)
df['stop_frame']=df['stop_frame'].astype('int')
df=df[df.columns[1:]]

# example slice
# df.loc[idx['P3','easy'],:]

participants = ['P3', 'P5', 'P6', 'P7', 'P8', 'P12', 'P13', 'P14']
intensities = ['easy', 'medium', 'hard']

com_dict = {
    'P3' : pd.DataFrame(index = range(101)),
    'P5' : pd.DataFrame(index = range(101)),
    'P6' : pd.DataFrame(index = range(101)),
    'P7' : pd.DataFrame(index = range(101)),
    'P8' : pd.DataFrame(index = range(101)),
    'P12' : pd.DataFrame(index = range(101)),
    'P13' : pd.DataFrame(index = range(101)),
    'P14' : pd.DataFrame(index = range(101))
}

for participant in participants:
    intensity_dict = {}
    for intensity in intensities:
        # load com data
        cp = Path(r'C:\Users\b1090197\Documents\Case Study Kit\Recordings') / participant / 'MVNX' / (
                    intensity + '_round_com.csv')
        com = pd.read_csv(cp, index_col=0)

        # get slice of interest
        slint = df.loc[participant].loc[intensity].sort_values(by='start_frame')
        # def comx_by_row(row, com_local=com):
        #     return [com_local['CoM pos x'][row['start_frame'] : row['stop_frame']].values - com_local['CoM pos x'][row['start_frame']]]
        def comx_by_row(row, com_local=com):
             a = com_local['CoM pos y'][row['start_frame'] : row['stop_frame']].values - com_local['CoM pos y'][row['start_frame']]
             b = com_local['CoM pos x'][row['start_frame'] : row['stop_frame']].values - com_local['CoM pos x'][row['start_frame']]
             return [np.linalg.norm([a,b], axis=0)]
        def comz_by_row(row, com_local=com):
            return [com_local['CoM pos z'][row['start_frame'] : row['stop_frame']].values - com_local['CoM pos z'][row['start_frame']]]
        slint['com_pos_x']=slint.apply(comx_by_row, axis=1)
        # slint['com_pos_y'] = slint.apply(comy_by_row, axis=1)
        slint['com_pos_z'] = slint.apply(comz_by_row, axis=1)

        tech_dict = {}
        for tech in set(slint['subtech'].values):
            subtech_df = pd.DataFrame(index = range(101))
            for i in range(len(slint['com_pos_z'][slint['subtech'] == tech])):
                x = slint['com_pos_x'][slint['subtech'] == tech].values[i][0]
                x_norm = x[get_normalization_idx(x,101)]
                z = slint['com_pos_z'][slint['subtech'] == tech].values[i][0]
                z_norm = z[get_normalization_idx(z,101)]

                subtech_df = pd.concat([subtech_df, pd.DataFrame(z_norm)], axis=1)

                #     plt.plot(z_norm, c='b')
            # plt.title(participant + intensity+tech, axis=1)
            # plt.show()

            # tech_dict[tech] = subtech_df
            tech_dict[tech] = pd.Series(np.mean(subtech_df, axis=1), name=tech)

        intensity_dict[intensity] = pd.concat(tech_dict, axis=1)

    com_dict[participant] = pd.concat(intensity_dict, axis=1)
com_df = pd.concat(com_dict, axis=1)
com_df.to_csv(working_dir/'mean_com_height.csv')








