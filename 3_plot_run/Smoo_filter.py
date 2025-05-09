# -*- coding: utf-8 -*-
"""
Curso NetOPS 19-24 mayo 2025

@author: Gonzalo M.F. 
gmartinez@­icm.csic.es

"""
#Suavizado de index for plots

def Smoo_filter (index:float,n:int)->float:
    import numpy as np
    index_                      = np.zeros((0,))
    # n this number is for the amount of surrounding data it takes to smooth
    for i in range(len(index)):
        if i < n:
            y                   = np.mean(index[i:i+(n+1)])
        elif i >= n and i != len(index) - n:
            y                   = np.mean(index[i-n:i+(n+1)])
        else:
            y                   = np.mean(index[i-n:len(index)])
        
        index_                  = np.append(index_, y)
    
    return index_