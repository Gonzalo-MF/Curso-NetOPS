# -*- coding: utf-8 -*-
"""
Curso NetOPS 19-24 mayo 2025

@author: Gonzalo M.F. 
gmartinez@­icm.csic.es

"""

###############################################################################
                            # DIRECTORIOS #
###############################################################################

#Cargamos directorios
base_dir          = "C:/Users/gmart/Proyectos/Curso_Cuenca_2025/"
input_dir         = base_dir +"1_start/input/"
output_dir        = base_dir +"1_start/output/"
index_dir         = base_dir +"/2_index_run/input/"

###############################################################################
                            # IMPORTS #
###############################################################################

import os
os.chdir(base_dir + "1_start/")
import glob
import numpy as np
from read_TRSdata import read_TRSdata #fundion propia
from datetime import datetime
from sunposition import sunposition #fundion propia
import shutil

###############################################################################
                            # CODIGO SENSORES #
###############################################################################
ed                = "*SAM_84CE*" 
li                = "*SAM_84DC*"
lt                = "*SAM_84C8*"

###############################################################################
                            # UBICACION #
###############################################################################
 
site_name         = 'Santa_Olalla'
lat               = 36.98
lon               = -6.48
heading           = 45 #no necesario para este codigo


###############################################################################
                            # PROCESADO #
###############################################################################

#Cargamos pre_datos de carpeta input
#Consejo: Renombrar los archivos a un código que quieras para no tener errores de formato 

input_data        = glob.glob(input_dir+ "*.dat")    

#creamos un ciclo para que haga el procesado de todos los .dat en imput

