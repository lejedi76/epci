# -*- coding: utf-8 -*-
"""
***************************************************************************
    generede_diagram.py
    ---------------------
    Date                 : 2016-11-18 09:01:18
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
__date__ = '2016-11-18 09:01:18'
__copyright__ = '(C) 2016, ASTER'

import os
from plot_epci import *
from plot_exception import *
from config_path import DATA_FOLDER

filepath = os.path.join(DATA_FOLDER, '1_denombrement_pop.xls')

diagram_property = {'filepath' : filepath,
                    'kind': 'line',
                    'figsize': cm2inch(13,6),
                    'title': u"Évolution de la population",
                    'parse_cols' : 'A:B, C:G',
                    'index_col' : (0,1),
                    'erase_y_label': True
                    }

dg = Diagram(**diagram_property)
dg.plot_and_save_all()



# Répartition secteur d'activité
filepath = os.path.join(DATA_FOLDER, '3_Emploi_au_LT_par_NA.xls')

diagram_property = {'filepath' : filepath,
                    'kind': 'pie',
                    'title': u"Répartition des emplois \npar secteur d'activité",
                    'parse_cols' : 'A:B, C:G',
                    'index_col' : (0,1),
                    'legend': False,
                    'shadow': False,
                    'erase_y_label': True,
                    }

dg = Diagram(**diagram_property)
dg.plot_and_save_all()

