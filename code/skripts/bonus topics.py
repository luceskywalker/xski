from IPython import get_ipython
#get_ipython().magic("reset -sf")

from mpl_toolkits.mplot3d.art3d import Line3DCollection
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os 

os.chdir(r'C:/Users/Matteo/Downloads/salzburg/projects/movella challenge/xsens_case-study-kit_2023-03-07_1502/Case Study Kit/Recordings/GPS RTK data')
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


znew = np.array([])

# moving avg for height

znew = np.append(znew, np.mean(z[0:3]))
znew = np.append(znew, np.mean(z[0:4]))

for i in range(2, len(z)-2):
    znew = np.append(znew, np.mean(z[i-2:i+3]))
    
znew = np.append(znew, np.mean(z[i-2:i+2]))  
znew = np.append(znew, np.mean(z[i-2:i+1]))   
z = znew

"""
df = pd.DataFrame({"x": x, "y": y,"z": z, "mu": mu_mixed})

#threshold_high = np.percentile(df["mu"].to_numpy(), 100)
#threshold_low = np.percentile(df["mu"].to_numpy(), 2.5)
#df = df[(df["mu"]< threshold_high)]

x=df["x"].to_numpy()
y=df["y"].to_numpy()
z=df["z"].to_numpy()
mu_mixed =df["mu"].to_numpy()
"""
###################### altern vel ########################################################
plt.close("all")  
points = np.array([x,y,z]).transpose().reshape(-1,1,3)
segs = np.concatenate([points[:-1],points[1:]],axis=1)
 
lc = Line3DCollection(segs, cmap=plt.get_cmap('jet'))
lc.set_array(mu_mixed) # color the segments by our parameter
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
line = ax.add_collection3d(lc)
cmap = fig.colorbar(line, ax=ax)
cmap.set_label(label='snow friction',size=15, labelpad=0)

ax.set_xlim(x.min(), x.max())
ax.set_ylim(y.min(), y.max())
ax.set_zlim(z.min(), z.max())

plt.show()
#fig.gca().set_title("Snow friction along skied trajectory, P13", fontsize = 30)  
fig.gca().set_xlabel("X Displacement", fontsize = 17, labelpad=7)
fig.gca().set_ylabel("Y displacement", fontsize = 17, labelpad=7)
fig.gca().set_zlabel("Elevation gain [m]", fontsize = 17)
       
  
    
  
    
    
