def vec_cod(ja_round, erg_ja_round, techd):
    import numpy as np
    from scipy import signal
    import math 
    
    jointd = dict()
    jointd["k_r"] = ja_round["Right Knee Flexion/Extension"]
    jointd["k_l"] = ja_round["Left Knee Flexion/Extension"]
    jointd["h_r"] = ja_round["Right Hip Flexion/Extension"]
    jointd["h_l"] = ja_round["Left Hip Flexion/Extension"]
    jointd["t_b"] = erg_ja_round["Pelvis_T8 Flexion/Extension"] # b = both sides
    jointd["s_l"] = erg_ja_round["T8_LeftUpperArm Flexion/Extension"]
    jointd["s_r"] = erg_ja_round["T8_RightUpperArm Flexion/Extension"]
    
    couplings = ["k_r / h_r", "k_l / h_l", "h_r / s_r", "h_l / s_l", "t_b / sh_r", "t_b / sh_l"]
    ecc = np.array([])
    conc  = np.array([])
    prox_conc = np.array([])
    prox_ecc = np.array([])
    
    coupd = {"k_r / h_r": dict(), "k_l / h_l": dict(), "h_r / s_r": dict(), 
                 "h_l / s_l": dict(), "t_b / sh_r": dict(), "t_b / sh_l": dict(),}
        
    
    for coupling in couplings:
        for interval in techd.keys():
            section = techd[interval]
            for i in range(0, len(section)-1):
            
                joint1 = jointd[coupling[0:3]]
                joint2 = jointd[coupling[-3:]]
                
                joint1_cycle = joint1[section[i]:section[i+1]]
                joint1_cycle_res = signal.resample_poly(joint1_cycle, 101, len(joint1_cycle), padtype="line")
                
                joint2_cycle = joint2[section[i]:section[i+1]]
                joint2_cycle_res = signal.resample_poly(joint2_cycle, 101, len(joint2_cycle), padtype="line")
                
                coup_ang = np.arctan2(np.diff(joint1_cycle_res), np.diff(joint2_cycle_res))*180/math.pi
                
                conc_howmany = len(coup_ang[(coup_ang<= - 90) & (coup_ang>-180)])
                ecc_howmany = len(coup_ang[(coup_ang>= 0) & (coup_ang<90)])
                prox_ecc_howmany = len(coup_ang[(coup_ang>= 90) & (coup_ang<180)])
                prox_conc_howmany = len(coup_ang[(coup_ang<=0) & (coup_ang> -90)])
                
                conc = np.append(conc, conc_howmany)
                ecc = np.append(ecc, ecc_howmany)
                prox_ecc = np.append(prox_ecc, prox_ecc_howmany)
                prox_conc = np.append(prox_conc, prox_conc_howmany)
                
        coupd[coupling]["conc"] = conc.copy()
        conc = np.array([])
        coupd[coupling]["ecc"] = ecc.copy()
        ecc = np.array([])
        coupd[coupling]["prox_ecc"] = prox_ecc.copy()
        prox_ecc = np.array([])
        coupd[coupling]["prox_conc"] = prox_conc.copy()
        prox_conc = np.array([])
        
    return coupd