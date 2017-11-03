# -*- coding: utf-8 -*-

FOLDER = os.path.join(DATA_FOLDER, 'Nouvel_EPCI')

filepath = os.path.join(FOLDER, u"1-Évolution_de_la_population.xls")
filename = unicode(os.path.split(filepath)[1][2:-4]).replace('_', ' ')
diagram_property = {'filepath' : filepath,
                'kind': 'line',
                'title': filename,
                'parse_cols' : 'A:B, C:G',
                'index_col' : (0,1),
                'legend': False,
                'annotate_value_label':True,
                'shadow': False,
                'erase_y_label': True,
                'figsize':cm2inch(14,8)
                }
dg = Diagram(**diagram_property)
#dg.plot_and_save_all()

filepath = os.path.join(FOLDER, u"1-Mégages_composition_taille moyenne_ménages.xls")
filename = unicode(os.path.split(filepath)[1][2:-4]).replace('_', ' ')
diagram_property = {'filepath' : filepath,
                'kind': 'pie',
                'title': u'Composition des ménages',
                'parse_cols' : 'A:B, C:H',
                'index_col' : (0,1),
                'legend': False,
                'annotate_value_label': True,
                'shadow': False,
                'erase_y_label': True,
                'figsize':cm2inch(14,14)
                }
dg = Diagram(**diagram_property)
#dg.plot_and_save_all()

filepath = os.path.join(FOLDER, u"1-Population_tranches_âges.xls")
filename = unicode(os.path.split(filepath)[1][2:-4]).replace('_', ' ')
diagram_property = {'filepath' : filepath,
                'kind': 'pie',
                'title': filename,
                'parse_cols' : 'A:B, C:H',
                'index_col' : (0,1),
                'legend': False,
                'annotate_value_label': True,
                'shadow': False,
                'erase_y_label': True,
                'figsize':cm2inch(14,14)
                }
dg = Diagram(**diagram_property)
#dg.plot_and_save_all()

filepath = os.path.join(FOLDER, u"3-Emploi_au _lieu travail_par secteur activité.xls")
filename = unicode(os.path.split(filepath)[1][2:-4]).replace('_', ' ')
diagram_property = {'filepath' : filepath,
                'kind': 'pie',
                'title': u"Emploi par secteur d'activité",
                'parse_cols' : 'A:B, C:G',
                'index_col' : (0,1),
                'legend': False,
                'annotate_value_label': True,
                'shadow': False,
                'erase_y_label': True,
                'figsize':cm2inch(14,14)
                }
dg = Diagram(**diagram_property)
#dg.plot_and_save_all()


filepath = os.path.join(FOLDER, u"3-Pop._active_total_repartition.xls")
filename = unicode(os.path.split(filepath)[1][2:-4]).replace('_', ' ')
diagram_property = {'filepath' : filepath,
                'kind': 'pie',
                'title': u"Répartition de la population active",
                'parse_cols' : 'A:B, C:H',
                'index_col' : (0,1),
                'legend': False,
                'annotate_value_label': True,
                'shadow': False,
                'erase_y_label': True,
                'figsize':cm2inch(14,14),
                'startangle': 60
                }
dg = Diagram(**diagram_property)
#dg.plot_and_save_all()
#
filepath = os.path.join(FOLDER, u"3-Pop_de_plus_de 15ans_par_csp.xls")
filename = unicode(os.path.split(filepath)[1][2:-4]).replace('_', ' ')
diagram_property = {'filepath' : filepath,
                'kind': 'pie',
                'title': u"Répartition de la population active (15 ans et +)\n par catégorie socio-professionnelle",
                'parse_cols' : 'A:B, C:J',
                'index_col' : (0,1),
                'legend': False,
                'annotate_value_label': True,
                'shadow': False,
                'erase_y_label': True,
                'figsize':cm2inch(14,14),
                'startangle': 20
                }
dg = Diagram(**diagram_property)
#dg.plot_and_save_all()
#
filepath = os.path.join(FOLDER, u"3-Pop_diplômes.xls")
filename = unicode(os.path.split(filepath)[1][2:-4]).replace('_', ' ')
diagram_property = {'filepath' : filepath,
                'kind': 'pie',
                'title': u"Niveau d'études de la population",
                'parse_cols' : 'A:B, C:F',
                'index_col' : (0,1),
                'legend': False,
                'annotate_value_label': True,
                'shadow': False,
                'erase_y_label': True,
                'figsize':cm2inch(14,14),
                'startangle': 0
                }
dg = Diagram(**diagram_property)
#dg.plot_and_save_all()
#
filepath = os.path.join(FOLDER, u"4-Catégorie de logements.xls")
filename = unicode(os.path.split(filepath)[1][2:-4]).replace('_', ' ')
diagram_property = {'filepath' : filepath,
                'kind': 'pie',
                'title': u"Catégorie de logements",
                'parse_cols' : 'A:B, C:E',
                'index_col' : (0,1),
                'legend': False,
                'annotate_value_label': True,
                'shadow': False,
                'erase_y_label': True,
                'figsize':cm2inch(14,14),
                'startangle': 20
                }
dg = Diagram(**diagram_property)
#dg.plot_and_save_all()

filepath = os.path.join(FOLDER, u"4-Const_logts_autorisés.xls")
filename = unicode(os.path.split(filepath)[1][2:-4]).replace('_', ' ')
diagram_property = {'filepath' : filepath,
                'kind': 'line',
                'title': u"Construction de logements autorisés",
                'parse_cols' : 'A:B, C:L',
                'index_col' : (0,1),
                'legend': False,
                'annotate_value_label': True,
                'shadow': False,
                'erase_y_label': True,
                'figsize':cm2inch(14,7),
                'startangle': 20
                }
dg = Diagram(**diagram_property)
#dg.plot_and_save_all()

filepath = os.path.join(FOLDER, u"4-Log_parc_rpls.xls")
filename = unicode(os.path.split(filepath)[1][2:-4]).replace('_', ' ')
diagram_property = {'filepath' : filepath,
                'kind': 'pie',
                'title': u"Répartition des logements (RPLS)",
                'parse_cols' : 'A:B, C:F',
                'index_col' : (0,1),
                'legend': False,
                'annotate_value_label': True,
                'shadow': False,
                'erase_y_label': True,
                'figsize':cm2inch(14,14),
                'startangle': 20
                }
dg = Diagram(**diagram_property)
#dg.plot_and_save_all()
#
filepath = os.path.join(FOLDER, u"4-Log_taille.xls")
filename = unicode(os.path.split(filepath)[1][2:-4]).replace('_', ' ')
diagram_property = {'filepath' : filepath,
                'kind': 'pie',
                'title': u"Taille des logements",
                'parse_cols' : 'A:B, C:H',
                'index_col' : (0,1),
                'legend': False,
                'annotate_value_label': True,
                'shadow': False,
                'erase_y_label': True,
                'figsize':cm2inch(14,14),
                'startangle': 20
                }
dg = Diagram(**diagram_property)
dg.plot_and_save_all()
