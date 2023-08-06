r"""Functionality for storing and analyzing a year/season of cyclones."""

import calendar
import numpy as np
import pandas as pd
import re
import scipy.interpolate as interp
import urllib
import warnings
from datetime import datetime as dt,timedelta

from .plot import TrackPlot
from .storm import Storm

#Import tools
from .tools import *
from ..utils import *
    
class Season:
    
    r"""
    Initializes an instance of Season, retrieved via ``TrackDataset.get_season()``.

    Parameters
    ----------
    season : dict
        Dict entry containing all storms within the requested season.
    info : dict
        Dict entry containing general information about the season.

    Returns
    -------
    Season
        Instance of a Season object.
    """
    
    def __setitem__(self, key, value):
        self.__dict__[key] = value
        
    def __getitem__(self, key):
        return self.__dict__[key]
   
    def __add__(self, new):
        #Add seasons
        
        #Ensure data sources and basins are the same
        if self.source_basin != new.source_basin:
            msg = 'Seasons can only be added for the same basin.'
            raise ValueError(msg)
        if self.source != new.source:
            msg = 'Seasons can only be added from the same source.'
            raise ValueError(msg)
        if self.source == 'ibtracs':
            msg = 'Only hurdat data sources are currently supported for this functionality.'
            raise RuntimeError(msg)
        
        #Retrieve old & new dict entries
        dict_original = self.dict.copy()
        dict_new = new.dict.copy()
        
        #Retrieve copy of coordinates
        new_coords = self.coords.copy()
        
        #Add year to list of years
        if isinstance(self.coords['year'],int) == True:
            new_coords['year'] = [self.year,new.year]
        else:
            new_coords['year'].append(new.year)
        
        #Sort list of years
        new_coords['year'] = (np.sort(new_coords['year'])).tolist()
        
        #Update dict
        dict_original.update(dict_new)
        
        #Iterate over every year to create a new dict
        new_dict = {}
        for year in new_coords['year']:
            for key in dict_original.keys():
                if int(key[-4:]) == year:
                    new_dict[key] = dict_original[key]
        
        #Return new Season object
        return Season(new_dict,new_coords)
    
    def __repr__(self):
         
        #Label object
        summary = ["<tropycal.tracks.Season>"]
        
        #Format keys for summary
        season_summary = self.summary()
        summary_keys = {'Total Storms':season_summary['season_storms'],
                        'Named Storms':season_summary['season_named'],
                        'Hurricanes':season_summary['season_hurricane'],
                        'Major Hurricanes':season_summary['season_major'],
                        'Season ACE':season_summary['season_ace']}

        #Add season summary
        summary.append("Season Summary:")
        add_space = np.max([len(key) for key in summary_keys.keys()])+3
        for key in summary_keys.keys():
            key_name = key+":"
            #val = '%0.1f'%(summary_keys[key]) if key == 'Season ACE' else summary_keys[key]
            #summary.append(f'{" "*4}{key_name:<{add_space}}{val}')
            summary.append(f'{" "*4}{key_name:<{add_space}}{summary_keys[key]}')
        
        #Add additional information
        summary.append("\nMore Information:")
        add_space = np.max([len(key) for key in self.coords.keys()])+3
        for key in self.coords.keys():
            key_name = key+":"
            #val = '%0.1f'%(self.coords[key]) if key == 'ace' else self.coords[key]
            #summary.append(f'{" "*4}{key_name:<{add_space}}{val}')
            summary.append(f'{" "*4}{key_name:<{add_space}}{self.coords[key]}')

        return "\n".join(summary)
    
    def __init__(self,season,info):
        
        #Save the dict entry of the season
        self.dict = season
        
        #Add other attributes about the storm
        keys = info.keys()
        self.coords = {}
        for key in keys:
            if isinstance(info[key], list) == False and isinstance(info[key], dict) == False:
                self[key] = info[key]
                self.coords[key] = info[key]
            if isinstance(info[key], list) == True and key == 'year':
                self[key] = info[key]
                self.coords[key] = info[key]
    
    def to_dataframe(self):
        
        r"""
        Converts the season dict into a pandas DataFrame object.
        
        Returns
        -------
        `pandas.DataFrame`
            A pandas DataFrame object containing information about the season.
        """
        
        #Try importing pandas
        try:
            import pandas as pd
        except ImportError as e:
            raise RuntimeError("Error: pandas is not available. Install pandas in order to use this function.") from e
        
        #Get season info
        season_info = self.summary()
        season_info_keys = season_info['id']
        
        #Set up empty dict for dataframe
        ds = {'id':[],'name':[],'vmax':[],'mslp':[],'category':[],'ace':[],'start_time':[],'end_time':[],'start_lat':[],'start_lon':[]}
        
        #Add every key containing a list into the dict
        keys = [k for k in self.dict.keys()]
        for key in keys:
            #Get tropical duration
            temp_type = np.array(self.dict[key]['type'])
            tropical_idx = np.where((temp_type == 'SS') | (temp_type == 'SD') | (temp_type == 'TD') | (temp_type == 'TS') | (temp_type == 'HU'))
            if key in season_info_keys:
                sidx = season_info_keys.index(key)
                ds['id'].append(key)
                ds['name'].append(self.dict[key]['name'])
                ds['vmax'].append(season_info['max_wspd'][sidx])
                ds['mslp'].append(season_info['min_mslp'][sidx])
                ds['category'].append(season_info['category'][sidx])
                ds['start_time'].append(np.array(self.dict[key]['date'])[tropical_idx][0])
                ds['end_time'].append(np.array(self.dict[key]['date'])[tropical_idx][-1])
                ds['start_lat'].append(np.array(self.dict[key]['lat'])[tropical_idx][0])
                ds['start_lon'].append(np.array(self.dict[key]['lon'])[tropical_idx][0])
                ds['ace'].append(np.round(season_info['ace'][sidx],1))
                    
        #Convert entire dict to a DataFrame
        ds = pd.DataFrame(ds)

        #Return dataset
        return ds
    
    def get_storm_id(self,storm):
        
        r"""
        Returns the storm ID (e.g., "AL012019") given the storm name and year.
        
        Parameters
        ----------
        storm : tuple
            Tuple containing the storm name and year (e.g., ("Matthew",2016)).
            
        Returns
        -------
        str or list
            If a single storm was found, returns a string containing its ID. Otherwise returns a list of matching IDs.
        """
        
        #Error check
        if isinstance(storm,tuple) == False:
            raise TypeError("storm must be of type tuple.")
        if len(storm) != 2:
            raise ValueError("storm must contain 2 elements, name (str) and year (int)")
        name,year = storm
        
        #Search for corresponding entry in keys
        keys_use = []
        for key in self.dict.keys():
            temp_year = self.dict[key]['year']
            if temp_year == year:
                temp_name = self.dict[key]['name']
                if temp_name == name.upper():
                    keys_use.append(key)
                
        #return key, or list of keys
        if len(keys_use) == 1: keys_use = keys_use[0]
        if len(keys_use) == 0: raise RuntimeError("Storm not found")
        return keys_use
    
    def get_storm(self,storm):
        
        r"""
        Retrieves a Storm object for the requested storm.
        
        Parameters
        ----------
        storm : str or tuple
            Requested storm. Can be either string of storm ID (e.g., "AL052019"), or tuple with storm name and year (e.g., ("Matthew",2016)).
        
        Returns
        -------
        tropycal.tracks.Storm
            Object containing information about the requested storm, and methods for analyzing and plotting the storm.
        """
        
        #Check if storm is str or tuple
        if isinstance(storm, str) == True:
            key = storm
        elif isinstance(storm, tuple) == True:
            key = self.get_storm_id((storm[0],storm[1]))
        else:
            raise RuntimeError("Storm must be a string (e.g., 'AL052019') or tuple (e.g., ('Matthew',2016)).")
        
        #Retrieve key of given storm
        if isinstance(key, str) == True:
            return Storm(self.dict[key])
        else:
            error_message = ''.join([f"\n{i}" for i in key])
            error_message = f"Multiple IDs were identified for the requested storm. Choose one of the following storm IDs and provide it as the 'storm' argument instead of a tuple:{error_message}"
            raise RuntimeError(error_message)
        
    def plot(self,ax=None,return_ax=False,cartopy_proj=None,prop={},map_prop={}):
        
        r"""
        Creates a plot of this season.
        
        Parameters
        ----------
        ax : axes
            Instance of axes to plot on. If none, one will be generated. Default is none.
        return_ax : bool
            If True, returns the axes instance on which the plot was generated for the user to further modify. Default is False.
        cartopy_proj : ccrs
            Instance of a cartopy projection to use. If none, one will be generated. Default is none.
        
        Other Parameters
        ----------------
        prop : dict
            Customization properties of storm track lines. Please refer to :ref:`options-prop` for available options.
        map_prop : dict
            Customization properties of Cartopy map. Please refer to :ref:`options-map-prop` for available options.
        """
        
        #Create instance of plot object
        self.plot_obj = TrackPlot()
        
        if self.basin in ['east_pacific','west_pacific','south_pacific','australia','all']:
            self.plot_obj.create_cartopy(proj='PlateCarree',central_longitude=180.0)
        else:
            self.plot_obj.create_cartopy(proj='PlateCarree',central_longitude=0.0)
            
        #Plot storm
        return_ax = self.plot_obj.plot_season(self,ax=ax,return_ax=return_ax,prop=prop,map_prop=map_prop)
        
        #Return axis
        if ax != None or return_ax == True: return return_ax
        
    def summary(self):
        
        r"""
        Generates a summary for this season with various cumulative statistics.
        
        Returns
        -------
        dict
            Dictionary containing various statistics about this season.
        """
        
        #Determine if season object has a single or multiple seasons
        multi_season = True if isinstance(self.year,list) == True else False
        
        #Initialize dict with info about all of year's storms
        if multi_season == False:
            hurdat_year = {'id':[],'operational_id':[],'name':[],'max_wspd':[],'min_mslp':[],'category':[],'ace':[]}
        else:
            hurdat_year = {'id':[[] for i in range(len(self.year))],
                           'operational_id':[[] for i in range(len(self.year))],
                           'name':[[] for i in range(len(self.year))],
                           'max_wspd':[[] for i in range(len(self.year))],
                           'min_mslp':[[] for i in range(len(self.year))],
                           'category':[[] for i in range(len(self.year))],
                           'ace':[[] for i in range(len(self.year))],
                           
                           'seasons':self.year + [],
                           'season_start':[0 for i in range(len(self.year))],
                           'season_end':[0 for i in range(len(self.year))],
                           'season_storms':[0 for i in range(len(self.year))],
                           'season_named':[0 for i in range(len(self.year))],
                           'season_hurricane':[0 for i in range(len(self.year))],
                           'season_major':[0 for i in range(len(self.year))],
                           'season_ace':[0 for i in range(len(self.year))],
                           'season_subtrop_pure':[0 for i in range(len(self.year))],
                           'season_subtrop_partial':[0 for i in range(len(self.year))],
                          }
        
        #Iterate over season(s)
        list_seasons = [self.year] if multi_season == False else self.year + []
        for season_idx,iter_season in enumerate(list_seasons):

            #Search for corresponding entry in keys
            count_ss_pure = 0
            count_ss_partial = 0
            iterate_id = 1
            for key in self.dict.keys():
                
                #Skip if using multi-season object and storm is outside of this season
                if multi_season == True and int(key[-4:]) != iter_season: continue

                #Retrieve info about storm
                temp_name = self.dict[key]['name']
                temp_vmax = np.array(self.dict[key]['vmax'])
                temp_mslp = np.array(self.dict[key]['mslp'])
                temp_type = np.array(self.dict[key]['type'])
                temp_time = np.array(self.dict[key]['date'])
                temp_ace = np.round(self.dict[key]['ace'],1)

                #Get indices of all tropical/subtropical time steps
                idx = np.where((temp_type == 'SS') | (temp_type == 'SD') | (temp_type == 'TD') | (temp_type == 'TS') | (temp_type == 'HU'))

                #Get times during existence of trop/subtrop storms
                if len(idx[0]) == 0: continue
                trop_time = temp_time[idx]
                
                if multi_season == False:
                    if 'season_start' not in hurdat_year.keys():
                        hurdat_year['season_start'] = trop_time[0]
                    if 'season_end' not in hurdat_year.keys():
                        hurdat_year['season_end'] = trop_time[-1]
                    else:
                        if trop_time[-1] > hurdat_year['season_end']: hurdat_year['season_end'] = trop_time[-1]
                else:
                    if hurdat_year['season_start'][season_idx] == 0:
                        hurdat_year['season_start'][season_idx] = trop_time[0]
                    if hurdat_year['season_end'][season_idx] == 0:
                        hurdat_year['season_end'][season_idx] = trop_time[-1]
                    else:
                        if trop_time[-1] > hurdat_year['season_end'][season_idx]: hurdat_year['season_end'][season_idx] = trop_time[-1]

                #Get max/min values and check for nan's
                np_wnd = np.array(temp_vmax[idx])
                np_slp = np.array(temp_mslp[idx])
                if len(np_wnd[~np.isnan(np_wnd)]) == 0:
                    max_wnd = np.nan
                    max_cat = -1
                else:
                    max_wnd = int(np.nanmax(temp_vmax[idx]))
                    max_cat = wind_to_category(np.nanmax(temp_vmax[idx]))
                if len(np_slp[~np.isnan(np_slp)]) == 0:
                    min_slp = np.nan
                else:
                    min_slp = int(np.nanmin(temp_mslp[idx]))

                #Append to dict
                if multi_season == False:
                    hurdat_year['id'].append(key)
                    hurdat_year['name'].append(temp_name)
                    hurdat_year['max_wspd'].append(max_wnd)
                    hurdat_year['min_mslp'].append(min_slp)
                    hurdat_year['category'].append(max_cat)
                    hurdat_year['ace'].append(temp_ace)
                    hurdat_year['operational_id'].append(self.dict[key]['operational_id'])
                else:
                    hurdat_year['id'][season_idx].append(key)
                    hurdat_year['name'][season_idx].append(temp_name)
                    hurdat_year['max_wspd'][season_idx].append(max_wnd)
                    hurdat_year['min_mslp'][season_idx].append(min_slp)
                    hurdat_year['category'][season_idx].append(max_cat)
                    hurdat_year['ace'][season_idx].append(temp_ace)
                    hurdat_year['operational_id'][season_idx].append(self.dict[key]['operational_id'])

                #Handle operational vs. non-operational storms

                #Check for purely subtropical storms
                if 'SS' in temp_type and True not in np.isin(temp_type,['TD','TS','HU']):
                    count_ss_pure += 1

                #Check for partially subtropical storms
                if 'SS' in temp_type:
                    count_ss_partial += 1

            #Add generic season info
            if multi_season == False:
                narray = np.array(hurdat_year['max_wspd'])
                narray = narray[~np.isnan(narray)]
                #hurdat_year['season_storms'] = len(hurdat_year['name'])
                hurdat_year['season_storms'] = len(narray)
                hurdat_year['season_named'] = len(narray[narray>=34])
                hurdat_year['season_hurricane'] = len(narray[narray>=65])
                hurdat_year['season_major'] = len(narray[narray>=100])
                hurdat_year['season_ace'] = np.round(np.sum(hurdat_year['ace']),1)
                hurdat_year['season_subtrop_pure'] = count_ss_pure
                hurdat_year['season_subtrop_partial'] = count_ss_partial
            else:
                narray = np.array(hurdat_year['max_wspd'][season_idx])
                narray = narray[~np.isnan(narray)]
                #hurdat_year['season_storms'][season_idx] = len(hurdat_year['name'])
                hurdat_year['season_storms'][season_idx] = len(narray)
                hurdat_year['season_named'][season_idx] = len(narray[narray>=34])
                hurdat_year['season_hurricane'][season_idx] = len(narray[narray>=65])
                hurdat_year['season_major'][season_idx] = len(narray[narray>=100])
                hurdat_year['season_ace'][season_idx] = np.round(np.sum(hurdat_year['ace'][season_idx]),1)
                hurdat_year['season_subtrop_pure'][season_idx] = count_ss_pure
                hurdat_year['season_subtrop_partial'][season_idx] = count_ss_partial
                
        #Return object
        return hurdat_year
