##0_import_epci=name
##nom=field epci
##siren=field epci
##epci=vector
outputs_QGISREFACTORFIELDS_1=processing.runalg('qgis:refactorfields', epci,'[{'expression': u'"ID_TERRAIN_GV"', 'length': 7, 'type': 2, 'name': u'ID_TERRAIN_GV', 'precision': 0}, {'expression': u'"NB_PLACE_CARAVANE"', 'length': 0, 'type': 2, 'name': u'NB_PLACE_CARAVANE', 'precision': 0}, {'expression': u'"DATE_FINANCEMENT"', 'length': 10, 'type': 14, 'name': u'DATE_FINANCEMENT', 'precision': 0}]',None)
outputs_QGISIMPORTINTOPOSTGIS_1=processing.runalg('qgis:importintopostgis', outputs_QGISREFACTORFIELDS_1['OUTPUT_LAYER'],2,'epci','epci','id','geom',True,True,False,False)