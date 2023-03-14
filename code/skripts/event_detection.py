from IPython import get_ipython
get_ipython().magic("reset -sf")

import numpy as np
import pandas as pd
import os

os.chdir('C:/Users/Matteo/Downloads/salzburg/projects/movella challenge/file esportati')

subjects= np.array([3, 5, 6, 7, 8, 12, 13, 14])
intensities = ["easy", "medium", "hard"]

intens = dict()
part = dict()
################## double poling #######################################

for subj in subjects:
    for intensity in intensities:
        
        name = "P" + str(subj) + "_" + intensity + "_round.xlsx"
        df = pd.read_excel(name, sheet_name = "Sensor Free Acceleration", usecols ="BY:CD")
        data_round = dict(zip(df.T.index, df.T.values))
      
        if data_round:
           intens[intensity]=data_round.copy()
        data_round.clear()  

    if intens:
       part["P"+ str(subj)]=intens.copy()
    intens.clear()                    
      
    