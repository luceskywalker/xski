from IPython import get_ipython
get_ipython().magic("reset -sf")

import numpy as np
import pandas as pd
import os
import pickle
from scipy import signal


os.chdir("C:/Users/Matteo/Downloads/salzburg/projects/movella challenge/file esportati")

file = open("com_position.pkl", "rb")
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
        
        for side in ["Right", "Left"]:
            foot_x = lin_pos[participant][intensity][side + " Foot x"]
            foot_y = lin_pos[participant][intensity][side + " Foot y"]
            
            delta_x = foot_x - com_x
            delta_y = foot_y - com_y
            delta = np.sqrt(delta_x**2 + delta_y**2)
            
            b,a= signal.butter(4, 10/(fs/2), 'Lowpass') # filter at 10 Hz
            delta = signal.filtfilt(b,a, delta) 
            delta =delta/height[counter]*100
            
            sided[side]= delta
            del delta
         
        if sided:    
            intd[intensity]= sided.copy()
        sided.clear()
        
    if intd:
        partd[participant] = intd.copy()
    intd.clear()
    
    
            

        
        














