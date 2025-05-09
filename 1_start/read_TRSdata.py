# -*- coding: utf-8 -*-
"""
Curso NetOPS 19-24 mayo 2025

@author: Gonzalo M.F. 
gmartinez@­icm.csic.es

"""
# Description:
    #read and format measurements
import numpy as np
import re
    

def read_TRSdata (fname:str)->float: 

    # count lines of header and datablock
    dummy = ''
    record = 0
    data_section = [np.nan, np.nan]

    with open(fname, "r") as unit:
        for dummy in unit:
            if not dummy:
                break
            if dummy.find('[DATA]') >= 0:
                if np.isnan(data_section[0]):
                    data_section[0] = record
                else:
                    data_section[1] = record
            record += 1


    # initialize data structutre
    structure= {
      "Version"                         : int(1), 
      "IDData"                          : "", 
      "IDDevice"                        : "", 
      "IDDataType"                      : "", 
      "IDDataTypeSub1"                  : "", 
      "IDDataTypeSub2"                  : "", 
      "IDDataTypeSub3"                  : "", 
      "DateTime"                        : "", 
      "PositionLatitude"                : float(1), 
      "PositionLongitude"               : float(1), 
      "Comment"                         : "", 
      "CommentSub1"                     : "", 
      "CommentSub2"                     : "", 
      "CommentSub3"                     : "", 
      "IDMethodType"                    : "", 
      "MethodName"                      : "", 
      "Mission"                         : "", 
      "MissionSub"                      : float(1), 
      "RecordType"                      : float(1), 
      "attributes"                      : {
        "CalFactor"                     : float(1), 
        "IDBasisSpec"                   : "", 
        "IDDataBack"                    : "", 
        "IDDataCal"                     : "", 
        "IntegrationTime"               : float(1), 
        "P31"                           : float(1), 
        "P31e"                          : float(1), 
        "PathLength"                    : float(1), 
        "RAWDynamic"                    : float(1), 
        "Temperature"                   : float(1), 
        "Unit1"                         : "", 
        "Unit2"                         : "", 
        "Unit3"                         : "", 
        "Unit4"                         : "", 
        "p999"                          : ""}, 
      "Data"                            : np.zeros((data_section[1]-data_section[0]-1, 4))}
    
    struct_tags                                                             = list(structure.keys())
    attributes_tags                                                         = list(structure["attributes"].keys())
    
    struct_tags_l                                                           = list(map(str.lower,struct_tags)) 
    attributes_tags_l                                                       = list(map(str.lower,attributes_tags)) 
    
    # read file
    dummy                                                                   = ''
    record                                                                  = 0
    unit                                                                    = open(fname,"r")
    for dummy in iter(unit.readline, ''):
        dummy = dummy.replace('\n', '')

        if (record <= data_section[0]) or (record >= data_section[1]):
            if dummy.find("[") != -1:
                pass
            else:
                stringa = re.split('[ =]+', dummy)
                var_name = stringa[0]
                var_value = ' '

                if len(stringa) == 2:
                    var_value = stringa[1]

                if len(stringa) == 3:
                    var_value = stringa[1] + ' ' + stringa[2]

                if var_name.lower() in struct_tags_l:
                    index = struct_tags_l.index(var_name.lower())
                    structure[struct_tags[index]] = var_value

                if var_name.lower() in attributes_tags_l:
                    index = attributes_tags_l.index(var_name.lower())
                    structure['attributes'][attributes_tags[index]] = var_value

        else:
            string = list(filter(None, re.split('[ \n]+', dummy)))
            structure['Data'][record - data_section[0] - 1, :] = string

        record += 1

    unit.close()
    
    return structure
     
    
