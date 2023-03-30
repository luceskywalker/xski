from IPython import get_ipython
get_ipython().magic("reset -sf")

import numpy as np
import os
import pickle
from scipy import signal
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

os.chdir("E:/movella challenge/file esportati")

file = open("linear_velocity.pkl", "rb")
lin_vel = pickle.load(file)
file.close()

file =open("angular_velocity.pkl", "rb")
ang_vel = pickle.load(file)
file.close()

file = open("linear_position.pkl", "rb")
lin_pos = pickle.load(file)
file.close()
del file

subjects_data = {"weight": [64, 50, 84, 68, 68, 100, 44, 46], "height": [1.75, 1.64, 2, 1.72, 1.71, 1.83, 1.65, 1.51],
                 "ski length" : [2.05, 1.83, 2.07, 1.95, 1.97, 1.94, 1.73, 1.67], 
                 "ski width": [0.045, 0.046, 0.044, 0.05, 0.045, 0.047, 0.047, 0.048],
                 "pole length": [1.33, 1.47, 1.72, 1.45, 1.43, 1.62, 1.36, 1.47], 
                 "ski cor": [0.945, 0.87, 0.94, 0.92, 0.92, 0.92, 0.82, 0.785]}


ski_thick = 0.01
length= {"foot": 0.152, "shank": 0.246, "thigh": 0.245, "forearm": 0.146, "arm": 0.186, "trunk": 0.47}
weight= {"foot": 1.43/100, "shank": 4.61/100, "thigh": 10.01/100, "forearm": 2.14/100, "arm": 2.64/100, "trunk": 56.34/100}
sensor_names = ["Foot", "Lower Leg", "Upper Leg", "Forearm", "Upper Arm", "T8"]

equipment =["Right pole", "Left pole", "Right ski", "Left ski"]
equipment_sensors = ["Prop Tracker 4", "Prop Tracker 3", "Prop Tracker 2", "Prop Tracker 1"]
segment_names =["foot", "shank", "thigh", "arm", "forearm", "trunk", "pole", "ski"]


segments_proportions = {"length":length, "weight": weight}
ski_weight = 0.625 # kg , per piece
poles_weight = 0.1 #kg, per piece
density = 1000 # kg/m3
poles_r = 0.01 #m
g = 9.81
fs = 240
fcut = 8

partd = dict()
intensd = dict()
segmentd = dict()
sided = dict()


b,a= signal.butter(4, fcut /(fs/2), 'Lowpass') 


