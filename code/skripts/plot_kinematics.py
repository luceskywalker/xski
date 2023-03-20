import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
idx = pd.IndexSlice
sns.set_style("darkgrid")

fp = r'C:\Users\b1090197\OneDrive\Documents\XSki\xski\files\joint_angles.csv'
df = pd.read_csv(fp, header=[0,1,2,3])
df = df.iloc[:,1:]
df.columns.rename("Participant", level=0, inplace=True)
df.columns.rename("Intensity", level=1, inplace=True)
df.columns.rename("Subtech", level=2, inplace=True)
df.columns.rename("Joint", level=3, inplace=True)


intensity = 'hard'
subtech = 'dp'
joint = 'Elbow'

sns.relplot(data=df.loc[:,idx[:, intensity,subtech,['Left '+joint, 'Right '+joint]]], aspect = 2, kind='line').set(
        ylabel='Joint Angle [°]',
        xlabel='Cycle [%]',
        title= joint + ' Angle (sagittal) - ' + subtech,
        xlim = [0,100]
)
plt.show()



