"""Tests for various modules."""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import numpy.testing
import datetime as dt
import pytest

from cartopy import crs as ccrs
import tropycal.tracks as tracks

def assert_almost_equal(actual, desired, decimal=7):
    """Check that values are almost equal, including units.
    Wrapper around :func:`numpy.testing.assert_almost_equal`
    """
    actual, desired = check_and_drop_units(actual, desired)
    numpy.testing.assert_almost_equal(actual, desired, decimal)


def assert_array_almost_equal(actual, desired, decimal=7):
    """Check that arrays are almost equal, including units.
    Wrapper around :func:`numpy.testing.assert_array_almost_equal`
    """
    actual, desired = check_and_drop_units(actual, desired)
    numpy.testing.assert_array_almost_equal(actual, desired, decimal)


def assert_array_equal(actual, desired):
    numpy.testing.assert_array_equal(actual, desired)

#@pytest.mark.mpl_image_compare(tolerance=.03, remove_text=False, style='default')
def test_code():

    @pytest.mark.mpl_image_compare(tolerance=.03, remove_text=False, style='default')
    def test_plot(methodToRun, proj, use_ax, positional_arguments, keyword_arguments, use_figsize=(14,9), use_dpi=200, ax_in_dict=False):
        
        if use_ax == True:
            fig = plt.figure(figsize=use_figsize,dpi=use_dpi)
            ax = plt.axes(projection=proj)
            ax = methodToRun(*positional_arguments, ax=ax, **keyword_arguments)
        else:
            fig = plt.figure(figsize=use_figsize,dpi=use_dpi)
            ax = methodToRun(*positional_arguments, **keyword_arguments)
        
        if ax_in_dict == True:
            ax = ax['ax']
        
        return fig

    #method2(storm.plot, ['spam'], {'ham': 'ham'})
    
    #Retrieve HURDAT2 reanalysis dataset for North Atlantic
    hurdat_atl = tracks.TrackDataset()

        
    #Assign all tornadoes to storm
    hurdat_atl.assign_storm_tornadoes()
    
    #------------------------------------------------------------
    
    #Search name
    hurdat_atl.search_name('michael')
    
    #Test getting storm ID
    storm_id = hurdat_atl.get_storm_id(('michael', 2018))
    if storm_id != 'AL142018':
        raise AssertionError("Incorrect type")
    
    #Test retrieving hurricane Michael (2018)
    storm = hurdat_atl.get_storm(('michael', 2018))
    
    #Cartopy proj
    proj = ccrs.PlateCarree(central_longitude=0.0)
    
    #Make plot of storm track
    test_plot(storm.plot, proj, True, [], {'return_ax': True}, use_figsize=(14,9))
    
    #Get NHC discussion
    disco = storm.get_nhc_discussion(forecast=1)
    
    #Plot NHC forecast
    test_plot(storm.plot_nhc_forecast, proj, True, [], {'forecast': 1, 'return_ax': True}, use_figsize=(14,9))
    #ax = storm.plot_nhc_forecast(forecast=1,return_ax=True)
    
    #Plot storm tornadoes
    #test_plot(storm.plot_tors, proj, [], {'return_ax': True})
    #ax = storm.plot_tors(return_ax=True)
    
    #Plot rotated tornadoes
    test_plot(storm.plot_TCtors_rotated, proj, False, [], {'return_ax': True}, use_figsize=(9,9), use_dpi=150)
    #ax = storm.plot_TCtors_rotated(return_ax=True)
    
    #Convert to datatypes
    storm.to_dict()
    storm.to_xarray()
    storm.to_dataframe()
    
    #------------------------------------------------------------
    
    #Test retrieving season
    season = hurdat_atl.get_season(2017)
    
    #Make plot of season
    test_plot(season.plot, proj, True, [], {'return_ax': True}, use_figsize=(14,9))
    #ax = season.plot(return_ax=True)
    
    #Annual summary
    season.summary()
    
    #Dataframe
    season.to_dataframe()
    
    #------------------------------------------------------------
    
    #Rank storms
    hurdat_atl.rank_storm('ace')
    
    #Gridded stats
    test_plot(hurdat_atl.gridded_stats, proj, True, ['maximum wind'], {}, use_figsize=(14,9))
    #hurdat_atl.gridded_stats('maximum wind',return_ax=True)
    