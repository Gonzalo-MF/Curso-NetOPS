# -*- coding: utf-8 -*-
"""
Curso NetOPS 19-24 mayo 2025

@author: Gonzalo M.F. 
gmartinez@­icm.csic.es

"""
import numpy as np
import math
def index_alg(Rrs)->float:    
    variables = ["PC_D", "PC_SY", "PC_S", "PC_RV", "PC_H1", "PC_H1b","PC_H3", "PC_W", "PC_L", "Chla_NDCI", "Chla_G08", "PC_Lu", 
    "PC_Br1", "PC_Br2", "PC_Br3", "chla_OC4Me", "CHL_m", "CHL2D_m", 
    "CHL2C_m", "CHL_P", "CHL2_P", "NDCI"]
    
    
    for var in variables:
        global PC_D, PC_SY, PC_S, PC_RV, PC_H1, PC_H1b,PC_H3, PC_W, PC_L, Chla_NDCI, Chla_G08, PC_Lu, PC_Br1, PC_Br2, PC_Br3, chla_OC4Me, CHL_m, CHL2D_m, CHL2C_m, CHL_P, CHL2_P, NDCI
        globals()[var]                              = np.zeros((0, 1))
    Rrsm                                            = Rrs/(0.52 +1.7*Rrs)
    all_var                                     ={}
    wl = np.array(range(400,902,2))
    for i in range(len(Rrs)):
        # Dekker, A.G., 1993. Detection of Optical water quality parameters for eutrophic waters by high resolution remote sensing. Free Universit. 1–222.
        PC_D_tmp                                    = np.interp(600,wl,Rrs[i,:]) + (np.interp(648,wl,Rrs[i,:]) - np.interp(600,wl,Rrs[i,:]))/2 - np.interp(624,wl,Rrs[i,:])
        PC_D                                        = np.append(PC_D, [PC_D_tmp])
    
        #Schalles, J.F, Yacobi, Y.Z. 2000. Remote detection and seasonal patterns of phycocyanin, carotenoid, and chlorophyll pigments in eutrophic waters. Archives fur Hydrobiologia - Special Issues Advancements in Limnology. 55: 153-168 in Ruiz-Verdu et al. "An evaluation of algorithms for the remote sensing of cyanobacterial biomass" Remote Sensing of Environment 112 (2008) 3996–4008. eq.2
        PC_SY_tmp                                   = (np.interp(650,wl,Rrs[i,:])/np.interp(625,wl,Rrs[i,:])-0.97)*1096.5                         
        PC_SY                                       = np.append(PC_SY,[PC_SY_tmp])
        #Simis et al. "Remote sensing of the cyanobacterial pigment phycocyanin in turbid inland water" Limnol. Oceanogr.,50(1), 2005, 237–245
        # --> Simis et al. "Influence of phytoplankton pigment composition on remote sensing of cyanobacterial biomass" Remote Sensing of Environment 106 (2007) 414 – 427 
        bb779                                       = 1.61*np.interp(779,wl,Rrs[i,:])/(0.082-0.6*np.interp(779,wl,Rrs[i,:])) #Gons, Rijkeboer, Ruddick "Effect of a waveband shift on chlorophyll retrieval from MERIS imagery of inland and coastal waters" Journal of Plankton Research, Volume 27, Issue 1, January 2005, Pages 125–127                             
        a_chla665                                   = np.interp(709,wl,Rrs[i,:])/np.interp(665,wl,Rrs[i,:])*(0.7+bb779)-bb779**1.062-0.4
        
        chla_S                                      = a_chla665/0.0161
        a_chla_pc620                                = (np.interp(709,wl,Rrs[i,:])/(np.interp(620,wl,Rrs[i,:]))* (0.727+bb779)-bb779-0.281)/0.84
        a_chla665                                   = (np.interp(709,wl,Rrs[i,:])/(np.interp(665,wl,Rrs[i,:]))* (0.727+bb779)-bb779-0.401)/0.68
        a_pc620                                     = a_chla_pc620 - 0.24*a_chla665
        PC_S_tmp                                    = a_pc620/0.007
        PC_S                                        =np.append(PC_S,[PC_S_tmp])
    
        #Ruiz-Verdu et al. "An evaluation of algorithms for the remote sensing of cyanobacterial biomass" Remote Sensing of Environment 112 (2008) 3996–4008. eq.3
        PC_RV_tmp                                   = -24.6 + 13686. * (0.5* (np.interp(600,wl,Rrsm[i,:])+ np.interp(650,wl,Rrsm[i,:]))-np.interp(625,wl,Rrsm[i,:]))
        PC_RV                                       =np.append(PC_RV,[PC_RV_tmp])
        
        #Hunter et al. "Spectral discrimination of phytoplankton colour groups: The effect of suspended particulate matter and sensor spectral resolution" Remote Sensing of Environment 112 (2008) 1527–1544
        PC_H1_tmp                                   = (1./np.interp(630,wl,Rrs[i,:])- 1./np.interp(660,wl,Rrs[i,:]))*np.interp(750,wl,Rrs[i,:])
        PC_H1                                       =np.append(PC_H1,[PC_H1_tmp])  
       
        PC_H1b_tmp                                  =(1./np.interp(620,wl,Rrs[i,:])-1./np.interp(709,wl,Rrs[i,:]))*np.interp(753,wl,Rrs[i,:])
        PC_H1b                                      =np.append(PC_H1b,[PC_H1b_tmp])
        
       
        #Hunter et al. "Hyperspectral remote sensing of cyanobacterial pigments as indicators for cell populations and toxins in eutrophic lake" Remote Sensing of Environment 114 (2010) 2705–2718s
        PC_H3_tmp                                   =(1./np.interp(615,wl,Rrs[i,:])-1./np.interp(600,wl,Rrs[i,:]))*np.interp(725,wl,Rrs[i,:])
        PC_H3                                       =np.append(PC_H3,[PC_H3_tmp])
        
        
        #Wynne et al. "Characterizing a cyanobacterial bloom in western Lake Erie using satellite imagery and meteorological data" Limnol. Oceanogr. 55(5) (2010) 2025–2036
        PC_W_tmp                                    = np.interp(681,wl,Rrs[i,:])-np.interp(665,wl,Rrs[i,:])-(np.interp(709,wl,Rrs[i,:])-np.interp(665,wl,Rrs[i,:]))*((681-665)/(709-665))
        PC_W                                        =np.append(PC_W,[PC_W_tmp])
        
        #Li et al. "A semi-analytical algorithm for remote estimation of phycocyanin in inland waters" Science of the Total Environment 435-436 (2012) 141–150
        R31                                         =(1./np.interp(625,wl,Rrs[i,:])-1./np.interp(600,wl,Rrs[i,:]))*np.interp(725,wl,Rrs[i,:])
        
        R32                                         =(1./np.interp(625,wl,Rrs[i,:])-1./np.interp(650,wl,Rrs[i,:]))*np.interp(725,wl,Rrs[i,:])
        
        bb_725                                      =(1.489*np.interp(725,wl,Rrs[i,:])/(0.082-np.interp(725,wl,Rrs[i,:]))) 
        
        #a_pc624 = 0.5 * ((a_w725) + bb_725) * (R31 + R32) - 2*a_w624 + aw_600 + aw648
        a_pc624                                     = 0.5 * (1.489 + bb_725) * (R31 + R32) - 2*0.2834 + 0.2224 + 0.34       # Pope and Fry
        PC_L_tmp                                    = a_pc624/0.0024
        PC_L                                        =np.append(PC_L,[PC_L_tmp])
    
        #Mishra and Mishra "Normalized difference chlorophyll index: A novel model for remote estimation of chlorophyll-a concentration in turbid productive waters" RSE Volume 117, 15 February 2012, Pages 394-406
        #NCDI inverted (for correct representation *-1)
        NDCI_tmp                                    = (np.interp(665,wl,Rrs[i,:])-np.interp(708,wl,Rrs[i,:]))/(np.interp(665,wl,Rrs[i,:])+np.interp(708,wl,Rrs[i,:]))
        #NDCI_tmp                                    = (np.nanmean(Rrs[i,125:140])-np.nanmean(Rrs[i,145:155]))/(np.nanmean(Rrs[i,125:140])+np.nanmean(Rrs[i,145:155]))
        NDCI                                        = np.append(NDCI, [NDCI_tmp])
        Chla_NDCI_tmp                               = 14.039 + 86.115*NDCI_tmp + 194.325*NDCI_tmp**2
        Chla_NDCI                                   = np.append(Chla_NDCI,[Chla_NDCI_tmp])
        
        #GO8 
        #Mishra and Mishra "Normalized difference chlorophyll index: A novel model for remote estimation of chlorophyll-a concentration in turbid productive waters" RSE Volume 117, 15 February 2012, Pages 394-406
        bb_G08                                      = 1.61*np.interp(775,wl,Rrs[i,:])/(0.082-0.6*np.interp(775,wl,Rrs[i,:]))
        Chla_G08_tmp                                = ((np.interp(708,wl,Rrs[i,:])/np.interp(665,wl,Rrs[i,:]))*(0.70+bb_G08)-0.4-bb_G08**1.06)/0.016 
        Chla_G08                                    = np.append(Chla_G08,[Chla_G08_tmp])
        
        #Lunetta et al. "Evaluation of cyanobacteria cell count detection derived from MERIS imagery across the eastern USA" Remote Sensing of Environment 157 (2015) 24–34
        PC_Lu_tmp                                   = np.interp(665,wl,Rrs[i,:]) -np.interp(620,wl,Rrs[i,:])-(np.interp(681,wl,Rrs[i,:]) -np.interp(620,wl,Rrs[i,:]))*((665-620)/(681-620))      
        PC_Lu                                       = np.append(PC_Lu,[PC_Lu_tmp])        
        
        #Band Ratio Mishra, S.; Mishra, D.R.; Schluchter, W.M. A Novel Algorithm for Predicting Phycocyanin Concentrations in Cyanobacteria: A Proximal Hyperspectral Remote Sensing Approach. Remote Sens. 2009, 1
        PC_Br1_tmp                                  = np.interp(654,wl,Rrs[i,:])/np.interp(617,wl,Rrs[i,:])
        PC_Br1                                      = np.append(PC_Br1,[PC_Br1_tmp])
        PC_Br2_tmp                                  = np.interp(708,wl,Rrs[i,:])/np.interp(620,wl,Rrs[i,:]) # anche Hunter
        PC_Br2                                      = np.append(PC_Br2,[PC_Br2_tmp])
        PC_Br3_tmp                                  = np.interp(700,wl,Rrs[i,:])/np.interp(600,wl,Rrs[i,:])
        PC_Br3                                      = np.append(PC_Br3,[PC_Br3_tmp])
        
        #Chla OC4Me -  non accuratissima, c'è terra e vegetazione
        Rrs_max                                     = max(np.interp(443,wl,Rrs[i,:]),np.interp(490,wl,Rrs[i,:]),np.interp(510,wl,Rrs[i,:]))
        x                                           = math.log10(((Rrs_max)/np.interp(560,wl,Rrs[i,:])))
        chla_OC4Me_tmp                              = 10.**(0.3255 - 2.7677*x + 2.4409*x**2 - 1.12259*x**3 + 0.5683*x**4)
        chla_OC4Me                                  = np.append(chla_OC4Me,[chla_OC4Me_tmp])
        
      
        # Matthews, Bernard, Robertson, "An algorithm for detecting trophic status (chlorophyll-a), cyanobacterial-dominance, surface scums and floating vegetation in inland and coastal waters", RSE 124 2012 637-652
        # Pitarch, J., A. Ruiz-Verdu, M. D. Sendra, and R. Santoleri (2017), Evaluation and reformulation of the maximum peak height algorithm (MPH) and application in a hypertrophic lagoon, J. Geophys. Res. Oceans, 122, 1206–1221, doi:10.1002/2016JC012174
    
        SICF                                        = np.interp(681,wl,Rrs[i,:]) - np.interp(665,wl,Rrs[i,:]) - (np.interp(709,wl,Rrs[i,:]) - np.interp(665,wl,Rrs[i,:]))/(709 - 665)*(681 - 665)   
        SIPF                                        = np.interp(665,wl,Rrs[i,:]) - np.interp(620,wl,Rrs[i,:]) - (np.interp(681,wl,Rrs[i,:]) - np.interp(620,wl,Rrs[i,:]))/(681 - 620)*(665 - 620)   
        BAIR                                        = np.interp(709,wl,Rrs[i,:]) - np.interp(665,wl,Rrs[i,:]) - (np.interp(885,wl,Rrs[i,:]) - np.interp(665,wl,Rrs[i,:]))/(885 - 665)*(709 - 665)   
        PCI                                         = -(np.interp(620,wl,Rrs[i,:]) - np.interp(560,wl,Rrs[i,:]) - (np.interp(665,wl,Rrs[i,:]) - np.interp(560,wl,Rrs[i,:]))/(665 - 560)*(620 - 560))  # Pitarch
        
        if SICF < 0 and SIPF > 0 and BAIR > 0.002:
            RRS_MPH                                 = np.transpose(np.interp(681,wl,Rrs[i,:])),np.transpose(np.interp(709,wl,Rrs[i,:]))
            wl_MPH                                  = [681,709]
        else:
            RRS_MPH                                 = np.transpose(np.interp(681,wl,Rrs[i,:])),np.transpose(np.interp(709,wl,Rrs[i,:])),np.transpose(np.interp(753,wl,Rrs[i,:]))
            wl_MPH                                  = [681,709,753]
        pos_max                                     = np.where(RRS_MPH == np.amax(RRS_MPH))
        pos_max                                     = pos_max[0][0]
        MPH                                         = np.interp(wl_MPH[pos_max],wl,Rrs[i,:]) - np.interp(665,wl,Rrs[i,:]) - (np.interp(885,wl,Rrs[i,:]) - np.interp(665,wl,Rrs[i,:]))/(885 - 665)*(wl_MPH[pos_max] - 665)
                
        CHL_M_tmp                                   = 2.72 + 6903.13*MPH
        CHL_m                                       = np.append(CHL_m,CHL_M_tmp)
        CHL2D_M_tmp                                 = 37.18 + 11228.38*MPH #d de diatomeas
        CHL2D_m                                     = np.append(CHL2D_m,CHL2D_M_tmp)
        CHL2C_M_tmp                                 = 22.44*math.exp(35.79*MPH)# c de cianobacterias
        CHL2C_m                                     = np.append(CHL2C_m,CHL2C_M_tmp)
        CHL_P_tmp                                   = 848.468*MPH**3 - 72058.*MPH**2 + 5515.7*MPH 
        CHL_P                                       = np.append(CHL_P,CHL_P_tmp)
        CHL2_P_tmp                                  = 490.947*MPH**3 - 611074.*PCI*abs(PCI) + 3872.9*MPH
        CHL2_P                                      = np.append(CHL2_P,CHL2_P_tmp)
    var_data                                        = [PC_D, PC_SY, PC_S, PC_RV, PC_H1, PC_H1b, 
                 PC_H3, PC_W, PC_L, Chla_NDCI, Chla_G08, PC_Lu, 
                 PC_Br1, PC_Br2, PC_Br3, chla_OC4Me, CHL_m, CHL2D_m, 
                 CHL2C_m, CHL_P, CHL2_P, NDCI]
    return var_data, variables