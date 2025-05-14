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
rrs_dir= base_dir + "2_index_run/output/"
index_dir= base_dir + "2_index_run/output/"
output_dirrrs = base_dir + "3_plot_run/rrs_output/" 
output_dirpcu = base_dir + "3_plot_run/pcu_output/" 
output_dirndci = base_dir + "3_plot_run/ndci_output/" 

###############################################################################
                            # IMPORTS #
###############################################################################

import matplotlib.pyplot as plt
import numpy as np 
import os
import pandas as pd
os.chdir(base_dir + "3_plot_run/")
from plots_def import rrs_plot, ndci_plot, pcu_plot
from Smoo_filter import Smoo_filter
from datetime import datetime


###############################################################################
                            # PROCESADO #
###############################################################################

####empezamos por rrs

#abrimos el archivo hecho por el grupo 1
with open(rrs_dir+"data_fil.dat", "r") as doc:
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

ID                  = df['Doy'].to_numpy().astype(str)
rrs                 = linelist[1:,1:].astype(float)
wl                  = list(range(400,902,2))
doy                 = [str(i[4:]) for i in ID]

#cambiamos fechas a normal para aislar meses
normal_fech              = ()
for f in ID:
    temp=datetime.strptime(f[0:4] + f[4:], "%Y%j").strftime("%d-%m-%Y")
    normal_fech=np.append(normal_fech,temp)

#seguimos por el archivo indices
#abrimos el archivo hecho por el grupo 1

with open(index_dir+"index_data.dat", "r") as doc:
        lines = doc.readlines()
# Procesar las líneas y dividirlas por ';'
linelist_index       = [line.strip().split(";") for line in lines]
# Convertir la lista de listas a un array de numpy
linelist_index       = np.array(linelist_index)

# linelit declaration for the memory
index_data          = linelist_index[1:,1:].astype(float)
index_name          = linelist_index[0,1:]
index_all           = {}

for j in range(len(index_data[0,:])):
    temp=((abs(index_data[:,j])-min(abs(index_data[:,j])))/(max(abs(index_data[:,j]))-min(abs(index_data[:,j]))))
    #temp=Smoo_filter(temp, 4) #suavizado
    index_all[index_name[j]]=temp
#name=list(index_all.keys())
chl_name=['Chla_NDCI', 'Chla_G08', 'chla_OC4Me', 'CHL_m', 'CHL2D_m', 'CHL2C_m', 'CHL_P', 'CHL2_P']
pcu_name=['PC_D', 'PC_SY', 'PC_S', 'PC_RV', 'PC_H3', 'PC_H1b',  'PC_L', 'PC_Br2' ]
chl_temp = [index_all[var] for var in chl_name]
chl_all = np.mean(chl_temp, axis=0)
chl_std= np.nanstd(chl_temp,axis=0)

pcu_temp = [index_all[var] for var in pcu_name]
pcu_all = np.mean(pcu_temp, axis=0)
pcu_std = np.nanstd(pcu_temp,axis=0)

ndci_all = index_all['NDCI']

##############################################################################    
    #Rrs all_year
##############################################################################

year_data=np.nanmean(rrs,axis=0)
year_std= np.nanstd(rrs,axis=0)
rrs_plot(wl,year_data,output_dirrrs,"allyear")

ndci_plot(normal_fech,chl_all,chl_std,ndci_all,output_dirndci,"allyear",False)

pcu_plot(normal_fech,pcu_all,pcu_std,output_dirpcu,"allyear",False)

##############################################################################    
    #Rrs plot today
##############################################################################
today               = max(ID)
rrs_today               = rrs[np.where(ID==today)]
todaymean               = np.nanmean(rrs_today,axis=0)
date                    = int(today)
chl_today               = chl_temp
rrs_plot(wl,todaymean,output_dirrrs,"today")

##############################################################################      
    #Range select
    #filter 1 month

##############################################################################

#hayar meses
normal_month             = np.array([nf[3:5] for nf in normal_fech])

month                    ={}
days                     ={}
month_name = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
month_numb = ['01','02','03','04','05','06','07','08','09','10','11','12']
for m in range(len(month_name)):
    temp=np.where(normal_month==month_numb[m])[0]
    rrs_temp=rrs[temp]
    days[month_name[m]]=rrs_temp
    month[month_name[m]]=np.nanmean(rrs_temp,axis=0)

for i in range(len(month)):
    rrs_plot(wl,month[month_name[i]],output_dirrrs,month_name[i])



for m in range(len(month_name)):
    temp=np.where(normal_month==month_numb[m])[0]
    chl_temp=chl_all[temp]
    ndci_temp=ndci_all[temp]
    pcu_temp=pcu_all[temp]
    day_month= normal_fech[temp]
    uniq_fech=np.unique(day_month)
    month_chl                    =[]
    month_chl_std                =[]
    month_ndci                   =[]
    month_ndci_std               =[]
    month_pcu                    =[]
    month_pcu_std                =[]
    for f in uniq_fech:
        temp_2=np.where(f==day_month)[0]
        month_chl=np.append(month_chl, [np.nanmean(chl_temp[temp_2])])
        month_chl_std=np.append(month_chl_std, [np.nanstd(chl_temp[temp_2])])
        month_ndci=np.append(month_ndci, [np.nanmean(ndci_temp[temp_2])])
        month_ndci_std=np.append(month_ndci_std, [np.nanstd(ndci_temp[temp_2])])
        month_pcu=np.append(month_pcu, [np.nanmean(pcu_temp[temp_2])])
        month_pcu_std=np.append(month_pcu_std, [np.nanstd(pcu_temp[temp_2])])
    ndci_plot(uniq_fech,month_chl,month_chl_std,month_ndci,output_dirndci,month_name[m],True)
    pcu_plot(uniq_fech,month_pcu,month_pcu_std,output_dirpcu,month_name[m],True)

##############################################################################      
    #Range select
    #filter all days

##############################################################################
uniq_fech=np.unique(normal_fech)
for f in uniq_fech:
    temp=np.where(f==normal_fech)[0]
    rrs_temp=np.nanmean(rrs[temp],axis=0)
    rrs_plot(wl,rrs_temp,output_dirrrs,str(f))
