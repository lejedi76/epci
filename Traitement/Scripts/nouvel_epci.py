# -*- coding: utf-8 -*-

FOLDER = os.path.join(DATA_FOLDER, 'Nouvel_EPCI')

#for filename in os.listdir(FOLDER):
#    filepath = os.path.join(FOLDER, filename)
#    diagram_property = {'filepath' : filepath,
#                    'kind': 'pie',
#                    'title': unicode(filename[:-4]),
#                    'parse_cols' : 'A:B, C:G',
#                    'index_col' : (0,1),
#                    'legend': False,
#                    'shadow': False,
#                    'erase_y_label': True,
#                    'figsize':cm2inch(13,13)
#                    }
#    dg = Diagram(**diagram_property)
#    dg.plot_and_save_all()
#

filepath = os.path.join(FOLDER, u'Pop par tranche d\'âge.xls')
filename = unicode(os.path.split(filepath)[1][:-4])
diagram_property = {'filepath' : filepath,
                'kind': 'pie',
                'title': unicode(filename),
                'parse_cols' : 'A:B, C:H',
                'index_col' : (0,1),
                'legend': True,
                'shadow': False,
                'erase_y_label': True,
                'figsize':cm2inch(13,13)
                }
dg = Diagram(**diagram_property)
fig = dg.plot(2)
dg.save_plot(fig, os.path.join(FOLDER,urlify(filename)))