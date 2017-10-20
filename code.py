#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 11:57:50 2017

@author: LouisGenieys
"""
# =============================================================================
import os
import pandas as pd
import pylab as plt
from datetime import datetime
import glob
import pickle
# =============================================================================

# On mettra par la suite les fonctions crees dans un fichier a part


def recup_fichiers(file_path=os.path.abspath(os.path.join(os.getcwd(),os.pardir))+"/sonobox/", methode = 0): 
    """ retourne tuple contenant la liste des noms des fichiers et la liste 
    des dates des fichiers dans le file_path donne
        * par default, file_path est le dossier contenant les csv qui se trouve dans le meme repertoire que le dossier contenant le code
        3 methodes differentes pour eviter les bugs :
        * methode = 0 : on utilise la methode os.listdir (defaut)
        * methode = 1 : on utilise la methode glob.glob 
        * methode = 2 : on utilise une methode dediee a Windows"""
    
    if methode == 0: liste_fichiers = [file_path+i for i in os.listdir(file_path)] ;   # liste des fichiers (et dossiers) presents dans le file_path
    
    elif methode == 1: liste_fichiers = glob.glob(file_path+"*.csv");
    
    elif methode == 2: print("A PROGRAMMER"); liste_fichiers = [];
    
    liste_dates = [datetime.strptime("20"+string.split("_")[2],"%Y%m%d").strftime("%Y-%m-%d") for string in os.listdir(file_path)] 
    # peut etre a changer en fct de la methode 
    # dans liste_dates se trouve la date obtenue pour chaque fichier
    # On met la date YYYYMMDD sous forme YYYY-MM-DD (pour pouvoir indexer en DateTime)

    return liste_fichiers,liste_dates


def conv_csv_dataframe(fichier,date):
    """ converti le fichier csv en DataFrame avec indexation sur la date+temps """
        
    data_frame = pd.read_csv(fichier, skiprows= 2, delimiter = ";", index_col = 0)
    # on aurait pu mettre en argument parse_dates=["Time"] mais on aurait eu la actuelle et pas la vraie date d enregistrement
        
    data_frame.index = pd.to_datetime(pd.Series([date for i in range(len(data_frame.index))]) + " " + pd.Series(data_frame.index)) 
    # ici on a mis l index du DataFrame sous la forme "YYYY-MM-DD HH:MM:SS" qui est un objet datetime
    
    return data_frame


def concat_dataframe(liste_fichiers,liste_dates):
    frames = [] # liste qui contiendra le DataFrame de chaque fichier       
    for i in range(len(liste_fichiers)): # on converti chaque fichier csv en un DataFrame   
        fichier = liste_fichiers[i]
        date = liste_dates[i]  
        data_frame = conv_csv_dataframe(fichier,date)
        frames.append(data_frame) 
    
    return pd.concat(frames) # on met "bout a bout" les DataFrame


def tracer(bande = "LAeq", grid=1):
    plt.figure()
    plt.plot(bigDT.index,bigDT[bande])
    plt.title("Bande "+bande)
    plt.xlabel("Temps (YYYY-MM-DD HH:MM:SS)")
    plt.ylabel("Niveau (dB)")
    plt.grid(grid)
    plt.show()
    
def moyenne_glissante(bande = "LAeq", frame = 100, grid=1):
    nom = "moyenne_mobile"+str(frame)+bande
    bigDT[nom]=bigDT[bande].rolling(window = frame).mean()
    ax1 = plt.subplot2grid((6,1),(0,0), rowspan=5, colspan=1)    
    ax1.plot(bigDT.index, bigDT[bande])
    ax1.plot(bigDT.index, bigDT[nom])
    plt.legend([bande,nom])
     
    plt.title(bande+" et sa moyenne mobile sur "+str(frame)+" secondes")
    plt.xlabel("Temps (YYYY-MM-DD HH:MM:SS)")
    plt.ylabel("Niveau (dB)")
    plt.grid(grid)
    plt.show()



# =============================================================================
#       MAIN
# =============================================================================

liste_fichiers,liste_dates = recup_fichiers()

bigDT = concat_dataframe(liste_fichiers,liste_dates) 
# attention il faut appeller le DT "bigDT" ou bien le rajouter comme variable dans les fonctions definies ci-dessus


# On trace LAeq en fonction du temps :

tracer()

# On trace la bande a 3.15kHz (la plus douloureuse aux oreilles) en fonction du temps :

tracer("3.15kHz")

# On trace la bande LAeq et sa courbe de moye


moyenne_glissante(frame=100)








