from IPython import get_ipython
get_ipython().magic("reset -sf")

import numpy as np
import os
import pickle

os.chdir("C:/Users/Matteo/Downloads/salzburg/projects/movella challenge/file esportati")

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

partd = dict()
intensd = dict()
segmentd = dict()
sided = dict()


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
                    
                    sided[side] = tot_energy_segment*fs/subjects_data["weight"][counter] # power normalized to bw [W/kg]
                    del tot_energy_segment
                    
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
                    
                sided["Right"] = tot_energy_segment*fs/subjects_data["weight"][counter] # power normalized to bw [W/kg]
                del tot_energy_segment
                
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
                        
                        sided[side] = tot_energy_segment*fs/poles_weight # power normalized to bw [W/kg]
                        del tot_energy_segment
                        
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
                        
                        sided[side] = tot_energy_segment*fs/ski_weight # power normalized to bw [W/kg]
                        del tot_energy_segment
                        
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
           
        total_power = lower_sum + upper_sum
        ratio = upper_sum/lower_sum
        intd[intensity] = {"total power": total_power, "power ratio": ratio, "upper body": upper_sum, "lower body": lower_sum}
        lower_sum = 0
        upper_sum = 0
        del total_power, ratio
    
    if intd:
        subjectd[participant] = intd.copy()
    intd.clear
          

            
        
        
        




