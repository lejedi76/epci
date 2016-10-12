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
import textwrap

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
        self.output_name = self.title
        self.labels = ['\n'.join(textwrap.wrap(label.replace('\n',''),15))
                                         for label in self.df.columns.tolist()] 
        #legend = True => legend in plot
        #legend = False => legend outside the plot
        self.legend = False
        self.fontsize = 9
        self.figsize = cm2inch(13, 13)
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
        if self.kind == 'pie':
            options = {
            'autopct' : '%1.1f%%',
            'startangle' : 180,
            'shadow' : True }
            # if legend = True put the label in legend
        elif self.kind in ('bar', 'barh'):
            options = { 'width': 1, 
                        'stacked' : False}
        else:
            return None
        plot_options = {k:v for k,v in self.__dict__.iteritems()
                    if k in options.keys()}
        options.update(plot_options)

        if self.kind == 'pie':
            if self.legend:
                print self.legend
                options['labels']= self.labels
            else:
                options['labels']= None
        return options

    def plot(self, i):
        df = self.df
        self.current_siren = find_siren(df, i)

        fig, ax = plt.subplots(figsize=self.figsize)

        df.iloc[i].plot(
            ax=ax,
            rot=0, 
            kind = self.kind, 
            title= self.title,
            legend=True,
            fontsize=9, 
            **self.plot_options)

        if not self.legend:
            pass


        if self.erase_y_label:
            ax.set_ylabel(u'')

        if self.source:
            ax.set_xlabel(self.source)

        if self.annotate_value_label:
            add_value_label(ax, df, i)
        return fig

    def plot_legend(self, fig):
        fig_legend_list = []
        for ax_number, ax in enumerate(fig.get_axes()):
            fig_legend = plt.figure(figsize=cm2inch(4,4))
            patches, labels = ax.get_legend_handles_labels()
            #delete \n and customize the label legend
            #to have nice print
            labels_legend = ['\n'.join(textwrap.wrap(label.replace('\n',''),25))
                                         for label in labels]
            plt.figlegend(patches, labels_legend, loc = 'center')
            fig_legend_list.append(fig_legend)
        return fig_legend_list

    def save_plot_default(self, fig, is_legend_plot=False, suffix=None):
        ''' Save plot in default folder with appropriate name
        is_legend_plot : True means that only the legend
        is printed'''
        filepath = os.path.join(EPCI_SIREN_FOLDER, self.current_siren, self.output_name)
        if is_legend_plot:
            filepath = '{}_legend_{}'.format(filepath, suffix)
        self.save_plot(fig, filepath)


    def save_plot(self, fig, filepath, formats=('png', 'svg')):
        try:
            #fig_filepath = os.path.join(EPCI_SIREN_FOLDER, self.current_siren, self.output_name)
            for format in formats:
                fig.savefig('{}.{}'.format(filepath, format), dpi=300, format=format)
        except Exception as e:
            raise ExecutionException(str(e))
        finally:
            if fig:
                plt.close(fig)

    def plot_and_save_all(self):
        df = self.df
        for i in range(len(df)):
            fig = self.plot(i)
            self.save_plot_default(fig)
            if not self.legend:
                #print the legend of all potential axes in separate files
                fig_legend_list = self.plot_legend(fig)
                for n, fig_legend in enumerate(fig_legend_list):
                    self.save_plot_default(fig_legend, is_legend_plot=True, suffix=n)


def plot(df, dg):
    self = dg
    fig, ax = plt.subplots(figsize=self.figsize)
    df.plot(
    ax=ax,
    rot=0, 
    kind = self.kind, 
    title= self.title,
    legend=False,
    fontsize=9, 
    **self.plot_options)




filepath = os.path.join(DATA_FOLDER, '3_Emploi_au_LT_par_NA.xls')

diagram_property = { 'filepath' : filepath,
                     'kind': 'pie',
                     'title': u"Répartition des emplois \npar secteur d'activité",
                     'parse_cols' : 'A:B, C:G',
                     'index_col' : (0,1),
                     # 'labels' : [u'Administration \npublique, \nenseignement, \nsanté humaine \net action sociale ', 
                     #            u'Agriculture, \nsylviculture \net pêche ', 
                     #            u'Commerce, \ntransports \net services \ndivers ', 
                     #            u'Construction', 
                     #            u'Industrie  \nmanufacturière, \nindustries \nextractives \net autres '],
                    'legend': True,
                    'shadow': False
                    }

dg = Diagram(**diagram_property)

#liste = [ '\n'.join(textwrap(label.replace('\n',''),25)) for label in ax.get_legend_handles_labels()[1]]
#plt.figlegend(*ax.get_legend_handles_labels(), loc = 'center')