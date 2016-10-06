# -*- coding: utf-8 -*-
"""
***************************************************************************
    configuration_path.py
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
__date__ = '2016-05-20 08:55:06'
__copyright__ = '(C) 2016, ASTER'

import os
#path settings
SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))
ROOT_FOLDER = os.path.dirname(os.path.dirname(SCRIPT_FOLDER))
DATA_FOLDER = os.path.join(ROOT_FOLDER, 'Extraction_donnees')
PROCESSING_FOLDER = os.path.join(ROOT_FOLDER, 'Traitement')
EPCI_FOLDER = os.path.join(PROCESSING_FOLDER, 'EPCI')
EPCI_NAME_FOLDER = os.path.join(PROCESSING_FOLDER, 'EPCI_Nom')
EPCI_SIREN_FOLDER = os.path.join(PROCESSING_FOLDER, 'EPCI_Siren')
EXPORT_FOLDER = os.path.join(PROCESSING_FOLDER, 'Export')
PROJECT_FOLDER = os.path.join(PROCESSING_FOLDER, 'Projet_Qgis')
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