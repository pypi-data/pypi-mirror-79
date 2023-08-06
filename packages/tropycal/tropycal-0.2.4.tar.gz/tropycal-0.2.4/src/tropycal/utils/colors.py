r"""Utility functions that are used across modules for colors.

Public utility functions should be added to documentation in the '/docs/_templates/overrides/tropycal.utils.rst' file."""

import os, sys
import numpy as np
import pandas as pd
from datetime import datetime as dt,timedelta
import requests
import urllib
import matplotlib.dates as mdates
import matplotlib.colors as mcolors
import matplotlib as mlib
import warnings

from .generic_utils import *

#===========================================================================================================
# Public utilities
# These are used internally and have use externally. Add these to documentation.
#===========================================================================================================

def get_colors_sshws(wind_speed):
    
    r"""
    Retrieve the default colors for the Saffir-Simpson Hurricane Wind Scale (SSHWS).
    
    Parameters
    ----------
    wind_speed : int or list
        Sustained wind speed in knots.
    
    Returns
    -------
    str
        Hex string for the corresponding color.
    """
    
    #If category string passed, convert to wind
    if isinstance(wind_speed,str) == True:
        wind_speed = category_label_to_wind(wind_speed)
    
    #Return default SSHWS category color scale
    if wind_speed < 5:
        return '#FFFFFF'
    elif wind_speed < 34:
        return '#8FC2F2' #'#7DB7ED'
    elif wind_speed < 64:
        return '#3185D3'
    elif wind_speed < 83:
        return '#FFFF00'
    elif wind_speed < 96:
        return '#FF9E00'
    elif wind_speed < 113:
        return '#DD0000'
    elif wind_speed < 137:
        return '#FF00FC'
    else:
        return '#8B0088'

def make_colormap(colors,whiten=0):
    
    z  = np.array(sorted(colors.keys()))
    n  = len(z)
    z1 = min(z)
    zn = max(z)
    x0 = (z - z1) / (zn - z1)
    
    CC = mcolors.ColorConverter()
    R = []
    G = []
    B = []
    for i in range(n):
        Ci = colors[z[i]]
        if type(Ci) == str:
            RGB = CC.to_rgb(Ci)
        else:
            RGB = Ci
        R.append(RGB[0] + (1-RGB[0])*whiten)
        G.append(RGB[1] + (1-RGB[1])*whiten)
        B.append(RGB[2] + (1-RGB[2])*whiten)
    
    cmap_dict = {}
    cmap_dict['red']   = [(x0[i],R[i],R[i]) for i in range(len(R))]
    cmap_dict['green'] = [(x0[i],G[i],G[i]) for i in range(len(G))]
    cmap_dict['blue']  = [(x0[i],B[i],B[i]) for i in range(len(B))]
    mymap = mcolors.LinearSegmentedColormap('mymap',cmap_dict)
    
    return mymap

def get_colors_ef(colormap='default'):
    
    r"""
    Retrieve a list of colors for the Enhanced Fujita (EF) tornado scale.
    
    Parameters
    ----------
    colormap : str or list
        Matplotlib colormap to use. Default is 'default', which uses Tropycal's default colors for the EF scale. If a list, this list must have 6 colors in order from EF0 to EF5.
    
    Returns
    -------
    list or cmap
        If used a matplotlib colormap, a cmap is returned, otherwise a list of colors is returned.
    """
    
    #Matplotlib colormap
    if isinstance(colormap,str) and colormap != 'default':
        try:
            cmap = mlib.cm.get_cmap(colormap)
            norm = mlib.colors.Normalize(vmin=0, vmax=5)
            colors = cmap(norm([0,1,2,3,4,5]))
        except:
            #colors = [colormap]*6
            raise ValueError('Colormap not found.')
    
    #User-passed list of colors
    elif isinstance(colormap,list):
        if len(colormap) == 6:
            colors = colormap
        else:
            raise ValueError('Must pass a list of 6 colors to correspond from EF0 to EF5.')
    
    #Otherwise, return default colors
    else:
        colors = ['lightsalmon','tomato','red','firebrick','darkred','purple']
    
    #Return list of colors, or colormap
    return colors

