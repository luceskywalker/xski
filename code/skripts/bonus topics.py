from IPython import get_ipython
get_ipython().magic("reset -sf")

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os 

os.chdir('C:/Users/Matteo/Downloads/salzburg/projects/movella challenge/xsens_case-study-kit_2023-03-07_1502/Case Study Kit/Recordings/GPS RTK data')
plt.close('all')

subject = 13
file = "P"+ str(subject) + "_coord.xlsx"
df = pd.read_excel(file)
################################################################# snow friction ###########################################################

df.loc[:, 'VelocityN':'GroundSpeed'] = df.loc[:, 'VelocityN':'GroundSpeed']/1000
g = 9.81 # (m/s^2)
cor_fact= 0.01
alpha_ice = 0.93 * 10**-6 #m^2/s
lambda_ice = 1.8 # W/(m*K)
film_thick = 10**-6 # assume film thickness 1 micrometer


if subject ==3:
    
    mu_dry = 0.215 # adimensional
    weight = 64 #kg
    fn = weight/2*g # force on each ski
    ski_length = 1.9 #m
    ski_width = 0.045#m
    ski_area = ski_length*ski_width #m2
    tsnow = -17 # Celsius deg
else:
    
    mu_dry = 0.21
    weight = 44
    fn = weight/2*g # force on each ski
    ski_length = 1.58
    ski_width = 0.048
    ski_area = ski_length*ski_width
    tsnow = -20 # Celsius deg
    

delta_t = 0- tsnow
    
vel = df["GroundSpeed"].to_numpy()
length_dry = (np.pi/(alpha_ice*vel)) * ((lambda_ice*ski_area*cor_fact* delta_t) / (2*mu_dry*fn))**2
length_dry[length_dry > ski_length] = ski_length


eta = (1.79- 0.054*tsnow) /1000 # from mPa to Pa
wet_length = ski_length-length_dry
wet_area = wet_length*ski_width

wet_force = (eta * wet_area*cor_fact * vel)/film_thick
dry_force = mu_dry * fn *(length_dry/ski_length)

mu_mixed = (wet_force + dry_force)/fn
    
    
    
############################################# 3d track ##############################################################    
x = df.iloc[:,-2].to_numpy()
y = df.iloc[:,-1].to_numpy()
z = ((df["Height"]- df["Height"][0])/1000).to_numpy()

###################### altern vel ########################################################
x = np.cumsum((df["VelocityN"]*0.25).to_numpy())
y = np.cumsum((df["VelocityE"]*0.25).to_numpy())
z = np.cumsum((df["VelocityD"]*0.25).to_numpy())



plt.figure()
ax = plt.axes(projection='3d')  
ax.plot3D(x, y, z)
    
    
    
    
    
    
    
    
    

