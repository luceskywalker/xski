from IPython import get_ipython
get_ipython().magic("reset -sf")

import matplotlib.pyplot as plt
import numpy as np
import pickle
import pandas as pd
import seaborn as sns
import os 
os.chdir('C:/Users/Matteo/Downloads/salzburg/projects/movella challenge/xski/code/skripts')
from vector_coding import vec_cod

"""
file = open("C:/Users/Matteo/Downloads/salzburg/projects/movella challenge/xski/files/ski_cycles.pkl",'rb')
ski_cycles = pickle.load(file)
file.close()

file = open("C:/Users/Matteo/Downloads/salzburg/projects/movella challenge/file esportati/joint_angles.pkl",'rb')
ja = pickle.load(file)
file.close()

file = open("C:/Users/Matteo/Downloads/salzburg/projects/movella challenge/file esportati/erg_joint_angles.pkl",'rb')
erg_ja = pickle.load(file)
file.close()
del file

intensd= dict()
particd = dict()
technique_d = dict()

for participant in ski_cycles.keys():
    partd = ski_cycles[participant]
    for intensity in partd.keys():
        intd = partd[intensity]
        for technique in intd.keys():
            ja_round = ja[participant][intensity]
            ja_round = ja[participant][intensity]
            erg_ja_round = erg_ja[participant][intensity]
            erg_ja_round = erg_ja[participant][intensity]
            
            techd = intd[technique]
            coupd = vec_cod(ja_round, erg_ja_round, techd)
            
            if coupd:            
               technique_d[technique]= coupd.copy()
            coupd.clear()
            
        if technique_d:            
           intensd[intensity]= technique_d.copy()
        technique_d.clear()
        
    if intensd:
        particd[participant] = intensd.copy()
    intensd.clear()

f = open("C:/Users/Matteo/Downloads/salzburg/projects/movella challenge/xski/files/coordination_states.pkl","wb")
pickle.dump(particd,f)
f.close()
"""

file = open("C:/Users/Matteo/Downloads/salzburg/projects/movella challenge/xski/files/coordination_states.pkl",'rb')
coord_dict = pickle.load(file)
file.close()
del file

df =pd.DataFrame()

# modidicare campi dizionario, poi è tutto abb  veloce

    
for participant in coord_dict.keys():
    datapart = coord_dict[participant]
    dfpartic= pd.DataFrame()
    
    for intensity in datapart.keys():
        dfint = pd.DataFrame()
        dataint = datapart[intensity]
            
        for technique in dataint.keys():
            datatech = dataint[technique]
            dftech = pd.DataFrame()
            
            for coupling in datatech.keys():
                datacoup= datatech[coupling]
                dfcoup= pd.DataFrame()
                
                for phase in datacoup.keys():
                    dataphase= datacoup[phase]
                    dftemp= pd.DataFrame()
                    
                    dftemp["phase_freq"] = dataphase
                    dftemp["subject"] = int(participant[1:])
                    dftemp["intensity"] = intensity
                    dftemp["technique"] = technique
                    dftemp["coupling"] = coupling[0] + coupling[6]
                    dftemp["side"] = coupling[-1]
                    dftemp["phase"] =  phase
                    dftemp["cycle"] = np.arange(1, len(dataphase)+1)
                    
                    
                    dfcoup= pd.concat([dfcoup, dftemp], ignore_index = True)
                dftech = pd.concat([dftech, dfcoup], ignore_index = True)
            dfint = pd.concat([dfint, dftech], ignore_index = True)
        dfpartic = pd.concat([dfpartic, dfint], ignore_index = True)
    df = pd.concat([df, dfpartic], ignore_index = True)

df = df[["subject", "intensity", "technique", "coupling", "side", "phase", "cycle", "phase_freq"]]

df= df.groupby(["subject", "intensity", "technique", "coupling", "phase", "cycle"], as_index=False)["phase_freq"].mean()

#dfmean = df.groupby(["subject", "intensity", "technique", "coupling", "phase"], as_index=False)["phase_freq"].mean()
#dfstd = df.groupby(["subject", "intensity", "technique", "coupling", "phase"], as_index=False)["phase_freq"].std()


dfmean_coup = df[(df["coupling"] == "kh") & 
                     (df["intensity"] == "medium") &
                     (df["technique"] == "dp")]


sns.barplot(data = dfmean_coup, x = "subject", y = "phase_freq", hue = "phase")