counter = -1
for participant in lin_vel.keys():
    counter +=1
    
    for intensity in ["easy", "medium", "hard"]:
        trial_lin_vel =lin_vel[participant][intensity]
        trial_ang_vel =ang_vel[participant][intensity]
        trial_lin_pos =lin_pos[participant][intensity]
        
        
        counter2 = -1 # for sensors
        for segment in segment_names:
            counter2 +=1
            
            if ((segment != "pole") & (segment != "ski")):
                segment_weight = segments_proportions["weight"][segment]*subjects_data["weight"][counter]
                segment_length = segments_proportions["length"][segment]*subjects_data["height"][counter]
                r_segment = np.sqrt((segment_weight/density)/(np.pi*segment_length))
                
            
            if (segment =="foot") or (segment =="shank") or(segment =="thigh") or(segment =="trunk"):
                Ix =Iy= ((segment_weight*r_segment**2)/4) + ((segment_weight*segment_length**2)/3)  
                Iz = 0.5*segment_weight*r_segment**2
            elif (segment =="arm") or (segment =="forearm"):
                Ix =Iz = ((segment_weight*r_segment**2)/4) + ((segment_weight*segment_length**2)/3)  
                Iy = 0.5*segment_weight*r_segment**2
            
            
            if (segment != "trunk") & (segment != "ski") & (segment != "pole") :
                
                for side in ["Right", "Left"]:
                    
                    v_x = trial_lin_vel[side + " " + sensor_names[counter2] + " x"]
                    v_y = trial_lin_vel[side + " " + sensor_names[counter2] + " y"]
                    v_z = trial_lin_vel[side + " " + sensor_names[counter2] + " z"]
                    omega_x = trial_ang_vel[side + " " + sensor_names[counter2] + " x"]
                    omega_y = trial_ang_vel[side + " " + sensor_names[counter2] + " y"]
                    omega_z = trial_ang_vel[side + " " + sensor_names[counter2] + " z"]
                    h = trial_lin_pos[side + " " + sensor_names[counter2] + " z"]
                    
                    
                    
                    
                    
                    kinetic_trans =0.5*segment_weight*(v_x**2 + v_y**2 + v_z**2)
                    kinetic_rot = 0.5*(Ix*omega_x**2 + Iy*omega_y**2 + Iz*omega_z**2)
                    pot = segment_weight*g*h
                    tot_energy_segment = kinetic_trans + kinetic_rot + pot
                    
                    power = np.diff(tot_energy_segment)*fs/subjects_data["weight"][counter]# power normalized to bw [W/kg]
                    power = signal.filtfilt(b,a,power)
                    sided[side] = power 
                    del power
                    
                if sided:
                    segmentd[segment] = sided.copy()
                sided.clear()
                    
            elif segment =="trunk": #if line 83
                
                v_x = trial_lin_vel["T8 x"]
                v_y = trial_lin_vel["T8 y"]
                v_z = trial_lin_vel["T8 z"]
                omega_x = trial_ang_vel["T8 x"]
                omega_y = trial_ang_vel["T8 y"]
                omega_z = trial_ang_vel["T8 z"]
                h = trial_lin_pos["T8 z"]
                    
                kinetic_trans =0.5*segment_weight*(v_x**2 + v_y**2 + v_z**2)
                kinetic_rot = 0.5*(Ix*omega_x**2 + Iy*omega_y**2 + Iz*omega_z**2)
                pot = segment_weight*g*h
                tot_energy_segment = kinetic_trans + kinetic_rot + pot
                power = np.diff(tot_energy_segment)*fs/subjects_data["weight"][counter]# power normalized to bw [W/kg]
                power = signal.filtfilt(b,a,power)
                sided["Right"] = power
                
                del power
                
                if sided:
                    segmentd[segment] = sided.copy()
                sided.clear()
                
            else: #if line 83
                
                if segment == "pole":
                    for side in ["Right", "Left"]:
                        Ix =Iy= ((poles_weight*poles_r**2)/4) + ((poles_weight*subjects_data["pole length"][counter]**2)/3)  
                        Iz = 0.5*poles_weight*poles_r**2
                        if side == "Right":
                            sensor = "Prop Tracker 4"
                        else:
                            sensor = "Prop Tracker 3"
                            
                        v_x = trial_lin_vel[sensor + " x"]
                        v_y = trial_lin_vel[sensor + " y"]
                        v_z = trial_lin_vel[sensor + " z"]
                        omega_x = trial_ang_vel[sensor + " x"]
                        omega_y = trial_ang_vel[sensor + " y"]
                        omega_z = trial_ang_vel[sensor + " z"]
                        h = trial_lin_pos[sensor + " z"]
                        
                        kinetic_trans =0.5*poles_weight*(v_x**2 + v_y**2 + v_z**2)
                        kinetic_rot = 0.5*(Ix*omega_x**2 + Iy*omega_y**2 + Iz*omega_z**2)
                        pot = poles_weight*g*h
                        tot_energy_segment = kinetic_trans + kinetic_rot + pot
                        power = np.diff(tot_energy_segment)*fs/subjects_data["weight"][counter]# power normalized to bw [W/kg]
                        power = signal.filtfilt(b,a,power)
                        
                        sided[side] = power
                        del power
                        
                    if sided:
                        segmentd[segment] = sided.copy()
                    sided.clear()
                
                elif segment == "ski":
                        
                    offset = subjects_data["ski length"][counter]/2- subjects_data["ski cor"][counter]
                     
                    Ix= 1/12**ski_weight*(subjects_data["ski length"][counter]**2 
                                          + ski_thick**2) + ski_weight*offset**2 
                    
                    Iy= 1/12**ski_weight*(subjects_data["ski width"][counter]**2 + 
                                          subjects_data["ski length"][counter]**2) + ski_weight*offset**2   
                    
                    Iz = 1/12**ski_weight*(subjects_data["ski width"][counter]**2 + ski_thick**2)
                
                    for side in ["Right", "Left"]:
                        if side == "Right":
                            sensor = "Prop Tracker 2"
                        else:
                            sensor = "Prop Tracker 1"
                            
                        v_x = trial_lin_vel[sensor + " x"]
                        v_y = trial_lin_vel[sensor + " y"]
                        v_z = trial_lin_vel[sensor + " z"]
                        omega_x = trial_ang_vel[sensor + " x"]
                        omega_y = trial_ang_vel[sensor + " y"]
                        omega_z = trial_ang_vel[sensor + " z"]
                        h = trial_lin_pos[sensor + " z"]
                        
                        kinetic_trans =0.5*ski_weight*(v_x**2 + v_y**2 + v_z**2)
                        kinetic_rot = 0.5*(Ix*omega_x**2 + Iy*omega_y**2 + Iz*omega_z**2)
                        pot = ski_weight*g*h
                        tot_energy_segment = kinetic_trans + kinetic_rot + pot
                        
                        power = np.diff(tot_energy_segment)*fs/subjects_data["weight"][counter]# power normalized to bw [W/kg]
                        
                        power = signal.filtfilt(b,a,power)
                        sided[side] = power
                        del power
                        
                    if sided:
                        segmentd[segment] = sided.copy()
                    sided.clear()
                         
         
        if segmentd:
            intensd[intensity] = segmentd.copy()
        segmentd.clear()
        
    if intensd:
        partd[participant] = intensd.copy()
    intensd.clear()
                
