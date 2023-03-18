from IPython import get_ipython
get_ipython().magic("reset -sf")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import pickle
from scipy import signal
from scipy.signal import find_peaks
  

os.chdir('C:/Users/Matteo/Downloads/salzburg/projects/movella challenge/file esportati/CoM')
plt.close("all")
subjects= np.array([3, 5, 6, 7, 8, 12, 13, 14])
intensities = ["easy", "medium", "hard"]
fs = 240
wind_part = (np.array([0.25, 0.15, 0.2, 0.2, 0.2, 0.2, 0.25, 0.2])*fs).astype(int)
dist_part = (np.array([0.8, 0.7, 0.6, 0.6, 0.7, 0.6, 0.7, 0.7])*fs).astype(int)
sub_techniques = ["dp", "dp-skate", "dp-kick", "diagonal", "heringbone"]

##################################### loading from excel ##################################

intens = dict()
part = dict()
for subj in subjects:
    for intensity in intensities:
        
        name = "P" + str(subj) + "_" + intensity + "_round.xlsx"
        df = pd.read_excel(name, sheet_name = "Center of Mass", usecols ="B:D")
        data_round = dict(zip(df.T.index, df.T.values))
      
        if data_round:
           intens[intensity]=data_round.copy()
        data_round.clear()  

    if intens:
       part["P"+ str(subj)]=intens.copy()
    intens.clear()                    

      
f = open("C:/Users/Matteo/Downloads/salzburg/projects/movella challenge/file esportati/com_position.pkl","wb")
pickle.dump(part,f)
f.close()

#######################################################################################################
###### load dictionary
file = open("C:/Users/Matteo/Downloads/salzburg/projects/movella challenge/file esportati/raw_acc_poles.pkl",'rb')
acc = pickle.load(file)
file.close()

file = open("C:/Users/Matteo/Downloads/salzburg/projects/movella challenge/file esportati/erg_joint_angles.pkl",'rb')
erg_ja = pickle.load(file)
file.close()

partd = dict()
intensd = dict()
techd = dict()
intervd = dict()



counter = -1
for participant in subjects:
    counter += 1
    
    for intensity in intensities:
        #plt.figure()

        frame = pd.read_csv("subtech_P" + str(participant) + "_" + intensity + ".csv", sep =";")
        
        res_left = np.sqrt(acc["P" + str(participant)][intensity]["Prop Tracker 3 x"]**2 + 
                       acc["P" + str(participant)][intensity]["Prop Tracker 3 y"]**2 + 
                       acc["P" + str(participant)][intensity]["Prop Tracker 3 z"]**2)

        b,a= signal.butter(4, 10/(fs/2), 'Lowpass') # filter at 10/0
        resultant_left = signal.filtfilt(b,a, res_left) # left pole

      #  plt.figure()
       # plt.plot(resultant_left)
        
        for technique in sub_techniques:
            tech_where = frame.index[frame['sub-technique'] == technique].tolist()
            
            
            if tech_where:
                
                for interval in tech_where:
                    start = frame["last frame"][interval-1].astype(int)
                    end = frame["last frame"][interval].astype(int)
                    
                    #left side
                    shoulder_left = erg_ja["P" + str(participant)][intensity]["T8_LeftUpperArm Flexion/Extension"]
                    peaks, _ = find_peaks(shoulder_left[start:end], height = 0, distance = dist_part[counter]) # at least 40° and 50 samples apart
                    peaks_sh = list(peaks + start)
                    
                    acc_peaks_left = np.array([])
                    for peak in peaks_sh:
                        
                        if peak-wind_part[counter] >0:
                            low_bound = peak-wind_part[counter]
                        else:
                            low_bound = 0
                            
                        if peak+wind_part[counter] < len(shoulder_left)-1:
                            up_bound = peak+wind_part[counter]
                        else:
                            low_bound = len(shoulder_left)-1
                        
                        ##finire questa parte
                        a = resultant_left[low_bound: up_bound]
                        peaks_window = find_peaks(resultant_left[low_bound: up_bound])
                        peaks_where = list([peaks_window][0][0])
                        max_ind = peaks_where[np.argmax(resultant_left[low_bound: up_bound][peaks_where])]
                        acc_peaks_left = np.append(acc_peaks_left, max_ind + low_bound)
                    
                        
                        
                        
                    
                    acc_peaks_left = acc_peaks_left.astype(int)
                    
                    
                    
                    plt.plot(np.arange(start,end), resultant_left[start: end], label = technique)
                    plt.plot(np.arange(start,end), shoulder_left[start: end], c = "black")
                    plt.plot(acc_peaks_left, resultant_left[acc_peaks_left], "v", color="red")
                    del start, end
                #plt.legend()
                    
                    if len(acc_peaks_left) != 0:            
                       intervd[interval]= acc_peaks_left 
                    acc_peaks_left = np.array([])
                    
                    
            if intervd:            
               techd[technique]= intervd.copy()
            intervd.clear()
            
        if techd:            
           intensd[intensity]= techd.copy()
        techd.clear()
    
    if intensd:            
       partd["P"+ str(participant)]= intensd.copy()
    intensd.clear()
                    
                    
import pickle
f = open("ski_cycles.pkl","wb")
pickle.dump(partd,f)
f.close()
