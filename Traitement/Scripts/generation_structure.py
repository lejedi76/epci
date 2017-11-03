# -*- coding: utf-8 -*-
"""
***************************************************************************
    generation_structure.py
    ---------------------
    Date                 : 2016-05-20 08:55:06
    Copyright            : (C) 2016 by ASTER
    Email                : ddtm-sctsrd-aster@eure.gouv.fr
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'ASTER'
__date__ = '2016-08-20 08:55:06'
__copyright__ = '(C) 2016, ASTER'
    
import os
import shutil
# import win32com.client

from config_path import *

# ROOT_FOLDER = ur'U:\Patrimoine_commun\ETUDES\1_fiches_territoriales_EPCI\Traitement'
# EPCI_FOLDER = os.path.join(ROOT_FOLDER, 'EPCI')
# EPCI_NAME_FOLDER = os.path.join(EPCI_FOLDER, 'EPCI_Nom')
# EPCI_SIREN_FOLDER = os.path.join(EPCI_FOLDER, 'EPCI_Siren')
# EXPORT_FOLDER = os.path.join(ROOT_FOLDER, 'Export')
# PROJECT_FOLDER = os.path.join(ROOT_FOLDER, 'Projet_Qgis')
#######################
# ETUDES
#   1_fiches_territoriales_EPCI
#       Extraction_donnees
#       Navettes_dom_travail
#       Traitement
#           EPCI
#               EPCI_Nom (lien symbolique)
#               EPCI_Siren
#           Export
#           Projet_Qgis
#           Scripts
#######################


def symlink(src, target):
    ''' os.symlink for linux
        win32file.CreateSymbolicLink(folder_nom, folder_siren, 1) not working on server
        create shortcut (.lnk)

    '''
    ws = win32com.client.Dispatch("wscript.shell")
    shortcut = ws.CreateShortCut(src + '.lnk')
    shortcut.Targetpath=target
    shortcut.save()


folders = [ROOT_FOLDER, EPCI_FOLDER, 
            EPCI_NAME_FOLDER, EPCI_SIREN_FOLDER, 
            EXPORT_FOLDER, PROJECT_FOLDER]

try:
    shutil.rmtree(EPCI_NAME_FOLDER)
except:
    pass

for folder in folders:
    if os.path.isdir(folder):
        continue
    os.mkdir(folder)

layer = iface.activeLayer()

for feat in layer.getFeatures():
    folder_siren = os.path.join(EPCI_FOLDER,'EPCI_Siren',feat['ID_EPCI'])
    try:
        os.mkdir(folder_siren)
    except:
        pass
    finally:
        folder_nom = os.path.join(EPCI_FOLDER,'EPCI_Nom',feat['F_epci'])
        #os.mkdir(folder_nom)
        symlink(folder_nom, folder_siren)
        #os.symlink(folder_nom, folder_siren)
        #win32file.CreateSymbolicLink(folder_nom, folder_siren, 1)


