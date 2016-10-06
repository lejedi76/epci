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
import re
import unicodedata

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
    @sheetname : string, int, mixed list of strings/ints, or None ([0,1,âSheet5â])
    @header : header : int, list of ints
    @skiprows : list-like
    @skip_footer : int, default 0 Rows at the end to skip (0-indexed)
    @index_col : int, list of ints, default None
    @parse_cols : int or list or string, default None (âA:Eâ or âA,C,E:Fâ)

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
    except:
        return None

def to_percent(df):
    return df.apply(lambda c: c / c.sum() * 100, axis=0)


def add_value_label(ax, df, i):
    '''
    add a label on the value
    '''
    for k, label in enumerate(df.iloc[i]):
        ax.annotate(str(label), (k , label + 0.2), horizontalalignment='center')


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

    def __init__(self, filepath, kind, title, **kwargs):
        
        self.filepath = filepath
        self.kind = kind
        self.title = title
        
        #construct the dataframe
        self.df = self.dataframe(**kwargs)
        
        #default values
        self.erase_y_label = None
        self.annotate_value_label = None
        self._output_name = urlify(self.title)
        self.labels = self.df.columns.tolist()
        self.legend = False
        self.fontsize = 9
        self.figsize = cm2inch(13, 13)
        self.source = None

        self.plot_options = self.init_plot(self.kind, kwargs)     

        self.current_siren = None
        self.current_epci = None

        for key, value in kwargs.items():
            setattr(self, key, value)


    def dataframe(self, **kwargs):
        return read_file(self.filepath, **kwargs)

    def init_plot(self, kind, kwargs):
        '''
        Return dictionary of options according to the kind of plot
        '''
        if kind == 'pie':
            options = {
            'autopct' : '%1.1f%%',
            'startangle' : 180,
            'shadow' : True ,
            'labels' : self.labels}
        elif kind in ('bar', 'barh'):
            options = { 'width': 1, 
                        'stacked' : False}
        else:
            return None
        plot_options_from_kwargs = {k:v for k,v in kwargs.iteritems()
                    if k in options.keys()}
        options.update(plot_options_from_kwargs)
        return options

    def plot(self, i):
        df = self.df
        self.siren = find_siren(df, i)

        fig, ax = plt.subplots(figsize=self.figsize)

        df.iloc[i].plot(
            ax=ax,
            rot=0, 
            kind = self.kind, 
            title= self.title,
            legend=True,
            fontsize=9, 
            **self.plot_options)

        if self.erase_y_label:
            ax.set_ylabel(u'')

        if self.source:
            ax.set_xlabel(self.source)

        if self.annotate_value_label:
            add_value_label(ax, df, i)
        return fig   

    def save_plot(self, fig):
        try:
            fig_filepath = os.path.join(EPCI_SIREN_FOLDER, self.current_siren, self.output_name)
            fig.savefig('{}.{}'.format(fig_filepath, 'png'), dpi=300, format='png')
            fig.savefig('{}.{}'.format(fig_filepath, 'svg'), dpi=300, format='svg')
        except:
            pass
        finally:
            if fig:
                plt.close(fig)

    def plot_and_save_all(self):
        for i in range(len(df)):
            fig = plot(i, **self.plot_options)
            save_plot(fig)


        


filepath = os.path.join(DATA_FOLDER, '1_population_age.xls')

diagram_property = { 'filepath' : filepath,
                     'kind': 'pie',
                     'title': u'Population Âge',
                     'parse_cols' : 'A:B, C:H',
                     'index_col' : (0,1)              
                    }

dg = Diagram(**diagram_property)

# diagram(df, title, output_filename, figsize=cm2inch(13, 13), 
#     kind='bar', labels=None, rot=0, erase_y_label=False, 
#     source=None, annotate_label=False, **kwargs):
    
#     if labels is None:
#         labels = df.columns.tolist()

#     for i in range(len(df)):
#         fig, ax = plt.subplots(figsize=figsize)
#         # df.iloc[i,2:].plot(ax=ax,  kind=kind, rot=0, title=title, width=0.3)
#         df.iloc[i].plot(ax=ax, 
#             kind=kind, 
#             title=title, 
#             rot=rot,
#             labels=labels,
#              **kwargs)
        
#         if annotate_label:
#             add_value_label(ax, df, i)
#         try :
#             destination = os.path.join(epci_path, str(find_siren(df,i)))
#             if not os.path.isdir(destination):
#                 os.mkdir(destination)
#             fig_filepath = os.path.join(destination, output_filename)
#             if erase_y_label:
#                 ax.set_ylabel(u'')
#             #fig_filepath = destination
#             if source is not None:
#                 fig.text(0.1,0,u'Source : {}'.format(source), fontsize=8)
#             #fig.tight_layout()
#             fig.savefig('{}.{}'.format(fig_filepath, 'png'), dpi=300, format='png')
#             fig.savefig('{}.{}'.format(fig_filepath, 'svg'), dpi=300, format='svg')
#         except:
#             pass
#         finally:
#             plt.close(fig)
