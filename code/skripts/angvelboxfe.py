def angvelfe(xfe, xaa, xie, fs):
    import numpy as np
    
    
    xfe1 = xfe[2:]
    xfe2 = xfe[0:-2]
    delta = xfe1-xfe2
    angvelx = delta / (2*(1/fs))
    
    xaa1 = xaa[2:]
    xaa2 = xaa[0:-2]
    delta = xaa1-xaa2
    angvely = delta / (2*(1/fs))
    
    xie1 = xie[2:]
    xie2 = xie[0:-2]
    delta = xie1-xie2
    angvelz = delta / (2*(1/fs))
    
    xaa = xaa[1:-1]
    xfe = xfe[1:-1]
    xie = xie[1:-1]
    
    
    angvelfe = angvelx + np.sin(xaa*(np.pi/180))*angvelz
    """
    angvelfe = np.cos(xaa*(np.pi/180))*np.cos(xie*(np.pi/180))*angvelx + np.sin(xie*(np.pi/180))*angvely
    """
    
    
    return angvelfe