# -*- coding: utf-8 -*-
"""
Curso NetOPS 19-24 mayo 2025

@author: Gonzalo M.F. 
gmartinez@­icm.csic.es

"""
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator)

def rrs_plot(xeje,yeje,output_dir,save_name)->float:
    fig                     =plt.figure(figsize=(15,10))
    ax                      =fig.add_axes([0.1,0.1,0.8,0.8])
    ax.plot(xeje,yeje,color="black",label="Rrs")
    ax.set_xlabel("Wavelength (nm)", fontsize=18)
    ax.set_ylabel("Rrs (Sr-1)", fontsize=18)
    ax.tick_params(axis='both', labelsize=20) 
    ax.grid(True)
    plt.legend()
    fig.savefig(output_dir+save_name+".jpg",dpi=300)

def ndci_plot(xeje,yeje,std,ndci,output_dir,save_name,filtro)->float:
    fig                     =plt.figure(figsize=(15,10))
    ax                      =fig.add_axes([0.1,0.1,0.8,0.8])
    ax.plot(xeje,yeje,color="green",label="Chl-a")
    ax.plot(xeje,ndci,color="black",label="NDCI")
    ax.fill_between(xeje, yeje - std, yeje + std, color="lightgreen", alpha=0.2, label="Std chl-a")
    if filtro==True:
        ax.xaxis.set_major_locator(MultipleLocator(2))
    else:
        ax.xaxis.set_major_locator(MultipleLocator(31))
    for tick in ax.get_xticklabels():
        tick.set_rotation(45)
    ax.set_ylabel("NDCI", fontsize=18)
    ax.tick_params(axis='both', labelsize=20) 
    ax.grid(True)
    plt.legend()
    fig.savefig(output_dir+save_name+".jpg",dpi=300)

def pcu_plot(xeje,yeje,std,output_dir,save_name,filtro)->float:
    fig                     =plt.figure(figsize=(15,10))
    ax                      =fig.add_axes([0.1,0.1,0.8,0.8])
    ax.plot(xeje,yeje,color="blue",label="PC$^μ$")
    ax.fill_between(xeje, yeje - std, yeje + std, color="lightblue", alpha=0.2, label="Std PC$^μ$")
    if filtro==True:
        ax.xaxis.set_major_locator(MultipleLocator(2))
    else:
        ax.xaxis.set_major_locator(MultipleLocator(31))
    for tick in ax.get_xticklabels():
        tick.set_rotation(45)
    ax.set_ylabel("PC$^μ$", fontsize=18)
    ax.tick_params(axis='both', labelsize=20) 
    ax.grid(True)
    plt.legend()
    fig.savefig(output_dir+save_name+".jpg",dpi=300)