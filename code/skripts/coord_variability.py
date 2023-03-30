from IPython import get_ipython
get_ipython().magic("reset -sf")

import matplotlib.pyplot as plt
import numpy as np
import os 
import pickle
from scipy import signal
from numpy.linalg import eig
from angvelboxfe import angvelfe
import pandas as pd
os.chdir('C:/Users/Matteo/Downloads/salzburg/projects/movella challenge/file esportati')# -*- coding: utf-8 -*-
"""
file = open("joint_angles.pkl", "rb")
ja = pickle.load(file)
file.close()

file = open("C:/Users/Matteo/Downloads/salzburg/projects/movella challenge/xski/files/ski_cycles.pkl", "rb")
ski_cycles = pickle.load(file)
file.close()

file = open("erg_joint_angles.pkl", "rb")
erg_ja = pickle.load(file)
file.close()
del file

couplings = ["k_r / h_r", "k_l / h_l", "h_r / s_r", "h_l / s_l", "t_b / sh_r", "t_b / sh_l"]
ki = 2.4478 # Milleaux 2017 p 3/7
fs = 240
couplingd = dict()
techd = dict()
intd = dict()
partd = dict()
########################## resampling ######################################################

for participant in ski_cycles.keys():
    for intensity in ski_cycles[participant].keys():
        
        jointd = dict()
        
        xfe = ja[participant][intensity]["Right Knee Flexion/Extension"]
        xaa = ja[participant][intensity]["Right Knee Abduction/Adduction"]
        xie = ja[participant][intensity]["Right Knee Internal/External Rotation"]
        jointd["k_r"] =angvelfe(xfe, xaa, xie, fs)
        
        xfe = ja[participant][intensity]["Left Knee Flexion/Extension"]
        xaa = ja[participant][intensity]["Left Knee Abduction/Adduction"]
        xie = ja[participant][intensity]["Left Knee Internal/External Rotation"]
        jointd["k_l"] =angvelfe(xfe, xaa, xie, fs)
        
        xfe = ja[participant][intensity]["Right Hip Flexion/Extension"]
        xaa = ja[participant][intensity]["Right Hip Abduction/Adduction"]
        xie = ja[participant][intensity]["Right Hip Internal/External Rotation"]
        jointd["h_r"] =angvelfe(xfe, xaa, xie, fs)
        
        xfe = ja[participant][intensity]["Left Hip Flexion/Extension"]
        xaa = ja[participant][intensity]["Left Hip Abduction/Adduction"]
        xie = ja[participant][intensity]["Left Hip Internal/External Rotation"]
        jointd["h_l"] =angvelfe(xfe, xaa, xie, fs)
        
        xfe = erg_ja[participant][intensity]["Pelvis_T8 Flexion/Extension"]
        xaa = erg_ja[participant][intensity]["Pelvis_T8 Lateral Bending"]
        xie = erg_ja[participant][intensity]["Pelvis_T8 Axial Bending"]
        jointd["t_b"] =angvelfe(xfe, xaa, xie, fs)
        
        xfe = erg_ja[participant][intensity]["T8_LeftUpperArm Flexion/Extension"]
        xaa = erg_ja[participant][intensity]["T8_LeftUpperArm Lateral Bending"]
        xie = erg_ja[participant][intensity]["T8_LeftUpperArm Axial Bending"]
        jointd["s_l"] =angvelfe(xfe, xaa, xie, fs)
        
        xfe = erg_ja[participant][intensity]["T8_RightUpperArm Flexion/Extension"]
        xaa = erg_ja[participant][intensity]["T8_RightUpperArm Lateral Bending"]
        xie = erg_ja[participant][intensity]["T8_RightUpperArm Axial Bending"]
        jointd["s_r"] =angvelfe(xfe, xaa, xie, fs)
        
        for technique in ski_cycles[participant][intensity].keys():
            
            jointd_res =dict()
            
            for angle in jointd.keys():
                ang_to_res = jointd[angle]
                angle_res = np.array([])
                for interval in ski_cycles[participant][intensity][technique].keys():
                    cycles = ski_cycles[participant][intensity][technique][interval]
                    for i in range(0, len(cycles)-1):
                        start = cycles[i]
                        end = cycles[i+1]
                        
                        ang_cycle = ang_to_res[start:end]
                        ang_cycle = signal.resample_poly(ang_cycle, 100, len(ang_cycle), padtype="line")
                        angle_res = np.append(angle_res, ang_cycle)
                        
                jointd_res[angle] = angle_res
            
            for coupling in couplings:
                joint1 = jointd_res[coupling[0:3]]
                joint2 = jointd_res[coupling[-3:]]
                
                areacycle = np.array([])
                for i in range(0, 100):  # qui parto a calcolare ellisse x  % gait cycle
                    delta1 = joint1[i + np.arange(0, len(joint1), 100)]
                    delta2 = joint2[i + np.arange(0, len(joint2), 100)]
                    #delta1, delta2 = remoutlier(delta1, delta2)
                    
                    covmat = np.cov(delta1,delta2)
                    val, vec = eig(covmat)
                    ellaxes = ki*np.sqrt(val)
                    areacycle = np.append(areacycle, np.prod(ellaxes)*np.pi)
                    
                if len(areacycle) > 0:
                    couplingd[coupling] = areacycle
             
            if couplingd:
                techd[technique] = couplingd.copy()
            couplingd.clear()
            
        if techd:
            intd[intensity] = techd.copy()
        techd.clear()
        
    if intd:
        partd[participant] = intd.copy()
    intd.clear()
                    

f = open("C:/Users/Matteo/Downloads/salzburg/projects/movella challenge/file esportati/ellipse_area.pkl","wb")
pickle.dump(partd,f)
f.close()
 """                  
