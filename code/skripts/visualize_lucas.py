import mvnx
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#from code.xski_utilites.signal import low_pass_filter
# file path

# fp = Path(r'C:\Users\b1090197\Documents\Case Study Kit\Recordings\P3\MVN\hard_round.mvnx')
# fp2 = Path(r'C:\Users\b1090197\Documents\Case Study Kit\Recordings\P3\MVNX\hard_round.mvnx')
# data = mvnx.load(fp)
# data2 = mvnx.load(fp2)
# com = pd.DataFrame(data.centerOfMass)
# com.plot()
# plt.show()
#
# com1 = np.diff(com, n=1, axis=0)
# com1 = np.gradient(com, axis=0)
# com2 = np.diff(com1, n=1, axis=0)

fp = r'C:\Users\b1090197\Documents\Case Study Kit\Recordings\P12\MVNX\hard_round.xlsx'

com = pd.read_excel(fp, sheet_name='Center of Mass', index_col=0)
gps = pd.read_excel(fp, sheet_name='Global Position', index_col=0)

plt.figure()
ax = plt.axes(projection='3d')
ax.plot3D(com['CoM pos x'], com['CoM pos y'], com['CoM pos z'])
plt.show()
#plt.plot(low_pass_filter(com.iloc[:,0], 240, .125, 4))
#plt.show()
#plt.plot(com.iloc[:,1])
#plt.plot(low_pass_filter(com.iloc[:,0], 240, .125, 4), low_pass_filter(com.iloc[:,2], 240, .125, 4))
#plt.show()

plt.plot(gps.iloc[:,0], gps.iloc[:,1])
plt.show()
#plt.plot(np.linalg.norm(gps.iloc[:,:2], axis =1), gps.iloc[:,2])
#plt.show()
a=12



