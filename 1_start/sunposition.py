
# -*- coding: utf-8 -*-
"""
Curso NetOPS 19-24 mayo 2025

@author: Gonzalo M.F. 
gmartinez@­icm.csic.es

"""
# Description:
    #detect sun position

import math    

#A program to calculate Sun zenith and azimuth for given date, time, latitude, and longitude
def sunposition (doy:float, hour:float, lat:float, lon:float)->float:
    #Returns:It returns the sun position [zenith, azimuth]
    #transform time
    
    #mean solar time
    mean_solar_time= hour + float(lon)/15.0 

    #equation of time
    a1= 1.00554*float(doy) - 6.28306    
    a2= 1.93946*float(doy) + 23.35089 
    equation_of_time= -7.67825*math.sin(a1/180.0*math.pi) - 10.09176*math.sin(a2/180.0*math.pi)

    #true solar time
    true_solar_time= mean_solar_time + equation_of_time/60.0 - 12.0

    #hour angle in degrees
    hour_angle= true_solar_time*15.0

    #solar declination in degrees
    a3= 0.9683*float(doy) - 78.00878    
    solar_declination= 23.4856*math.sin(a3/180.0*math.pi)

    #elevation and azimuth
    sun_y= math.sin(float(lat)/180.0*math.pi)*math.sin(solar_declination/180.0*math.pi) + math.cos(float(lat)/180.0*math.pi)*math.cos(solar_declination/180.0*math.pi)*math.cos(hour_angle/180.0*math.pi)
    elevation= math.asin(sun_y)/math.pi*180.0
    sun_x= math.cos(solar_declination/180.0*math.pi)*math.sin(hour_angle/180.0*math.pi)/math.cos(elevation/180.0*math.pi)
    corrected_sun_x= (-math.cos(float(lat)/180.0*math.pi)*math.sin(solar_declination/180.0*math.pi) + math.sin(float(lat)/180.0*math.pi)*math.cos(solar_declination/180.0*math.pi)*math.cos(hour_angle/180.0*math.pi))/math.cos(elevation/180.0*math.pi)
    azimuth= math.asin(sun_x)/math.pi*180.0
    
    if(corrected_sun_x <= 0):
        azimuth= 180.0 - azimuth
    if(corrected_sun_x > 0) and (sun_x <= 0):
        azimuth= 360.0 + azimuth
    azimuth= azimuth + 180.0
    
    if(azimuth > 360.0):
        azimuth= azimuth - 360.0
    
    zenith= 90.0 - elevation
    
    
    sun_position= [zenith,azimuth]   
    return sun_position

