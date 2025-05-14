# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 02:03:37 2024

@author: Gonzalo Martínez Fornos
gmail:gmartinez@icm.csic.es
"""
import datetime
import zipfile
import glob
import os
import shutil
import subprocess
from ndci_generator import ndci_generator
import tmart
#funcion de creacion de archivos acolite, es algo pesado y va algo lento el proceso
def acolite_fun (root_dir:str)->str:

    def descomprimir_archivo(archivo_zip, directorio_destino):
        with zipfile.ZipFile(archivo_zip, 'r') as zip_ref:
            zip_ref.extractall(directorio_destino)
        print("Archivo descomprimido con éxito.")
    
    downloads = root_dir +"Downloads/"
    tmp = root_dir+"tmp/"
    output = root_dir+"output/"
    
    #decompress
    dir_zip = glob.glob(downloads+"*.zip")
    for i in dir_zip:
        try:
            descomprimir_archivo(i, tmp)
            #T-mart funtion
            file_tmart  = glob.glob(tmp+"*.SAFE")[0]
            tmart.AEC.run(file_tmart,'opt4cyan','Opt4cyan_2024',overwrite=True)
            print ('tmart  Complete ####################################')
        
            # create folder
            dir_safe            = glob.glob(tmp+"/*")
            dir_safe            = dir_safe[0].replace("\\","/")
            name                =dir_safe[dir_safe.find('MS'):dir_safe.find('.SAFE')]
            
            dir_folder = os.path.join(output, name)
            os.makedirs(dir_folder)
            settings = dir_dest = output + "/" + name + "/Settings_file.txt"
        
            # copy of .txt
            def mod_txt(arch_origen, dir_dest, remplazo):
                shutil.copy(arch_origen, settings)
                with open(settings, 'r') as file:
                    cambio = file.read()
        
                modif = cambio.replace(remplazo, name_arch)
                with open(settings, 'w') as file:
                    file.write(modif)
        
            arch_origen = output+"/NDCI_doc/Settings_file.txt"
            name_arch = dir_safe[dir_safe.find('S2'):]
            dir_dest = output + name_arch
            remplazo = "[change]"
        
            mod_txt(arch_origen, dir_dest, remplazo)
                
            #ACOLITE ACTIVATE
            os.chdir("C:/Users/gmart/Proyectos/opt4cyan_tmart/acolite_py_win")
            #comando =  'cd /d C:\\Users\\doftdefault\\acolite_py_win && dist\\acolite\\acolite.exe --cli --settings="C:\\Users\\doftdefault\\Desktop\\Doñana\\OPT4CYAN\\Sentinel2\\Output\\'
            comando =  'dist\\acolite\\acolite.exe --cli --settings="C:\\Users\\gmart\\Proyectos\\opt4cyan_tmart\\Sentinel\\Output\\'
            comando = comando + name + '\\Settings_file.txt"'
            subprocess.run(comando, shell=True)
            print("Acolite ok")
            
            #Acolite data is created in this dir due to lack of permissions when executing the command
            #now we move them to the created folder
            
            origin_folder = "C:/Users/gmart/Proyectos/opt4cyan_tmart/acolite_py_win/Output/"
            destination_folder= output+"/" +name

            
            
            dir_nc= glob.glob(origin_folder + "/"+ "*L2W.nc")
            dir_nc= dir_nc[0]
            #esto es por si falla en algun momento acolite
            data= name[7:15]
            if len(dir_nc)==0:
                print("FAIL:"+data)
            #Continua si no hay fallos
            dir_nc= dir_nc.replace("\\","/")
            ndci= ndci_generator(dir_nc,destination_folder,name,origin_folder)
            
            #Doc with dates create
            
            SantaOlalla=ndci[0]
            Lucio=ndci[1]
            Hondon=ndci[2]
            Duque=ndci[3]
            
            from datetime import datetime
            fecha = datetime.strptime(data, "%Y%m%d")  
            doy                 = str(fecha.strftime('%Y'))+str(fecha.strftime('%j'))
            
            
            def c_m_arch(Today,appended):
               # Copy current file to previous file (rename)
               # Open the current file in append mode (append to the end)
               with open(Today, 'a') as Today:
                   Today.writelines(appended)
                   print("Operación completada sin errores.")
        
            Today               = root_dir + "ndci.dat"
            if len(glob.glob(Today))==0:
                with open(Today, 'w') as archivo:
                    archivo.write("Doy;Santa_Olalla;Lucio_del_rey;Hondon_del_Burro;Fuente_Duque\n")
                  
            appended = [ str(doy) + ";"+ str(SantaOlalla) + ";" + str(Lucio) +";" +str(Hondon) + ";"+str(Duque)+ "\n"]
            c_m_arch(Today,appended)
                # Abrir el archivo actual en modo append (añadir al final)
            
            def eliminar_carpeta_safe(carpeta_safe):
                try:
                    
                    shutil.rmtree(carpeta_safe)
                    print("Carpeta .SAFE eliminada:", carpeta_safe)
                except Exception as e:
                    print("Error al eliminar la carpeta .SAFE:", e)
            # Ejemplo de uso
            carpeta_safe = "C://Users//gmart//Desktop//OPT4CYAN//acolite_py_win//Tmp//"
            eliminar_carpeta_safe(carpeta_safe)
            eliminar_carpeta_safe(tmp)
            
            for j in os.listdir(origin_folder):
                os.remove(os.path.join(origin_folder,j))
        except:
            print("Saltoo.............#######################")
            if len(glob.glob(tmp+'*.SAFE'))!=0:
                   def eliminar_carpeta_safe(carpeta_safe):
                       try:
                           
                           shutil.rmtree(carpeta_safe)
                           print("Carpeta .SAFE eliminada:", carpeta_safe)
                       except Exception as e:
                           print("Error al eliminar la carpeta .SAFE:", e)
                   eliminar_carpeta_safe(tmp)
        
    
    

     
