# -*- coding: utf-8 -*-
"""
Curso NetOPS 19-24 mayo 2025

@author: Gonzalo M.F. 
gmartinez@­icm.csic.es

"""

###############################################################################
                            # DIRECTORIOS #
###############################################################################

base_dir          = "C:/Users/gmart/Proyectos/Curso_Cuenca_2025/"
input_dir         =base_dir + "2_index_run/input/"
output_dir        =base_dir + "2_index_run/output/" 

###############################################################################
                            # IMPORTS #
###############################################################################
import os
os.chdir(base_dir + "2_index_run")
import glob
import shutil
import numpy as np
import pandas as pd
from index_alg import index_alg
import matplotlib.pyplot as plt

###############################################################################
                            # OPEN #
###############################################################################

#abrimos el archivo hecho por el grupo 1
with open(input_dir+"ed.dat", "r") as doc:
        lines = doc.readlines()
linelist       = [line.strip().split(";") for line in lines]
# Convertir la lista de listas a un array de numpy
linelist       = np.array(linelist)


with open(input_dir+"lt.dat", "r") as doc:
        lines = doc.readlines()
linelist_lt       = [line.strip().split(";") for line in lines]
# Convertir la lista de listas a un array de numpy
linelist_lt       = np.array(linelist_lt)


###############################################################################
                            # DATA EXTRATION #
###############################################################################          
#necesitamos seleccionar solo la rrs de las columnas y la fecha doy y year
lt= linelist_lt[1:,5:].astype(float)
ed=linelist[1:,5:].astype(float)

Rrs=lt/ed

df             = pd.DataFrame(linelist)
df.columns     = df.iloc[0] # Asigna la primera fila como nombres de columnas
df             = df[1:]  

ID                  = df['Id'].to_numpy().astype(int)

doy                 = df['Doy'].to_numpy().astype(float)
year                = df['Year'].to_numpy().astype(int)

###############################################################################
                            # LAND FILTER #
############################################################################### 

rrs_fil               = []
ed_fil                    = []
lt_fil                    = []
doy_uni=np.unique(ID)
for d in doy_uni:
    tmp              = np.where(d==ID)[0]
    tmp_rrs          = Rrs[tmp,:]
    tmp_ed           = ed[tmp,:]
    tmp_lt           = lt[tmp,:]
    max_rrs          = np.sum(Rrs[tmp,:],axis=1)
    mask             = max_rrs-np.nanmax(max_rrs)
    len_id           = int(round(len(mask)/2,0))
    mask_limp        = np.sort(mask)[:len_id]
    ind              = []
    for i in  mask_limp:
        tmp          = np.where(i==mask)[0]
        ind.append(tmp)
    ind = np.array(ind)[:,0]
    rrs_median   = np.nanmedian(tmp_rrs[ind],axis=0)
    ed_median   = np.nanmedian(tmp_ed[ind],axis=0)
    lt_median   = np.nanmedian(tmp_lt[ind],axis=0)
    rrs_fil.append(rrs_median)
    ed_fil.append(ed_median)
    lt_fil.append(lt_median)
Rrs                  = np.array(rrs_fil) 
ed                   = np.array(ed_fil)
lt                   = np.array(lt_fil)   


###############################################################################
                            # Plots lt ed and rrs #
############################################################################### 
wl                  = list(range(400,902,2))
for i in range(len(doy_uni)):
    plt.plot(wl,Rrs[i,:])

for i in range(len(doy_uni)):
    plt.plot(wl,ed[i,:])
    
for i in range(len(doy_uni)):
    plt.plot(wl,lt[i,:])


#lo guardamos en un array o .dat
#haremos un .dat por facilidad y rapided para programar aunque es mas solido estudiar el paquete array
def c_m_arch(Today,appended):
    # Copy current file to previous file (rename)
    # Open the current file in append mode (append to the end)
    with open(Today, 'a') as Today:
        Today.writelines(appended)

data_doc                               = output_dir+ "data_fil" +".dat"
lt_doc                                 = output_dir + "lt_fil.dat"
ed_doc                                 = output_dir + "ed_fil.dat"
backup_doc                           = output_dir+ "backup_fil" +".dat"
title                               =["Doy"] 
###############################################################################
                            # Rrs #