file = open("ellipse_area.pkl", "rb")
partd = pickle.load(file)
file.close()   
del file
                 
df = pd.DataFrame()                
for participant in partd.keys():
    datapart = partd[participant]
    dfpartic= pd.DataFrame()
    
    for intensity in datapart.keys():
        dfint = pd.DataFrame()
        dataint = datapart[intensity]
            
        for technique in dataint.keys():
            datatech = dataint[technique]
            dftech = pd.DataFrame()
            
            for coupling in datatech.keys():
                datacoup= datatech[coupling]
                dftemp= pd.DataFrame()
                
               
                    
                dftemp["area"] = datacoup
                dftemp["subject"] = participant
                dftemp["intensity"] = intensity
                dftemp["percentile"] =np.arange(1,101)
                dftemp["technique"] = technique
                dftemp["coupling"] = coupling[0] + coupling[6]
                dftemp["side"] = coupling[-1]
                
                
                    
                dftech = pd.concat([dftech, dftemp], ignore_index = True)
            dfint = pd.concat([dfint, dftech], ignore_index = True)
        dfpartic = pd.concat([dfpartic, dfint], ignore_index = True)
    df = pd.concat([df, dfpartic], ignore_index = True)

df = df[["subject", "intensity", "technique", "coupling", "side", "percentile", "area"]]
df = df.dropna().reset_index(drop=True)
df= df.groupby(["subject", "intensity", "technique", "coupling", "percentile"], as_index=False)["area"].mean()

intens = "hard"
tech = "dp"
coupling = "hs"

dfplot = df[(df["intensity"] == intens) & (df["technique"] == tech) & (df["coupling"] == coupling)]           
 
import seaborn as sns               
plt.figure()           
ax = sns.lineplot(data = dfplot, 
            x = "percentile", y = "area", hue = "subject", 
            hue_order = ["P3", "P5","P6","P7","P8","P12","P13", "P14"] , linewidth = 3)

plt.setp(ax.get_legend().get_texts(), fontsize='15') # for legend text
leg = plt.legend(ncol=8, loc="upper left", fontsize = 18.5, bbox_to_anchor=(0, 1))
plt.title("Coordination variability hip shoulder in double poling", fontsize = 40)
plt.xlabel("Ski cycle [%]", fontsize = 35)
plt.ylabel("Ellipse area [$°^2$/ $s^2$]", fontsize = 35)
plt.xticks(fontsize = 20)
plt.yticks(fontsize = 20)
#ax.set_ylim([0, 135000])
for line in leg.get_lines():
    line.set_linewidth(3.0)             
             
             
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
        









