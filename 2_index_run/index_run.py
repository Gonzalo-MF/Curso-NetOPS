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

###############################################################################
                            # OPEN #
###############################################################################

#abrimos el archivo hecho por el grupo 1
with open(input_dir+"data.dat", "r") as doc:
        lines = doc.readlines()
# Procesar las líneas y dividirlas por ';'
linelist       = [line.strip().split(";") for line in lines]
# Convertir la lista de listas a un array de numpy
linelist       = np.array(linelist)
df             = pd.DataFrame(linelist)
df.columns     = df.iloc[0] # Asigna la primera fila como nombres de columnas
df             = df[1:]  

###############################################################################
                            # DATA EXTRATION #
###############################################################################          
#necesitamos seleccionar solo la rrs de las columnas y la fecha doy y year

ID                  = df['Id'].to_numpy().astype(int)

doy                 = df['Doy'].to_numpy().astype(float)
year                = df['Year'].to_numpy().astype(int)
Rrs                 = linelist[1:,5:].astype(float)
#comenzamos con los indices, para ello habremos seleccionado algunos
index_data          = index_alg(Rrs)[0]
index_name          = index_alg(Rrs)[1]   


#creamos el codigo otra vez para guardarlo en .dat 
def c_m_arch(data,appended):
    # Copy current file to previous file (rename)
    # Open the current file in append mode (append to the end)
    with open(data, 'a') as data:
        data.writelines(appended)

data_doc                               = output_dir+ "data" +".dat"
backup_doc                           = output_dir+ "backup" +".dat"
title                               =["ID","Year","Doy"] 

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
    appended     =  (str(ID[data])+";"+str(int(year[data]))+";"+str(doy[data])+";"+columna2_str+"\n")
    c_m_arch(data_doc,appended)
print("Appended data and backup")