####################################################################################### 
upper_segments = ["arm", "forearm", "trunk", "pole"] 
lower_segments = ["foot", "shank", "thigh","ski"]             

lower_sum = 0
upper_sum = 0



intd= dict()
subjectd = dict()            
for participant in partd.keys():
    intensd = partd[participant]
    
    for intensity in ["easy", "medium", "hard"]:
        data_trial = intensd[intensity] 
        
        for segment in segment_names:
            
            if segment in upper_segments:
                
                for side in data_trial[segment].keys():
                    upper_sum = upper_sum + data_trial[segment][side]
            else:
                
                for side in data_trial[segment].keys():
                    lower_sum = lower_sum + data_trial[segment][side]
           
        intd[intensity] = {"upper body": upper_sum, "lower body": lower_sum}
        lower_sum = 0
        upper_sum = 0
        
    
    if intd:
        subjectd[participant] = intd.copy()
    intd.clear
          
########################################### di df and pics #################################################################    
file = open("C:/Users/Matteo/Downloads/salzburg/projects/movella challenge/xski/files/ski_cycles.pkl", "rb")
ski_cycles = pickle.load(file)
file.close() 
            
        
df = pd.DataFrame(columns=['subject', 'intensity', 'technique', "quantity", "cycle", "parcentile", "power"])

from scipy import signal
partlist = []    
intlist = []
techlist = []
perclist = []
powlist =[]  
cyclelist =[]
quantlist = []

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
                    
                    for quantity in ["lower body", "upper body"]:
                        
                        power_cycle = subjectd[participant][intensity][quantity][start:end]
                        power_cycle = signal.resample_poly(power_cycle, 100, len(power_cycle), padtype="line")
                        
                        partlist = partlist + [participant]*100 
                        intlist = intlist + [intensity]*100 
                        techlist = techlist + [technique]*100
                        quantlist = quantlist + [quantity]*100
                        cyclelist = cyclelist + [plant]*100
                        perclist = perclist + list(np.arange(1,101))
                        powlist = powlist + list(power_cycle)
                        
    
df = pd.DataFrame()
df["subject"] = partlist
df["intensity"] = intlist
df["technique"] = techlist
df["cycle"] = cyclelist
df["percentile"] = perclist                
df["power"] = powlist               
df["quantity"] = quantlist  


quant= "upper body"

dfq = df[df["quantity"] == quant].reset_index(drop =True)   
dfq = dfq.groupby(["subject", "intensity", "technique", "percentile"], as_index = False)["power"].mean() 
dfq_dp =dfq[dfq["technique"] == "dp"]
  
intens = "hard"
dfq_dp =dfq_dp[dfq_dp["intensity"] == intens]

partord = ["P3", "P5", "P6", "P7", "P8", "P12", "P13", "P14"]

plt.figure()
ax = sns.lineplot(x = "percentile", y = "power", hue = "subject", data = dfq_dp, hue_order = partord, linewidth = 3)
plt.setp(ax.get_legend().get_texts(), fontsize='15') # for legend text
leg = plt.legend(ncol=8, loc="upper left", fontsize = 18.5, bbox_to_anchor=(0, 1))
plt.title("Power output in " + quant)
plt.xlabel("Ski cycle [%]", fontsize = 35)
plt.ylabel("Power [W/kg]", fontsize = 35)
for line in leg.get_lines():
    line.set_linewidth(3.0)
    

dfu = df[df["quantity"] == "upper body"].reset_index(drop =True)   
dfl = df[df["quantity"] == "lower body"].reset_index(drop =True)   

dfu = dfu.groupby(["subject", "intensity", "technique", "percentile"], as_index = False)["power"].mean() 
dfl = dfl.groupby(["subject", "intensity", "technique", "percentile"], as_index = False)["power"].mean() 

dfu["ratio"] = abs(dfu["power"]) / (abs(dfu["power"]) + abs(dfl["power"]))*100
dfu_dp =dfu[(dfu["technique"] == "dp") & (dfu["intensity"] == "hard")]
 





plt.figure()
ax = sns.lineplot(x = "percentile", y = "ratio", hue = "subject", data = dfu_dp, hue_order = partord, linewidth = 3)
plt.setp(ax.get_legend().get_texts(), fontsize='15') # for legend text
leg = plt.legend(ncol=8, loc="upper left", fontsize = 18.5, bbox_to_anchor=(0, 0.1))
plt.title("Upper body contribution as percentage of full body power", fontsize = 40)
plt.xlabel("Ski cycle [%]", fontsize = 35)
plt.ylabel("Percentage [%]", fontsize = 35)
plt.xticks(fontsize = 25)
plt.yticks(fontsize = 25)
for line in leg.get_lines():
    line.set_linewidth(3.0)