for i in input_data:
    data                           = open(i,"r")
    #despues de abrir un .dat leemos las lineas
    # y eliminamos con un if los valores erroneos que no acaben en END
    lines                          =data.readlines()
    if lines[len(lines)-2]=='[END] of [Spectrum]\n':
        #leemos cada linea y cortamos cada vez que encontramos la palabra 
        data                           = open(i,"r")
        for dummy in iter(data.readline,''):
            if not dummy:
                break
            if '#TBID:' in dummy:
                tmp_name                    = dummy.split('#TBID:')
                tmp_name                    = tmp_name[1].replace(" ", "_")
                tmp_name                    = tmp_name.replace(":", "-")
                fields                      = tmp_name.split(";")
                if fields[2]                == 'RAW':
                    fname_out               = (fields[1] + '_Spectrum_RAW_'  + fields[0] + '_000_' + fields[1]  + '_1234_RAW' + fields[0] + '_000_00.dat')
                else:
                    fname_out               = (fields[1] + '_Spectrum_Calibrated_' + fields[0] + '_000_' + fields[1] + '_1234_Calibrated_' + fields[0] + '_000_01.dat')
            if '[Spectrum]' in dummy:
                with open(output_dir + fname_out, "w") as unit2:
                    unit2.writelines(str(dummy.format("%s\r\n")))
                    while True:
                        dummy               = data.readline()
                        unit2.writelines(str(dummy.format("%s\r\n")))
                        if '[END] of [Spectrum]' in dummy:
                            break
        
        data.close()
    #elegimos solo los Calibrated 

    ed_in = glob.glob(output_dir + ed + "*Calibrated*" + "*.dat")
    li_in = glob.glob(output_dir + li + "*Calibrated*" + "*.dat")
    lt_in = glob.glob(output_dir + lt + "*Calibrated*" + "*.dat")
    
    #ahora toca un limpiado de datos para quedaarnos solo con un doc de rrs
    float_formatter                         = "{:.8f}".format #is for format 
    np.set_printoptions(formatter={'float_kind':float_formatter}) 
    #calculate es, lt anf li with rearrange measurements script
    #hay que hacer un bucle para calcular ed LT y LI
    ######    calibrated #MT
    ###rango de spectro entre 400 y 900
    wl                          = list(range(400,902,2))
    sensors=[ed_in,li_in,lt_in]
    keys=['ed','li','lt']
    all_data={}
    all_doy={}
    k=0
    for sensor in sensors:
        measurement                 = np.zeros((0,len(wl)))
        timedate                    = np.zeros((0,1))
        doy                         = np.zeros((0,1))
        year                        = np.zeros((0,1))
        angle                       = np.zeros((0,2))
        count                       = 0
        for s in range(len(sensor)):
            if s == sensor.index(sensor[-1]):
                break
    
            if sensor:
                fname = str(sensor[s])
                data = read_TRSdata(fname)
                time = datetime.strptime(data['DateTime'], "%Y-%m-%d %H:%M:%S")
    
                # Hacemos un primer filtro de horas para quitar las horas que claramente no hay luz
                # Así hacemos que sea más rápido el proceso y luego filtramos por ángulo, entre 40 y 90
                if 10 <= time.hour <= 16:
                    measurement_tmp = np.interp(wl, data['Data'][0:-1, 0], data['Data'][0:-1, 1])
                    doy_tmp = float(time.strftime('%j'))
                    # jd              = OPT4CYAN_julianday(time.year, time.month, time.day, time.hour, time.minute, time.second)
                    hour_d = time.hour + (time.minute + time.second / 60) / 60
                    angle_tmp = sunposition(doy_tmp, hour_d, lat, lon)
                    zenith = angle_tmp[0]
    
                    if 40 <= zenith <= 90:
                        doy = np.append(doy, doy_tmp + round(hour_d / 24, 4))
                        year = np.append(year, time.year)
                        measurement = np.append(measurement, [measurement_tmp], axis=0)
                        angle = np.append(angle, [angle_tmp], axis=0)
                        count += 1
        all_data[keys[k]]=measurement
        all_doy[keys[k]]=doy
        k=k+1
        print("Complete sensors Variable     100%")
    #finalmente creamos la variable RRs y lo guadamos en un archivo .dat o en un array
    Rrs                                     = np.zeros((0,len(wl)))
    lt_dat                                  = np.zeros((0,len(wl)))
    ed_dat                                  = np.zeros((0,len(wl)))
    doy_rrs                                 = np.zeros((0,1))
    angle_rrs                               = np.zeros((0,2))
    year_rrs                                = np.zeros((0,1))
    
    
    #create a variable RRs and create file document and paste the importants dates
    if len(all_doy['lt'])!=0:
        for z in np.arange(len(all_doy['lt'])):
            delta_t                         = abs(all_doy['lt'][z] - all_doy['ed'])
            if min(delta_t) < 1e-4: #1./(24*60*60) # 1 sec
                index_t                     = np.where(delta_t == min(delta_t))                    
                Rrs                         = np.append(Rrs,np.divide(all_data['lt'][z],all_data['ed'][index_t]),axis=0)
                lt_dat                      = np.append(lt_dat,all_data['lt'][index_t],axis=0)
                ed_dat                      = np.append(ed_dat,all_data['ed'][index_t],axis=0)
                doy_rrs                     = np.append(doy_rrs,all_doy['lt'][z])
                doy_str                     = [str(int(num)).zfill(3) for num in doy_rrs]
                angle_rrs                   = np.append(angle_rrs,[angle[z]],axis=0)
                year_rrs                    = np.append(year_rrs,year[z])
                year_str                    =  [str(int(num)) for num in year_rrs]
                ID                          = [year_str[i] + doy_str[i] for i in range(len(doy_str))]

   #lo guardamos en un array o .dat
   #haremos un .dat por facilidad y rapided para programar aunque es mas solido estudiar el paquete array
    def c_m_arch(Today,appended):
        # Copy current file to previous file (rename)
        # Open the current file in append mode (append to the end)
        with open(Today, 'a') as Today:
            Today.writelines(appended)
    
    data_doc                               = index_dir+ "data" +".dat"
    lt_doc                                 = index_dir + "lt.dat"
    ed_doc                                 = index_dir + "ed.dat"
    backup_doc                           = index_dir+ "backup" +".dat"
    title                               =["Id","Year","Doy","Zenith","Azimuth"] 
    
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
        columna1_str = ';'.join(map(str, angle_rrs[data,:]))
        appended     =  (str(ID[data])+";"+str(int(year_rrs[data]))+";"+str(doy_rrs[data])+";"+columna1_str+";"+columna2_str+"\n")
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
        

   
    for data in range(len(lt_dat)):
        columna2_str = ';'.join(map(str, lt_dat[data,:]))
        columna1_str = ';'.join(map(str, angle_rrs[data,:]))
        appended     =  (str(ID[data])+";"+str(int(year_rrs[data]))+";"+str(doy_rrs[data])+";"+columna1_str+";"+columna2_str+"\n")
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
        

   
    for data in range(len(ed_dat)):
        columna2_str = ';'.join(map(str, ed_dat[data,:]))
        columna1_str = ';'.join(map(str, angle_rrs[data,:]))
        appended     =  (str(ID[data])+";"+str(int(year_rrs[data]))+";"+str(doy_rrs[data])+";"+columna1_str+";"+columna2_str+"\n")
        c_m_arch(ed_doc,appended)
    print("Appended ed and Backup")
        
        
        
   #borramos el output de star     
    for f in os.listdir(output_dir):
        os.remove(os.path.join(output_dir, f)) 
    print("Arch ----> "+ str(i) +"     Complete")
        
    