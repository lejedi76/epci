##epci=group
##import_epci=name
##epci=vector
##nom=field epci
##siren=field epci
outputs_QGISREFACTORFIELDS_1=processing.runalg('qgis:refactorfields', epci,
    """[{'expression': u'"%s"', 'length': 100, 'type': 10, 'name': u'nom', 'precision': 0}, {'expression': u'"%s"', 'length': 10, 'type': 10, 'name': u'siren', 'precision': 0}]"""% (nom,siren), None)
outputs_QGISIMPORTINTOPOSTGIS_1=processing.runalg('qgis:importintopostgis', outputs_QGISREFACTORFIELDS_1['OUTPUT_LAYER'],2,'fiche','epci','id','geom',True,True,False,False)