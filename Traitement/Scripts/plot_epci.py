# -*- coding: utf-8 -*-
"""
***************************************************************************
    plot_epci.py
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
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import re
import unicodedata
import textwrap

from qgis.utils import iface
from qgis.gui import QgsMessageBar

#path settings
from config_path import (
    SCRIPT_FOLDER,
    ROOT_FOLDER,
    PROCESSING_FOLDER,
    DATA_FOLDER,
    EPCI_FOLDER,
    EPCI_NAME_FOLDER,
    EPCI_SIREN_FOLDER,
    EXPORT_FOLDER,
    PROJECT_FOLDER)

from plot_exception import ExecutionException

#matplotlib settings
style = 'ggplot'
stylepath = os.path.join(SCRIPT_FOLDER,'site-packages', 'matplotlib', 'mpl-data', 'stylelib', style)
stylefile = stylepath + '.mplstyle'
print stylefile
matplotlib.style.use(stylefile)

#usefull functons
def urlify(s):
    # Remove all accent
    s = unicodedata.normalize('NFKD', unicode(s)).encode('ASCII', 'ignore')
    # Remove all non-word characters (everything except numbers and letters)
    s = re.sub(r"[^\w\s]", '', s)
    # Replace all runs of whitespace with a single dash
    s = re.sub(r"\s+", '-', s)
    return s


def cm2inch(*tupl):
    inch = 2.54
    if isinstance(tupl[0], tuple):
        return tuple(i/inch for i in tupl[0])
    else:
        return tuple(i/inch for i in tupl)

def read_file(filepath, 
        sheetname = 0,
        header = 0,
        skiprows=None, 
        skip_footer=0, 
        index_col=None,
        parse_cols=None,
        **kwargs):
    '''
    http://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_excel.html

    @filepath : string, path object
    @sheetname : string, int, mixed list of strings/ints, or None ([0,1,Sheet5])
    @header : header : int, list of ints
    @skiprows : list-like
    @skip_footer : int, default 0 Rows at the end to skip (0-indexed)
    @index_col : int, list of ints, default None
    @parse_cols : int or list or string, default None (A:E or A,C,E:F)

    return dataframe
    '''
    df = pd.read_excel(filepath, 
        sheetname=sheetname, 
        header=header, 
        skiprows=skiprows, 
        skip_footer=skip_footer,
        index_col=index_col, 
        parse_cols=parse_cols,
        **kwargs)

    return df

def find_siren(df, i):
    '''
    scan columns to extract the siren number
    @df : dataframe
    @i : row
    '''

    try:
        index = df.index.tolist()[i]
        match = re.match('(.*)([1-2]{1}[0-9]{8})(.*)',str(index))
        if match:
            return match.group(2)
        #multi-index
        for sub_index in index:
                match = re.match('(.*)([1-2]{1}[0-9]{8})(.*)',str(sub_index))
                if match:
                    return match.group(2)
                    
        for column in df.columns.tolist():
            match = re.match('(.*)([1-2]{1}[0-9]{8})(.*)',str(df[column].iloc[i]))
            if match:
                return match.group(2)
    except Exception as e:
        raise ExecutionException(str(e))

#cleanup and format label
def wrap(label, size):
    return '\n'.join(textwrap.wrap(label.replace('\n',' '),size)).strip()

def to_percent(df):
    return df.apply(lambda c: c / c.sum() * 100, axis=0)


def add_value_label(ax, df, i):
    '''
    add a label on the value
    http://composition.al/blog/2015/11/29/a-better-way-to-add-labels-to-bar-charts-with-matplotlib/
    '''
    # Get y-axis height to calculate label position from.
    (y_bottom, y_top) = ax.get_ylim()
    y_height = y_top - y_bottom

    for k, height in enumerate(df.iloc[i]):
        ax.annotate(str(height), (k , height+ y_height*0.02),
             size=10,
             path_effects=[pe.withStroke(linewidth=2, foreground="white")],
            #bbox=dict(boxstyle='round,pad=0.2', fc='yellow', alpha=0.3),
            horizontalalignment='center')


class Diagram(object):
    '''
    Diagram class
    
    Mandatory arguments :
    @filepath : xls filepath
    @kind : 'bar', 'pie'...
    @title : diagram title
    
    Optional arguments :
    @output_name : filename of the output
    @labels : diagram labels
    @kwargs : all options available with matplotlib
    '''

    @property
    def output_name(self):
        return self._output_name
    
    @output_name.setter
    def output_name(self, output_name):
        self._output_name = urlify(output_name)

    @property
    def labels(self):
        return self._labels

    @labels.setter
    def labels(self, labels):
        self._labels = [wrap(label, 15) for label in labels]

    def __init__(self, filepath, kind, title, **kwargs):
        
        self.filepath = filepath
        self.kind = kind
        self.title = title.upper()
        
        #construct the dataframe
        self.df = self.dataframe(**kwargs)
        
        #default values
        self.erase_y_label = True
        self.annotate_value_label = False
        self.rot = 0
        self.output_name = self.title
        self.labels = self.df.columns.tolist()
        #legend = True => legend in plot
        #legend = False => legend outside the plot
        self.legend = False
        self.fontsize = 9
        self.figsize = cm2inch(14, 14)
        self.source = None

             

        self.current_siren = None
        self.current_epci = None

        for key, value in kwargs.items():
            setattr(self, key, value)


        self.labels_legend = None
        self.plot_options = self.get_plot_options()


    def dataframe(self, **kwargs):
        return read_file(self.filepath, **kwargs)

    def get_plot_options(self):
        '''
        Return dictionary of options according to the kind of plot
        '''
        if self.kind == 'line':
            options = {'linewidth': 4, 'marker': 'o' , 'markersize' : 10}
        elif self.kind == 'pie':
            options = {
            'autopct' : '%1.1f%%',
            'startangle' : 180,
            'shadow' : False }
            # if legend = True put the label in legend
        elif self.kind in ('bar', 'barh'):
            options = { 'width': 0.3, 
                        'stacked' : False}
        else:
            return None
        plot_options = {k:v for k,v in self.__dict__.iteritems()
                    if k in options.keys()}
        options.update(plot_options)

        if self.kind == 'pie':
            if self.annotate_value_label:
                options['labels']= self.labels
            else:
                options['labels']=['' for columns in self.df.columns.tolist()]

        return options

    def plot(self, i):
        df = self.df
        self.current_siren = find_siren(df, i)

        if self.current_siren is None:
            return None

        fig, ax = plt.subplots(figsize=self.figsize)
        # plt.subplots_adjust(top=0.85)

        #stest if stacked options is True
        #transform the pandas series to dataframe
        has_stacked = self.plot_options.get('stacked', False)
        if not has_stacked:
            df.iloc[i].plot(
                ax=ax,
                rot=self.rot, 
                kind = self.kind, 
                title= self.title,
                legend=True,
                fontsize=9, 
                **self.plot_options)
        else:
            df.iloc[i:i+1].plot(
                ax=ax,
                rot=self.rot, 
                kind = self.kind, 
                title= self.title,
                legend=True,
                fontsize=9, 
                **self.plot_options)

        #legend must be create otherwise
        #legend can not be create in separate file
        if not self.legend:
            for axes in fig.get_axes():
                legend = axes.get_legend()
                legend.set_visible(False)

        # plt.gca().set_xlim(left=-1)
        # ylim = max(df.iloc[i]) + (max(df.iloc[i])-min(df.iloc[i]))*0.1
        # plt.gca().set_ylim(top=ylim)


        if self.erase_y_label:
            ax.set_ylabel(u'')

        if self.source:
            ax.set_xlabel(self.source)

        if self.annotate_value_label and self.kind <> 'pie':
            add_value_label(ax, df, i)
        return fig

    def plot_legend(self, fig):
        fig_legend_list = []
        for ax_number, ax in enumerate(fig.get_axes()):
            fig_legend = plt.figure(figsize=cm2inch(5,5))
            patches, labels = ax.get_legend_handles_labels()
            #delete \n and customize the label legend
            #to have nice print
            labels_legend = [ wrap(label, 25) for label in labels]
            plt.figlegend(patches, labels_legend, loc = 'center')
            fig_legend_list.append(fig_legend)
        return fig_legend_list

    def save_plot_default(self, fig, is_legend_plot=False, suffix=None):
        ''' Save plot in default folder with appropriate name
        is_legend_plot : True means that only the legend
        is printed'''
        filepath = os.path.join(EPCI_SIREN_FOLDER, self.current_siren, self.output_name)
        print filepath
        if is_legend_plot:
            filepath = '{}_legend_{}'.format(filepath, suffix)
        self.save_plot(fig, filepath)


    def save_plot(self, fig, filepath, formats=('png', 'svg')):
        try:
            #fig_filepath = os.path.join(EPCI_SIREN_FOLDER, self.current_siren, self.output_name)
            for format in formats:
                #fig.tight_layout()
                fig.savefig('{}.{}'.format(filepath, format), dpi=300, format=format)
                print 'save'
        except Exception as e:
            iface.messageBar().pushMessage('erreur', str(e), level=QgsMessageBar.CRITICAL)
        finally:
            if fig:
                plt.close(fig)

    def plot_and_save_all(self):
        df = self.df
        for i in range(len(df)):
            fig = self.plot(i)
            if fig is None:
                return None
            self.save_plot_default(fig)
            if not self.legend:
                #print the legend of all potential axes in separate files
                fig_legend_list = self.plot_legend(fig)
                for n, fig_legend in enumerate(fig_legend_list):
                    self.save_plot_default(fig_legend, is_legend_plot=True, suffix=n)

#emploi
filepath = os.path.join(DATA_FOLDER, '3_Emploi_au_LT_par_NA.xls')

diagram_property = {'filepath' : filepath,
                    'kind': 'pie',
                    'title': u"Répartition des emplois \npar secteur d'activité",
                    'parse_cols' : 'A:B, C:G',
                    'index_col' : (0,1),
                    'legend': False,
                    'shadow': False,
                    'erase_y_label': True,
                    'figsize':cm2inch(15,15)
                    }

dg = Diagram(**diagram_property)
# dg.plot_and_save_all()

# #évolution population
# filepath = os.path.join(DATA_FOLDER, '1_denombrement_pop.xls')

# diagram_property = {'filepath' : filepath,
#                     'kind': 'line',
#                     'figsize': cm2inch(13,6),
#                     'title': u"Évolution de la population",
#                     'parse_cols' : 'A:B, C:G',
#                     'index_col' : (0,1),
#                     'erase_y_label': True
#                     }

# dg = Diagram(**diagram_property)
# dg.plot_and_save_all()

# # répartition age
# filepath = os.path.join(DATA_FOLDER, '1_population_age.xls')

# diagram_property = {'filepath' : filepath,
#                     'kind': 'bar',
#                     'title': u"Répartition de l'âge",
#                     'parse_cols' : 'A:B, C:H',
#                     'index_col' : (0,1),
#                     'erase_y_label': True,
#                     'stacked':True,
#                     'annotate_value_label': False,
#                     'figsize':cm2inch(12,14),
#                     'width' : 0.1
#                     }

# dg = Diagram(**diagram_property)
# dg.plot_and_save_all()
#liste = [ '\n'.join(textwrap(label.replace('\n',''),25)) for label in ax.get_legend_handles_labels()[1]]
#plt.figlegend(*ax.get_legend_handles_labels(), loc = 'center')
