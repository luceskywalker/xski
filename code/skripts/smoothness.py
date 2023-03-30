from IPython import get_ipython
get_ipython().magic("reset -sf")

import numpy as np
import pandas as pd
import os
import pickle
from scipy import signal
import seaborn as sns
import matplotlib.pyplot as plt



os.chdir("C:/Users/Matteo/Downloads/salzburg/projects/movella challenge/xski/code/skripts")

file= open("C:/Users/Matteo/Downloads/salzburg/projects/movella challenge/file esportati/linear_position.pkl", "rb")
segment_data= pickle.load(file)
file.close()

file= open("C:/Users/Matteo/Downloads/salzburg/projects/movella challenge/file esportati/com_data.pkl", "rb")
com_data= pickle.load(file)
file.close()

file= open("C:/Users/Matteo/Downloads/salzburg/projects/movella challenge/xski/files/ski_cycles.pkl", "rb")
ski_cycles = pickle.load(file)
file.close()
del file

name_segment = "CoM acc"
fs = 240
fcut = 8

df = pd.DataFrame(columns=['subject', 'intensity', 'technique', "direction", "NJ"])


for participant in ski_cycles.keys():
    for intensity in ["easy", "medium", "hard"]:
        
        data_x = com_data[participant][intensity][name_segment + " x"]
        data_y = com_data[participant][intensity][name_segment + " y"]
        data_z = com_data[participant][intensity][name_segment + " z"]
        
        pos_x = com_data[participant][intensity]["CoM pos x"]
        pos_y = com_data[participant][intensity]["CoM pos y"]
        pos_z = com_data[participant][intensity]["CoM pos z"]
        
        
        data_h = np.sqrt(data_x**2 + data_y**2) # horiyontal data
        b,a= signal.butter(4, fcut /(fs/2), 'Lowpass') # filter at 7 Hz
        
        pos_x = signal.filtfilt(b,a, pos_x)
        pos_y = signal.filtfilt(b,a, pos_x) 
        pos_z = signal.filtfilt(b,a, pos_z)
        
        data_x = signal.filtfilt(b,a, data_x)
        data_y = signal.filtfilt(b,a, data_x) 
        data_z = signal.filtfilt(b,a, data_z) 
        
        for technique in ski_cycles[participant][intensity].keys():
            for interval in ski_cycles[participant][intensity][technique].keys():
                pole_plants = ski_cycles[participant][intensity][technique][interval]
                
                for i in range(0, len(pole_plants)-1):
                    start = pole_plants[i]
                    end = pole_plants[i+1]+1 # one more point cause when differentiating I eliminate one
                    
                    
                    
                    jerk_x = np.diff(data_x[start:end])*fs
                    jerk_y = np.diff(data_y[start:end])*fs
                    jerk_z = np.diff(data_z[start:end])*fs
                    
                    length_x = max(pos_x[start:end]) - min(pos_x[start:end])
                    length_y = max(pos_y[start:end]) - min(pos_y[start:end]) 
                    length_z = max(pos_z[start:end]) - min(pos_z[start:end]) 
                    
                    dur = (end-start)/fs
                    corr_fact_x = dur**5/length_x**2
                    corr_fact_y = dur**5/length_y**2
                    corr_fact_z = dur**5/length_z**2
                    
                    norm_jerk_x = np.sqrt((0.5*np.sum(jerk_x**2)*corr_fact_x))
                    norm_jerk_y = np.sqrt((0.5*np.sum(jerk_y**2)*corr_fact_y))
                    norm_jerk_z = np.sqrt((0.5*np.sum(jerk_z**2)*corr_fact_z))
                    
                    norm_jerk_h = (norm_jerk_x**2 + norm_jerk_y**2)**0.5
                    
                    row =[participant, intensity, technique, "horizontal", norm_jerk_h]
                    df.loc[len(df)] = row
                    row =[participant, intensity, technique, "vertical", norm_jerk_z]
                    df.loc[len(df)] = row
                    
                    



    
    
    
dfh = df[df["direction"] == "horizontal"].reset_index(drop = True)
dfv = df[df["direction"] == "vertical"].reset_index(drop = True)

threshold_high = np.percentile(dfh["NJ"].to_numpy(), 97.5)
threshold_low = np.percentile(dfh["NJ"].to_numpy(), 2.5)
dfh = dfh[(dfh["NJ"]> threshold_low) & (dfh["NJ"]< threshold_high)]

threshold_high = np.percentile(dfv["NJ"].to_numpy(), 97.5)
threshold_low = np.percentile(dfv["NJ"].to_numpy(), 2.5)
dfv = dfv[(dfv["NJ"]> threshold_low) & (dfv["NJ"]< threshold_high)]

df = pd.concat([dfh, dfv])






tech = "dp"

plt.figure()           
ax = sns.barplot(data = df[(df["technique"] == tech)], 
            x = "direction", y = "NJ", hue = "subject",
            hue_order = ["P3", "P5","P6","P7","P8","P12","P13", "P14"])
  
plt.setp(ax.get_legend().get_texts(), fontsize='15') # for legend text
leg = plt.legend(ncol=8, loc="upper left", fontsize = 18.5, bbox_to_anchor=(0.1, 1))
plt.title("CoM movement smoothness", fontsize = 40)
plt.xlabel("Motion direction", fontsize = 35)
plt.ylabel("Normalized jerk", fontsize = 35)
plt.xticks(fontsize = 20)
plt.yticks(fontsize = 20)
for line in leg.get_lines():
    line.set_linewidth(3.0)








