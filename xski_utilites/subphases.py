from xski_utilites.signal import euler_from_quaternion, low_pass_filter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_pole_off_dp(start_c1, start_c2, join_angles):
    left = join_angles['Left Elbow Flexion/Extension'][start_c1:start_c1+(start_c2-start_c1)*2//3]
    right = join_angles['Right Elbow Flexion/Extension'][start_c1:start_c1+(start_c2-start_c1)*2//3]

    lmax = np.argmin(left)
    if lmax == 0:
        lmax = int(np.diff([start_c1, start_c2])//2)
    rmax = np.argmin(right)
    if rmax == 0:
        rmax = lmax

    if np.diff([lmax, rmax]) > 100:
        print('Pole off difference large: '+ str(np.diff([lmax, rmax])))

    plt.plot(left)
    plt.plot(right)
    plt.vlines(np.mean([lmax, rmax]), ymin=min(left), ymax=max(left), colors='k')
    #plt.show()

    pole_off = start_c1 + int(np.mean([lmax, rmax]))


    return pole_off
