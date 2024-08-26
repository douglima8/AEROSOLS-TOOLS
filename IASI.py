#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 09:25:05 2024

@author: douglas
"""

import os
import glob
import xarray as xr
import dask
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
from matplotlib.colors import ListedColormap
import cartopy, cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader # Import shapefiles
import cartopy.feature as cfeature
import warnings
from concurrent.futures import ProcessPoolExecutor
import time
warnings.filterwarnings('ignore')
warnings.simplefilter(action='ignore', category=RuntimeWarning)

def load_data(file_path):
    dataset = xr.open_dataset(file_path, chunks={'ground_pixel': 10000})
    co_data = dataset['CO_total_column']
    lat = dataset['latitude']
    lon = dataset['longitude']
    return co_data, lat, lon, dataset.attrs

def preprocess_data(co_data, lat, lon, conversion_factor):
    co_data = co_data * co_data.attrs.get('multiplication_factor_to_convert_to_molecules_per_cm2', 1.0)
    co_data_processed = xr.DataArray(
        co_data,
        dims=('ground_pixel'),
        coords={
            'latitude': ('ground_pixel', lat.data),
            'longitude': ('ground_pixel', lon.data)
        },
        attrs={'long_name': co_data.name, 'units': co_data.attrs.get('units', 'unknown')},
        name=co_data.name
    )
    return co_data_processed * conversion_factor

def create_colormap():
    matrix = np.array([[256, 256, 256],
                       [210, 214, 234],
                       [167, 174, 214],
                       [135, 145, 190],
                       [162, 167, 144],
                       [189, 188, 101],
                       [215, 209, 57],
                       [242, 230, 11],
                       [243, 197, 10],
                       [245, 164, 8],
                       [247, 131, 6],
                       [248, 98, 5],
                       [250, 65, 3],
                       [252, 32, 1],
                       [254, 0, 0]])
    n = 17
    cams = np.ones((253, 4))
    for i in range(matrix.shape[0]):
        cams[(i * n):((i + 1) * n), :] = np.array([matrix[i, 0] / 256, matrix[i, 1] / 256, matrix[i, 2] / 256, 1])
    return ListedColormap(cams)

def plot_data(co_data, lat, lon, conversion_factor, shapefile_path, date_str, output_dir):
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_extent([-93.0, -25.0, -60.0, 10.0], crs=ccrs.PlateCarree())

    cmap = create_colormap()
    img = ax.scatter(
        lon.data,
        lat.data,
        c=co_data.data,
        cmap=cmap,
        marker='o',
        s=8,
        transform=ccrs.PlateCarree(),
        vmin=0,
        vmax=8
    )

    shapefile = list(shpreader.Reader(shapefile_path).geometries())
    ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='gray',facecolor='none', linewidth=0.3)
    ax.coastlines(resolution='10m', color='black', linewidth=0.8)
    ax.add_feature(cartopy.feature.BORDERS, edgecolor='black', linewidth=0.5)
    gl = ax.gridlines(crs=ccrs.PlateCarree(), color='gray', alpha=1.0, linestyle='--', linewidth=0.25, xlocs=np.arange(-180, 180, 5), ylocs=np.arange(-90, 90, 5), draw_labels=True)
    gl.top_labels = False
    gl.right_labels = False

    cbar = fig.colorbar(img, label='*1e-18 molecules per cm2', ax=ax, orientation='horizontal', extend='both', pad=0.05, fraction=0.05)
    ax.set_title(f'IASI/Metop-B - Total Column Carbon Monoxide', fontsize=10, loc='left')
    ax.set_title(f'{date_str}', fontsize=10, loc='right')
    
    
    plt.savefig(os.path.join(output_dir, f'CO_IASI_{date_str}.png'),bbox_inches='tight', pad_inches=0,dpi=100)
    plt.close(fig)

def process_file(file_path, shapefile_path, output_dir):
    co_data, lat, lon, attrs = load_data(file_path)
    co_data_processed = preprocess_data(co_data, lat, lon, conversion_factor=1e-18)

    date_str = attrs.get("time_coverage_start", "unknown")[:8]
    date_obj = datetime.strptime(date_str, "%Y%m%d")
    formatted_date = date_obj.strftime("%d %B %Y")

    plot_data(co_data_processed, lat, lon, 1e-18, shapefile_path, formatted_date, output_dir)

def main():
    start_time = time.time()

    input_pattern = '/PUT/YOUR/PATH/IASI_METOPB_L2_CO_*.nc'
    shapefile_path = '/PUT/YOUR/PATH/BR_UF_2019.shp'
    output_dir = '/PUT/YOUR/PATH/plots'

    os.makedirs(output_dir, exist_ok=True)

    input_files = glob.glob(input_pattern)

    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_file, file_path, shapefile_path, output_dir) for file_path in input_files]
        for future in futures:
            future.result()

    end_time = time.time()  # Record end time
    execution_time = end_time - start_time
    print(f"Total execution time: {execution_time:.2f} seconds")

if __name__ == "__main__":
    main()