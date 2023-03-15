from IPython import get_ipython
get_ipython().magic("reset -sf")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import pickle
from scipy import signal
from scipy.signal import find_peaks
    

os.chdir('C:/Users/Matteo/Downloads/salzburg/projects/movella challenge/xski/files')

subjects= np.array([3, 5, 6, 7, 8, 12, 13, 14])
intensities = ["easy", "medium", "hard"]
fs = 240
window = int(0.3*fs) # seconds in samples
sub_techniques = ["dp", "dp-skate", "dp-kick", "diagonal", "heringbone"]

##################################### loading from excel ##################################
"""
intens = dict()
part = dict()
for subj in subjects:
    for intensity in intensities:
        
        name = "P" + str(subj) + "_" + intensity + "_round.xlsx"
        df = pd.read_excel(name, sheet_name = "Ergonomic Joint Angles ZXY", usecols ="B:S")
        data_round = dict(zip(df.T.index, df.T.values))
      
        if data_round:
           intens[intensity]=data_round.copy()
        data_round.clear()  

    if intens:
       part["P"+ str(subj)]=intens.copy()
    intens.clear()                    

      
import pickle
f = open("C:/Users/Matteo/Downloads/salzburg/projects/movella challenge/xski/files/erg_joint_angles.pkl","wb")
pickle.dump(part,f)
f.close()
"""
#######################################################################################################
###### load dictionary
file = open("C:/Users/Matteo/Downloads/salzburg/projects/movella challenge/file esportati/raw_acc_poles.pkl",'rb')
acc = pickle.load(file)
file.close()

file = open("C:/Users/Matteo/Downloads/salzburg/projects/movella challenge/file esportati/erg_joint_angles.pkl",'rb')
erg_ja = pickle.load(file)
file.close()

for participant in subjects:
    for intensity in intensities:

        frame = pd.read_csv("subtech_P" + str(participant) + "_" + intensity + ".csv", sep =";")
        
        res_left = np.sqrt(acc["P" + str(participant)][intensity]["Prop Tracker 3 x"]**2 + 
                       acc["P" + str(participant)][intensity]["Prop Tracker 3 y"]**2 + 
                       acc["P" + str(participant)][intensity]["Prop Tracker 3 z"]**2)

        b,a= signal.butter(4, 10/(fs/2), 'Lowpass') # filter at 10/0
        resultant_left = signal.filtfilt(b,a, res_left) # left pole

        plt.figure()
        plt.plot(resultant_left)
        
        for technique in sub_techniques:
            tech_where = frame.index[frame['sub-technique'] == technique].tolist()
            
            if tech_where:
                
                for interval in tech_where:
                    start = frame["last frame"][interval-1].astype(int)
                    end = frame["last frame"][interval].astype(int)
                    
                    #left side
                    shoulder_left = erg_ja["P" + str(participant)][intensity]["T8_LeftUpperArm Flexion/Extension"]
                    peaks, _ = find_peaks(shoulder_left[start:end], height = 40, distance = 0.5*fs) # at least 40° and 50 samples apart
                    peaks_sh = list(peaks + start)
                    
                    acc_peaks_left = np.array([])
                    for peak in peaks_sh:
                        
                        if peak-window >0:
                            low_bound = peak-window 
                        else:
                            low_bound = 0
                            
                        if peak+window < len(shoulder_left)-1:
                            up_bound = peak+window 
                        else:
                            low_bound = len(shoulder_left)-1
                        
                        
                        max_window = max(resultant_left[low_bound: up_bound])
                        acc_peaks_left = np.append(acc_peaks_left, 
                                              list(resultant_left[low_bound: up_bound]).index(max_window) + low_bound)
                    
                    
                    acc_peaks_left = acc_peaks_left.astype(int)
                    plt.plot(acc_peaks_left, resultant_left[acc_peaks_left], "v", color="red")
                    del start, end
                    
                    plt.figure()
                    plt.plot(shoulder_left)
                    plt.plot(resultant_left)


plt.plot(shoulder_left)
plt.plot(peaks_sh, shoulder_left[peaks_sh], "v", color="red")


