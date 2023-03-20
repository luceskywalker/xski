import pickle
import pandas as pd
import numpy as np
from pathlib import Path
import mvnx
from xski_utilites.subphases import get_pole_off_dp

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

# cycle parameters
cycle_params_df = pd.DataFrame(columns=['participant', 'intensity', 'subtech', 'start_frame', 'stop_frame',
                                        'cycle_time', 'cycle_distance', 'cycle_speed'])

# start loop for dp Pole Off
all_score = {}
for participant in participants:
    part_score = {}
    #participant='P6'
    int_score = pd.Series()
    for intensity in intensities:
        gps = 1
        if participant in ['P3', 'P5', 'P6', 'P7', 'P12', 'P13']:

            # load gps_data
            gp = Path(r'C:\Users\b1090197\Documents\Case Study Kit\Recordings')/participant/'MVNX'/(intensity+'_round_gps.csv')
            gps = pd.read_csv(gp, index_col=0)

        for subtech in cycle_dict[participant][intensity].keys():

            cycles = {}
            for order in cycle_dict[participant][intensity][subtech].keys():
                cycles['cycle_time'] = np.diff(cycle_dict[participant][intensity][subtech][order])/240
                n_cyc = len(cycles['cycle_time'])
                cycles['subtech'] = np.repeat(subtech, n_cyc)
                cycles['participant'] = np.repeat(participant, n_cyc)
                cycles['intensity'] = np.repeat(intensity, n_cyc)
                cycles['start_frame'] = cycle_dict[participant][intensity][subtech][order][:-1]
                cycles['stop_frame'] = cycle_dict[participant][intensity][subtech][order][1:]


                cycles['cycle_distance'] = np.repeat(0, n_cyc)
                cycles['cycle_speed'] = np.repeat(0, n_cyc)
                if type(gps)== type(pd.DataFrame()):
                    current = cycle_dict[participant][intensity][subtech][order]
                    cycles['cycle_distance']=np.repeat(0, n_cyc)

                    dist = []

                    for jj in range(len(current)-1):
                        x = gps.values[current[jj]:current[jj+1], 1]
                        y = gps.values[current[jj]:current[jj+1], 0]
                        # substract start frame (offset) and convert to m
                        x = (x - x[0]) * 111139
                        y = (y - y[0]) * 111139
                        # calculate distance between 2 consecutive points
                        dx = np.diff(x)
                        dy = np.diff(y)
                        # total distance
                        distance = np.cumsum(np.linalg.norm([dx, dy], axis=0))[-1]
                        dist.append(distance)
                    cycles['cycle_distance'] = np.array(dist)
                    cycles['cycle_speed'] = cycles['cycle_distance']/cycles['cycle_time']*3.6
                cycle_params_df = pd.concat([cycle_params_df, pd.DataFrame(cycles)], axis=0)
        # dp score
        dp_dict = cycle_dict[participant][intensity]['dp']
        score = []
        for value in dp_dict.values():
            # get pole off values
            # value = dp_dict[12]

            for i in range(len(value)-1):
                # dp tech score
                tech_score = 0
                s1 = value[i]
                s2 = value[i+1]
                pole_off = get_pole_off_dp(s1,s2,joint_angles[participant][intensity])

                #print(pole_off)
                #pole_off = 37250

                # extract parameters
                # elbow angle at pole plant between 80 - 90°
                if (
                        joint_angles[participant][intensity]['Left Elbow Flexion/Extension'][s1] < 90
                ) and (
                        joint_angles[participant][intensity]['Left Elbow Flexion/Extension'][s1] > 80
                ) and (
                        joint_angles[participant][intensity]['Right Elbow Flexion/Extension'][s1] < 90
                ) and (
                        joint_angles[participant][intensity]['Right Elbow Flexion/Extension'][s1] > 80
                ):
                    print(participant + intensity+' good elbow')
                    tech_score +=1

                # shoulder angle > 80 °
                if (
                        joint_angles[participant][intensity]['Left Shoulder Flexion/Extension'][s1] > 80
                ) and (
                        joint_angles[participant][intensity]['Right Shoulder Flexion/Extension'][s1] > 80
                ):
                    print(participant + intensity+' good shoulder')
                    tech_score += 1

                # trunk angle between 50 and 60 °
                #  --> hip between 20 and 30° flexed
                if (
                        joint_angles[participant][intensity]['Left Hip Flexion/Extension'][s1] < 30
                ) and (
                        joint_angles[participant][intensity]['Left Hip Flexion/Extension'][s1] > 20
                ) and (
                        joint_angles[participant][intensity]['Right Hip Flexion/Extension'][s1] < 30
                ) and (
                        joint_angles[participant][intensity]['Right Hip Flexion/Extension'][s1] > 20
                ):
                    print(participant + intensity+' good hip')
                    tech_score += 1

                # knee angle < 40 °
                if (
                        joint_angles[participant][intensity]['Left Knee Flexion/Extension'][s1] < 40
                ) and (
                        joint_angles[participant][intensity]['Right Knee Flexion/Extension'][s1] < 40
                ):
                    print(participant + intensity+' good knee')
                    tech_score += 1

                # dorsiflex > 10 °
                if (
                        joint_angles[participant][intensity]['Left Ankle Dorsiflexion/Plantarflexion'][s1] > 10
                ) and (
                        joint_angles[participant][intensity]['Right Ankle Dorsiflexion/Plantarflexion'][s1] > 10
                ):
                    print(participant + intensity + ' good shank')
                    tech_score += 1

                ### criteria during push phase
                # elbow angle never bigger than 120°
                if (
                        np.max(joint_angles[participant][intensity]['Left Elbow Flexion/Extension'][s1:pole_off]) < 120
                ) and (
                        np.max(joint_angles[participant][intensity]['Right Elbow Flexion/Extension'][s1:pole_off]) < 120
                ):
                    print(participant + intensity + ' good ellbow push')
                    tech_score += 1

                # mean knee angle between 40 and 70°
                if (
                        np.mean(joint_angles[participant][intensity]['Left Knee Flexion/Extension'][s1:pole_off]) < 70
                ) and (
                        np.mean(joint_angles[participant][intensity]['Left Knee Flexion/Extension'][s1:pole_off]) > 40
                ) and (
                        np.mean(joint_angles[participant][intensity]['Right Knee Flexion/Extension'][s1:pole_off]) < 70
                ) and (
                        np.mean(joint_angles[participant][intensity]['Right Knee Flexion/Extension'][s1:pole_off]) > 40
                ):
                    print(participant + intensity+' good knee push')
                    tech_score += 1

                # ankle angle > 20 °
                if (
                        np.mean(
                            joint_angles[participant][intensity]['Left Ankle Dorsiflexion/Plantarflexion'][s1:pole_off]) > 20
                ) and (
                        np.mean(joint_angles[participant][intensity]['Left Ankle Dorsiflexion/Plantarflexion'][
                               s1:pole_off]) > 20
                ):
                    print(participant + intensity + ' good shank push')
                    tech_score += 1

            score.append(tech_score)

        # mean score for respective intensity
        int_score[intensity] = np.mean(np.array(score))
    part_score[participant] = int_score
    all_score[participant] = pd.DataFrame(part_score)
all_score = pd.concat(all_score, axis=1)

cycle_params_df.to_csv(working_dir/'cycle_temp_params.csv')










# gps.sort_values()
#
#
# s1, s2 = cycle_dict['P6']['easy']['dp'][1][6:8]

#get_pole_off(s1,s2, joint_angles['P6']['easy'])

a=12
