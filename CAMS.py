#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 10:12:04 2024

@author: douglas
"""

import cdsapi
from zipfile import ZipFile
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import cartopy, cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
from matplotlib.colors import ListedColormap
import urllib3 

# Disable warnings for data download via API
urllib3.disable_warnings()

# Global Variables
URL = 'https://ads-beta.atmosphere.copernicus.eu/api'
KEY = '########################################'
DATADIR = './'
SHAPEFILE_PATH = '/PUT/YOUR/PATH/BR_UF_2019.shp'
OUTPUT_DIR = '/PUT/YOUR/PATH/forecast/'


def download_and_extract_data():
    c = cdsapi.Client(url=URL, key=KEY)
    c.retrieve(
        'cams-global-atmospheric-composition-forecasts',
        {
            'date': '2024-08-25/2024-08-25',
            'type': 'forecast',
            'format': 'netcdf_zip',
            'variable': [
                '10m_u_component_of_wind', '10m_v_component_of_wind', 'black_carbon_aerosol_optical_depth_550nm',
                'total_aerosol_optical_depth_550nm', 'total_column_carbon_monoxide',
            ],
            'time': '00:00',
            'leadtime_hour': [str(i) for i in range(121)],
            'area': [10, -93, -60, -25],
        },
        f'{DATADIR}/CAMS.zip'
    )

    # Extract the contents of the zip file
    with ZipFile(f'{DATADIR}/CAMS.zip', 'r') as zipObj:
        zipObj.extractall(path=f'{DATADIR}/CAMS/')


def create_colormap():
    matrix = np.array([
        [256, 256, 256], [210, 214, 234], [167, 174, 214], [135, 145, 190], 
        [162, 167, 144], [189, 188, 101], [215, 209, 57], [242, 230, 11], 
        [243, 197, 10], [245, 164, 8], [247, 131, 6], [248, 98, 5], 
        [250, 65, 3], [252, 32, 1], [254, 0, 0]
    ])
    n = 17
    cams = np.ones((253, 4))
    for i in range(matrix.shape[0]):
        cams[(i * n):((i + 1) * n), :] = np.array([matrix[i, 0] / 256, matrix[i, 1] / 256, matrix[i, 2] / 256, 1])
    return ListedColormap(cams)


def plot_and_save(ds, index, colormap):
    da = ds['aod550'][index, 0, :, :]
    
    data_min, data_max, interval = 0.0, 3.0, 0.2
    levels = np.arange(data_min, data_max + interval, interval)

    fig = plt.figure(figsize=(15, 10))
    ax = plt.subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_title('AOD at 550nm', fontsize=12, loc='left') 
    ax.set_title(str(da.valid_time.values)[:-10], fontsize=12, loc='right')
    
    im = ax.contourf(da.longitude, da.latitude, da, cmap=colormap, levels=levels, extend='both', transform=ccrs.PlateCarree())
    
    # Adding shapefile
    shapefile = list(shpreader.Reader(SHAPEFILE_PATH).geometries())
    ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='gray', facecolor='none', linewidth=0.3)
    
    ax.coastlines(resolution='10m', color='black', linewidth=0.8)
    ax.add_feature(cartopy.feature.BORDERS, edgecolor='black', linewidth=0.5)
    
    gl = ax.gridlines(crs=ccrs.PlateCarree(), color='gray', alpha=1.0, linestyle='--', linewidth=0.25, 
                      xlocs=np.arange(-180, 180, 5), ylocs=np.arange(-90, 90, 5), draw_labels=True)
    gl.top_labels = False
    gl.right_labels = False
    
    cbar = plt.colorbar(im, orientation='horizontal', pad=0.05, fraction=0.05, extend='both')
    cbar.set_label('Aerosol Optical Depth 550 nm') 
    
    plt.savefig(f'{OUTPUT_DIR}/AOD{str(da.valid_time.values)[:-10]}.png', bbox_inches='tight', pad_inches=0, dpi=100)
    plt.close()


def main():
    download_and_extract_data()
    
    fn = f'{DATADIR}/CAMS/data_sfc.nc'
    ds = xr.open_dataset(fn)
    
    colormap = create_colormap()
    
    for i in range(120):
        plot_and_save(ds, i, colormap)


if __name__ == '__main__':
    main()