###############################################################################
#hacemos que wl haga su nombre a Rrs_ y el valor de wl
name_rrs = [f"Rrs_{r}" for r in range(400, 901, 2)]
#creamos los archivos porque el primer intento no existe, solo pasara una vez
if len(glob.glob(data_doc))==0:
    with open(data_doc, 'w') as archivo:
       # Convertir columna3 en una cadena de texto donde cada valor está separado por un ;
       columna2_str = ';'.join(map(str, name_rrs))
       columna1_str = ';'.join(map(str, title))

        # Escribir los datos en una fila, con los valores de columna3 como columnas separadas por ;
       archivo.write(columna1_str + ";"+columna2_str+"\n")
    #crea yesterday
    open(backup_doc,'w')
    shutil.copy(data_doc, backup_doc)
########
#si ya esta creado el archivo solo hayq ue guardadr la info 
####
    
shutil.copy(data_doc, backup_doc)
   
for data in range(len(Rrs)):
    columna2_str = ';'.join(map(str, Rrs[data,:]))
    appended     =  (str(doy_uni[data])+";"+columna2_str+"\n")
    c_m_arch(data_doc,appended)
print("Appended Data and Backup")
    
###############################################################################
                            # Lt #
###############################################################################    
    
#hacemos que wl haga su nombre a lt_ y el valor de wl
name_lt = [f"Lt_{r}" for r in range(400, 901, 2)]
#creamos los archivos porque el primer intento no existe, solo pasara una vez
if len(glob.glob(lt_doc))==0:
    with open(lt_doc, 'w') as archivo:
       # Convertir columna3 en una cadena de texto donde cada valor está separado por un ;
       columna2_str = ';'.join(map(str, name_lt))
       columna1_str = ';'.join(map(str, title))
        # Escribir los datos en una fila, con los valores de columna3 como columnas separadas por ;
       archivo.write(columna1_str + ";"+columna2_str+"\n")
########
#si ya esta creado el archivo solo hayq ue guardadr la info 
####
    

   
for data in range(len(lt)):
    columna2_str = ';'.join(map(str, lt[data,:]))
    appended     =  (str(doy_uni[data])+";"+columna2_str+"\n")
    c_m_arch(lt_doc,appended)
print("Appended lt and Backup")

###############################################################################
                        # ed #
###############################################################################    

#hacemos que wl haga su nombre a ed_ y el valor de wl
name_lt = [f"ed_{r}" for r in range(400, 901, 2)]
#creamos los archivos porque el primer intento no existe, solo pasara una vez
if len(glob.glob(ed_doc))==0:
    with open(ed_doc, 'w') as archivo:
       # Convertir columna3 en una cadena de texto donde cada valor está separado por un ;
       columna2_str = ';'.join(map(str, name_lt))
       columna1_str = ';'.join(map(str, title))

        # Escribir los datos en una fila, con los valores de columna3 como columnas separadas por ;
       archivo.write(columna1_str + ";"+columna2_str+"\n")
########
#si ya esta creado el archivo solo hayq ue guardadr la info 
####
    

   
for data in range(len(ed)):
    columna2_str = ';'.join(map(str, ed[data,:]))
    appended     =  (str(doy_uni[data])+";"+columna2_str+"\n")
    c_m_arch(ed_doc,appended)
print("Appended ed and Backup")
    

###############################################################################
                            # Index #
############################################################################### 

#comenzamos con los indices, para ello habremos seleccionado algunos
index_data          = index_alg(Rrs)[0]
index_name          = index_alg(Rrs)[1]   


#creamos el codigo otra vez para guardarlo en .dat 
def c_m_arch(data,appended):
    # Copy current file to previous file (rename)
    # Open the current file in append mode (append to the end)
    with open(data, 'a') as data:
        data.writelines(appended)

data_doc                               = output_dir+ "index_data" +".dat"
backup_doc                           = output_dir+ "index_backup" +".dat"
title                               =["Doy"] 

#creamos los archivos porque el primero no existe, solo pasara una vez
if len(glob.glob(data_doc))==0:
    with open(data_doc, 'w') as archivo:
       # Convertir columna3 en una cadena de texto donde cada valor está separado por un ;
       columna2_str = ';'.join(map(str, index_name))
       columna1_str = ';'.join(map(str, title))

        # Escribir los datos en una fila, con los valores de columna3 como columnas separadas por ;
       archivo.write(columna1_str + ";"+columna2_str+"\n")
    #crea backup
    open(backup_doc,'w')
    shutil.copy(data_doc, backup_doc)
########
#si ya esta creado el archivo solo hayq ue guardadr la info 
####
    
shutil.copy(data_doc, backup_doc)
index_data             = np.transpose(index_data)
for data in range(len(index_data)):
    columna2_str = ';'.join(map(str, index_data[data,:]))
    appended     =  (str(doy_uni[data])+";"+columna2_str+"\n")
    c_m_arch(data_doc,appended)
print("Appended data and backup")
