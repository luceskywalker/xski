import os
os.chdir(r'Directory with present script, "
         "Developer Toolkit scripts and mvnx file to load')

from load_mvnx import load_mvnx
data = load_mvnx("P3_easy_round.mvnx")
vel = data.get_segment_angular_vel(0,-1,-1) # segment (pelvis), all frames, all axis













