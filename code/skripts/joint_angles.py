import pickle
import pandas as pd
import numpy as np
from pathlib import Path
import mvnx
from xski_utilites.signal import get_normalization_idx, low_pass_filter

working_dir = Path().absolute().parent.parent/'files'
with open(str(working_dir/'ski_cycles.pkl'), 'rb') as f:
    cycle_dict = pickle.load(f)

fp = Path(r'C:\Users\b1090197\Documents\Case Study Kit\Recordings')
with open(str(fp/'erg_joint_angles.pkl'), 'rb') as f:
    erg_joint_angles = pickle.load(f)
with open(str(fp/'joint_angles.pkl'), 'rb') as f:
    joint_angles = pickle.load(f)

participants = ['P3', 'P5', 'P6', 'P7', 'P8', 'P12', 'P13', 'P14']
intensities = ['easy', 'medium', 'hard']
joints = ['Left Elbow','Right Elbow', 'Left Shoulder', 'Right Shoulder', 'Left Hip', 'Right Hip', 'Left Knee', 'Right Knee']
n = 101

# init joint angle dicts
ja_dict = {
    'P3' : pd.DataFrame(index = range(n)),
    'P5' : pd.DataFrame(index = range(n)),
    'P6' : pd.DataFrame(index = range(n)),
    'P7' : pd.DataFrame(index = range(n)),
    'P8' : pd.DataFrame(index = range(n)),
    'P12' : pd.DataFrame(index = range(n)),
    'P13' : pd.DataFrame(index = range(n)),
    'P14' : pd.DataFrame(index = range(n))
}


# start loop for dp Pole Off
for participant in participants:
    intensity_dict={}
    for intensity in intensities:
        subtech_dict = {}
        for subtech in cycle_dict[participant][intensity].keys():

            # array3 = np.empty([n, len(joints)])
            k = 0
            for order in cycle_dict[participant][intensity][subtech].keys():

                s1 = cycle_dict[participant][intensity][subtech][order][:-1]
                s2 = cycle_dict[participant][intensity][subtech][order][1:]

                current = joint_angles[participant][intensity]


                for i in range(len(s1)):
                    ja_df = pd.DataFrame(index = range(n), columns=joints)
                    for joint in joints:
                        # get joint angles
                        ja = current[joint + ' Flexion/Extension'][s1[i]:s2[i]]
                        # filter
                        # ja = low_pass_filter(ja,120,2,2)
                        # normalize
                        ja_df[joint] = ja[get_normalization_idx(ja, n)]
                    if k == 0:
                        array3 = ja_df.values
                        k = 1
                    else:
                        array3=np.hstack([array3, ja_df.values])

            # reshape and safe
            sig = np.mean(np.reshape(array3, [n, len(joints), -1], order='F'), axis=2)
            #sig_filt = low_pass_filter(sig,240,12,2)
            sig_filt=sig
            subtech_dict[subtech] = pd.DataFrame(sig_filt, columns=joints)
        intensity_dict[intensity] = pd.concat(subtech_dict, axis=1)
    ja_dict[participant] = pd.concat(intensity_dict, axis=1)
ja_all_df = pd.concat(ja_dict, axis=1)
ja_all_df.to_csv(working_dir/'joint_angles.csv')

















# gps.sort_values()
#
#
# s1, s2 = cycle_dict['P6']['easy']['dp'][1][6:8]

#get_pole_off(s1,s2, joint_angles['P6']['easy'])

a=12
