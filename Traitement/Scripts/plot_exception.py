# -*- coding: utf-8 -*-
"""
***************************************************************************
    plot_exception.py
    ---------------------
    Date                 : 2016-10-13 14:05:13
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
__date__ = '2016-10-13 08:55:06'
__copyright__ = '(C) 2016, ASTER'

from qgis.utils import iface
from qgis.gui import QgsMessageBar

class ExecutionException(Exception):
    def __init__(self, msg, details=None):
        super(ExecutionException, self).__init__()
        self.msg = msg
        self.details = details
        self.inform_user(msg, details)
    def inform_user(self, msg, details):
        iface.messageBar().pushMessage(msg, details, level=QgsMessageBar.CRITICAL)