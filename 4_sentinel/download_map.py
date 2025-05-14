# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 02:03:37 2024

@author: Gonzalo Martínez Fornos
gmail:gmartinez@icm.csic.es
"""
import os
import requests
import json
import pandas as pd
#scrip para la descarga de datos copernicus
def download_map (date,download_dir,opt)->float:
    if opt=='ndci':
      # Import credentials
      #from creds import *
      os.chdir(download_dir)
      def get_keycloak(username: str, password: str) -> str:
          data = {
              "client_id": "cdse-public",
              "username": username,
              "password": password,
              "grant_type": "password",
              }
          try:
              r = requests.post("https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token",
              data=data,
              )
              r.raise_for_status()
          except Exception as e:
              raise Exception(
                  f"Keycloak token creation failed. Reponse from the server was: {r.json()}"
                  )
          return r.json()["access_token"]
              
      
      
      
      
      start_date = date
      end_date = date
      data_collection = "SENTINEL-2"
      aoi = "POINT(-6.41%2036.950)"
      keycloak_token = get_keycloak("opt4cyanproject@gmail.com", "Opt4cyan_2024")
      
      json_key = requests.get(f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=Attributes/OData.CSC.DoubleAttribute/any(att:att/Name eq 'cloudCover' and att/OData.CSC.DoubleAttribute/Value lt 30.00) and Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'productType' and att/OData.CSC.StringAttribute/Value eq 'S2MSI1C') and OData.CSC.Intersects(area=geography%27SRID=4326;{aoi}%27) and ContentDate/Start gt {start_date}T00:00:00.000Z and ContentDate/Start lt {end_date}T23:59:59.000Z").json()
      #sin covertura de nubes es el siguiente
      #json = requests.get(f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=Collection/Name eq '{data_collection}' and OData.CSC.Intersects(area=geography%27SRID=4326;{aoi}%27) and ContentDate/Start gt {start_date}T00:00:00.000Z and ContentDate/Start lt {end_date}T23:59:59.000Z").json()
      value= pd.DataFrame.from_dict(json_key['value']).head()
      
      if len(value) >0:
          # Filtra las filas donde la columna 'name' 
          filtered_S2A = value[value['Name'].str.startswith('S2A_MSIL1C_')]
          ID=filtered_S2A['Id'].tolist()
          
          if len(filtered_S2A) >0:
              for i in range(len(filtered_S2A)):
                  code = ID[i]
                  #keycloak_token = get_keycloak("opt4cyanproject@gmail.com", "Opt4cyan_2024")
                  session = requests.Session()
                  session.headers.update({'Authorization': f'Bearer {keycloak_token}'})
                  url = f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products({code})/$value"
                  response = session.get(url, allow_redirects=False)
              
                  while response.status_code in (301, 302, 303, 307):
                      url = response.headers['Location']
                      response = session.get(url, allow_redirects=False)
              
                  file = session.get(url, verify=False, allow_redirects=True)
              
                  with open(f"S2A_{i}.zip", 'wb') as p:
                      p.write(file.content)
                  print("download_A_" +str(i)+"  ok")
                   
          filtered_S2B = value[value['Name'].str.startswith('S2B_MSIL1C_')]
          ID=filtered_S2B['Id'].tolist()
          
          if len(filtered_S2B) >0:
             for i in range(len(filtered_S2B)):
                 code = ID[i]
                 #keycloak_token = get_keycloak("opt4cyanproject@gmail.com", "Opt4cyan_2024")
                 session = requests.Session()
                 session.headers.update({'Authorization': f'Bearer {keycloak_token}'})
                 url = f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products({code})/$value"
                 response = session.get(url, allow_redirects=False)
             
                 while response.status_code in (301, 302, 303, 307):
                     url = response.headers['Location']
                     response = session.get(url, allow_redirects=False)
             
                 file = session.get(url, verify=False, allow_redirects=True)
             
                 with open(f"S2B_{i}.zip", 'wb') as p:
                     p.write(file.content)
                 print("download_B_" +str(i)+"  ok")
          response= "ok"
      else:
          response= None
    
    else:
        # Import credentials
        #from creds import *
        os.chdir(download_dir)
        def get_keycloak(username: str, password: str) -> str:
            data = {
                "client_id": "cdse-public",
                "username": username,
                "password": password,
                "grant_type": "password",
                }
            try:
                r = requests.post("https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token",
                data=data,
                )
                r.raise_for_status()
            except Exception as e:
                raise Exception(
                    f"Keycloak token creation failed. Reponse from the server was: {r.json()}"
                    )
            return r.json()["access_token"]
                
        
        
        
        
        start_date = date
        end_date = date
        data_collection = "SENTINEL-2"
        aoi = "POINT(-6.41%2036.950)"
        keycloak_token = get_keycloak("opt4cyanproject@gmail.com", "Opt4cyan_2024")
        
        json_key = requests.get(f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=Attributes/OData.CSC.DoubleAttribute/any(att:att/Name eq 'cloudCover' and att/OData.CSC.DoubleAttribute/Value lt 30.00) and Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'productType' and att/OData.CSC.StringAttribute/Value eq 'S2MSI2A') and OData.CSC.Intersects(area=geography%27SRID=4326;{aoi}%27) and ContentDate/Start gt {start_date}T00:00:00.000Z and ContentDate/Start lt {end_date}T23:59:59.000Z").json()
        #sin covertura de nubes es el siguiente
        #json = requests.get(f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=Collection/Name eq '{data_collection}' and OData.CSC.Intersects(area=geography%27SRID=4326;{aoi}%27) and ContentDate/Start gt {start_date}T00:00:00.000Z and ContentDate/Start lt {end_date}T23:59:59.000Z").json()
        value= pd.DataFrame.from_dict(json_key['value']).head()
        
        if len(value) >0:
            # Filtra las filas donde la columna 'name' 
            filtered_S2A = value[value['Name'].str.startswith('S2A_MSIL2A_')]
            ID=filtered_S2A['Id'].tolist()
            
            if len(filtered_S2A) >0:
                for i in range(len(filtered_S2A)):
                    code = ID[i]
                    #keycloak_token = get_keycloak("opt4cyanproject@gmail.com", "Opt4cyan_2024")
                    session = requests.Session()
                    session.headers.update({'Authorization': f'Bearer {keycloak_token}'})
                    url = f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products({code})/$value"
                    response = session.get(url, allow_redirects=False)
                
                    while response.status_code in (301, 302, 303, 307):
                        url = response.headers['Location']
                        response = session.get(url, allow_redirects=False)
                
                    file = session.get(url, verify=False, allow_redirects=True)
                
                    with open(f"S2A_{i}.zip", 'wb') as p:
                        p.write(file.content)
                    print("download_A_" +str(i)+"  ok")
                     
            filtered_S2B = value[value['Name'].str.startswith('S2B_MSIL2A_')]
            ID=filtered_S2B['Id'].tolist()
            
            if len(filtered_S2B) >0:
               for i in range(len(filtered_S2B)):
                   code = ID[i]
                   #keycloak_token = get_keycloak("opt4cyanproject@gmail.com", "Opt4cyan_2024")
                   session = requests.Session()
                   session.headers.update({'Authorization': f'Bearer {keycloak_token}'})
                   url = f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products({code})/$value"
                   response = session.get(url, allow_redirects=False)
               
                   while response.status_code in (301, 302, 303, 307):
                       url = response.headers['Location']
                       response = session.get(url, allow_redirects=False)
               
                   file = session.get(url, verify=False, allow_redirects=True)
               
                   with open(f"S2B_{i}.zip", 'wb') as p:
                       p.write(file.content)
                   print("download_B_" +str(i)+"  ok")
            response= "ok"
        else:
            response= None
        
    return response