def get_colors_pph(plot_type,colormap,levels=None):
    
    r"""
    Retrieve a list of colors for Practically Perfect Hindcast (PPH) for tornadoes.
    
    Parameters
    ----------
    plot_type : str
        Plot type for PPH. Can be "daily" for single-day PPH, or "total" for multi-day PPH.
    colormap : str or list
        Matplotlib colormap to use. Default is 'spc', which uses Tropycal's default colors for the EF scale. If a list, this list must have 6 colors in order from EF0 to EF5.
    levels : list
        List of contour levels. Default is SPC intervals.
    
    Returns
    -------
    colors : list or cmap
        If used a matplotlib colormap, a cmap is returned, otherwise a list of colors is returned.
    levels : list
        List of contour levels.
    """
    
    #Insert default levels if none specified
    if levels is None: levels = [2,5,10,15,30,45,60,100]
    
    #Default SPC colormap
    if colormap == 'spc':
        
        #Daily plot type
        if plot_type == 'daily':
            levels = [2,5,10,15,30,45,60,100]
            colors = ['#008B00','#8B4726','#FFC800','#FF0000','#FF00FF','#912CEE','#104E8B']
        
        #Multi-day plot type
        else:
            warnings.warn('SPC colors only allowed for daily PPH.\n'+\
                          'Defaulting to plasma colormap.')
            colormap = 'plasma'
    
    #User-defined colormap
    if colormap != 'spc':
        
        #Matplotlib colormap
        if isinstance(colormap,str):
            cmap = mlib.cm.get_cmap(colormap)
            norm = mlib.colors.Normalize(vmin=0, vmax=len(levels)-2)
            colors = cmap(norm(np.arange(len(levels))))
        
        #User defined list of colors
        elif isinstance(colormap,list):
            colors = colormap
        
        #If a cmap is passed
        else:
            norm = mlib.colors.Normalize(vmin=0, vmax=len(levels)-2)
            colors = colormap(norm(np.arange(len(levels))))
    
    #Return colormap and values
    return colors, levels

#===========================================================================================================
# Private utilities
# These are primarily intended to be used internally. Do not add these to documentation.
#===========================================================================================================

def get_cmap_levels(varname,colormap,levels,linear=False):
    
    r"""
    Retrieve a list of colors for Practically Perfect Hindcast (PPH) for tornadoes.
    
    Parameters
    ----------
    varname : str
        if 'vmax', 'sfmr', or 'fl_to_sfc', then SSHWS category colors can be used.
    colormap : str or list
        Matplotlib colormap to use. Default is 'category', which uses Tropycal's default colors for the SSHWS scale. If a list, a colormap is generated from this list.
    levels : list
        List of contour levels. Default is SPC intervals.
    linear : bool
        If colormap is 'category', determine whether to generate a colorbar using linear category increments (True) or wind increments (False).
    
    Returns
    -------
    colors : cmap
        Matplotlib colormap object.
    levels : list
        List of contour levels.
    """
    
    #Default SSHWS colormap
    if colormap == 'category':
        
        #Ensure variable contains some element of surface wind
        if varname in ['vmax','sfmr','fl_to_sfc']:
            
            #Generate contour levels
            levels = [category_to_wind(c) for c in range(-1,6)]+[200]
            
            #Linear category increments
            if linear == True:
                colors = [mcolors.to_rgba(get_colors_sshws(lev)) \
                               for c,lev in enumerate(levels[:-1]) for _ in range(levels[c+1]-levels[c])]
            
            #Linear wind increments
            else:
                levels = [category_to_wind(c) for c in range(-1,6)]+[200]
                colors = [get_colors_sshws(lev) for lev in levels[:-1]]
                cmap = mcolors.ListedColormap(colors)
        
        #Otherwise, default to plasma colormap
        else:
            warnings.warn('Saffir Simpson category colors allowed only for surface winds')
            colormap = 'plasma'
    
    #Other colormap options
    if colormap != 'category':
        
        #Matplotlib colormap name
        if isinstance(colormap,str):
            cmap = mlib.cm.get_cmap(colormap)
        
        #User defined list of colors
        elif isinstance(colormap,list):
            cmap = mcolors.ListedColormap(colormap)
        
        #Dictionary
        elif isinstance(colormap,dict):
            cmap = make_colormap(colormap)
        
        #Otherwise, a cmap was passed
        else:
            cmap = colormap
        
        #Normalize colors relative to levels
        norm = mlib.colors.Normalize(vmin=0, vmax=len(levels)-1)
        
        #If more than 2 levels were passed, use those for the contour levels
        if len(levels) > 2:
            colors = cmap(norm(np.arange(len(levels)-1)))
            cmap = mcolors.ListedColormap(colors)
        
        #Otherwise, create a list of colors based on levels
        else:
            colors = cmap(norm(np.linspace(0,1,256)))
            cmap = mcolors.LinearSegmentedColormap.from_list('my_colormap',colors)
            
            y0 = min(levels)
            y1 = max(levels)
            dy = (y1-y0)/8
            scalemag = int(np.log(dy)/np.log(10))
            dy_scaled = dy*10**-scalemag
            dc = min([1,2,5,10], key=lambda x:abs(x-dy_scaled))
            dc = dc*10**scalemag
            c0 = np.ceil(y0/dc)*dc
            c1 = np.floor(y1/dc)*dc
            levels = np.arange(c0,c1+dc,dc)
    
            if scalemag > 0:
                levels = levels.astype(int)
    
    #Return colormap and levels
    return cmap, levels
