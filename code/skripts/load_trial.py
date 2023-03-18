import os
os.chdir(r'C:/Users/Matteo/Downloads/salzburg/projects/movella challenge/xski/code/skripts')

from load_mvnx_movella import load_mvnx
data = load_mvnx("C:/Users/Matteo/Downloads/salzburg/projects/movella challenge/xsens_case-study-kit_2023-03-07_1502/Case Study Kit/Recordings/P3/MVNX/easy_round.mvnx")
vel = data.get_segment_angular_vel(0,-1,-1) # segment (pelvis), all frames, all axis

velnew = [i*180/np.pi for i in vel]












