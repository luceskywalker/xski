from IPython import get_ipython
get_ipython().magic("reset -sf")

import numpy as np
import pandas as pd
import os
import pickle
from scipy import signal


os.chdir("C:/Users/Matteo/Downloads/salzburg/projects/movella challenge/file esportati")

file = open("com_data.pkl", "rb")
com_data = pickle.load(file)
file.close()

file =open("linear_position.pkl", "rb")
lin_pos = pickle.load(file)
file.close()
del file
fs = 240
height = [1.75, 1.64, 2, 1.72, 1.71, 1.83, 1.65, 1.51]

sided = dict()
intd = dict()
partd = dict()

counter = -1
for participant in lin_pos.keys():
    counter += 1
    for intensity in ["easy", "medium", "hard"]:
        com_x= com_data[participant][intensity]["CoM pos x"]
        com_y= com_data[participant][intensity]["CoM pos y"]
        
        
        right_foot_x = lin_pos[participant][intensity]["Right Foot x"]
        right_foot_y = lin_pos[participant][intensity]["Right Foot y"]
        left_foot_x = lin_pos[participant][intensity]["Left Foot x"]
        left_foot_y = lin_pos[participant][intensity]["Left Foot y"]
        
        foot_mean_x = np.mean([right_foot_x, left_foot_x], axis = 0)
        foot_mean_y = np.mean([right_foot_y, left_foot_y], axis = 0)
        
        
        delta_x = foot_mean_x - com_x
        delta_y = foot_mean_y - com_y
        delta = np.sqrt(delta_x**2 + delta_y**2)
        
        b,a= signal.butter(4, 10/(fs/2), 'Lowpass') # filter at 10 Hz
        delta = signal.filtfilt(b,a, delta) 
        delta =delta/height[counter]*100
        
        if len(delta)>0:    
            intd[intensity]= delta
        del delta
        
    if intd:
        partd[participant] = intd.copy()
    intd.clear()
    

file = open("C:/Users/Matteo/Downloads/salzburg/projects/movella challenge/xski/files/ski_cycles.pkl", "rb")
ski_cycles = pickle.load(file)
file.close()  
  
df = pd.DataFrame(columns=['subject', 'intensity', 'technique', "parcentile", "sway"])

from scipy import signal
partlist = []    
intlist = []
techlist = []
perclist = []
swaylist =[]  
cyclelist =[]

plant = 0
for participant in ski_cycles.keys():
    for intensity in ["easy", "medium", "hard"]:
        for technique in ski_cycles[participant][intensity].keys():
            for interval in ski_cycles[participant][intensity][technique]:
                
                cycles = ski_cycles[participant][intensity][technique][interval]
                
                for i in range(0, len(cycles)-1):
                    start = cycles[i]
                    end = cycles[i+1]
                    plant +=1
                    
                    balance_cycle = partd[participant][intensity][start:end]
                    
                    balance_cycle = signal.resample_poly(balance_cycle, 100, len(balance_cycle), padtype="line")
                    
                    partlist = partlist + [participant]*100 
                    intlist = intlist + [intensity]*100 
                    techlist = techlist + [technique]*100
                    cyclelist = cyclelist + [plant]*100
                    perclist = perclist + list(np.arange(1,101))
                    swaylist = swaylist + list(balance_cycle)
                    
    
df = pd.DataFrame()
df["subject"] = partlist
df["intensity"] = intlist
df["technique"] = techlist
df["cycle"] = cyclelist
df["percentile"] = perclist                
df["sway"] = swaylist       


dfmean = df.groupby(["subject", "intensity", "technique", "percentile"], as_index = False)["sway"].mean() 
    


dfmean = dfmean[dfmean["intensity"] =="hard"].reset_index(drop = True)


import seaborn as sns 
import matplotlib.pyplot as plt

tech = "dp"  
plt.figure()           
ax = sns.lineplot(data = dfmean[(dfmean["technique"] == tech)], 
            x = "percentile", y = "sway", hue = "subject" , 
            hue_order = ["P3", "P5","P6","P7","P8","P12","P13", "P14"], linewidth = 3)

plt.setp(ax.get_legend().get_texts(), fontsize='15') # for legend text
leg = plt.legend(ncol=8, loc="upper left", fontsize = 18.5, bbox_to_anchor=(0, 1))
plt.title("Horizontal sway CoM- feet in double poling", fontsize = 40)
plt.xlabel("Ski cycle [%]", fontsize = 35)
plt.ylabel("Sway [% body height]", fontsize = 35)
plt.xticks(fontsize = 20)
plt.yticks(fontsize = 20)
ax.set_ylim([0, 16])
for line in leg.get_lines():
    line.set_linewidth(3.0)











