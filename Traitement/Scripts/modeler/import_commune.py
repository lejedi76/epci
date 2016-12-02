##epci=group
##import_commune=name
##commune=vector
##nom=field commune
##insee=field commune
##population=optional field commune
param = """[{'expression': u'"%s"', 'length': 100, 'type': 10, 'name': u'nom', 'precision': 0} """ % (nom,)
param +=""", {'expression': u'"%s"', 'length': 10, 'type': 10, 'name': u'insee', 'precision': 0}"""% (insee,)
if population:
    param +=""", {'expression': u'"%s"', 'length': 10, 'type': 2, 'name': u'population', 'precision': 0}"""% (population,)
param +="]"
outputs_QGISREFACTORFIELDS_1=processing.runalg('qgis:refactorfields', commune, param
    , None)
outputs_QGISIMPORTINTOPOSTGIS_1=processing.runalg('qgis:importintopostgis', outputs_QGISREFACTORFIELDS_1['OUTPUT_LAYER'],2,'fiche','commune','id','geom',True,True,False,False)