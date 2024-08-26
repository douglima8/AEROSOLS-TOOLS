#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 24 09:11:43 2024

@author: douglas
"""

import xarray as xr
import glob
import matplotlib.pyplot as plt
import cartopy, cartopy.crs as ccrs        # Plot maps
import cartopy.io.shapereader as shpreader # Import shapefiles
from matplotlib.pyplot import MultipleLocator
import numpy as np
import re
from datetime import datetime

extent = [-93.00,-60.00,-25.00,10.00]

def extract_date_from_filename(filename):
    """Extract date from filename in the format YYYYMMDD."""
    match = re.search(r'(\d{8})\.nc$', filename)
    if match:
        return datetime.strptime(match.group(1), '%Y%m%d')
    else:
        raise ValueError(f"Filename {filename} does not match the expected format.")

def extract_month_from_filename(filename):
    """Extract month and year from filename in the format YYYYMM."""
    match = re.search(r'(\d{6})', filename)
    if match:
        return datetime.strptime(match.group(1), '%Y%m').strftime('%B_%Y')
    else:
        raise ValueError(f"Filename {filename} does not match the expected format.")

def process_files(file_list):
    """Load and concatenate aerosol data from multiple files."""
    datasets = []
    for file in file_list:
        print(f"Processing file: {file}")
        dataset = xr.open_dataset(file)
        aerosol = dataset['MYD08_D3_6_1_Deep_Blue_Aerosol_Optical_Depth_550_Land_Mean']
        datasets.append(aerosol)
    combined = xr.concat(datasets, dim='time')
    mean_aerosol = combined.mean(dim='time')
    return mean_aerosol, dataset

def plot_data(mean_aerosol, dataset, title_str, output_filename):
    """Plot the data and save the figure."""
    lat = dataset['lat_bnds'][:, 0]
    lon = dataset['lon_bnds'][:, 0]

    plt.figure(figsize=(12, 10))
    ax = plt.axes(projection=ccrs.PlateCarree())
    img_extent = [extent[0], extent[2], extent[1], extent[3]]
    ax.set_extent([extent[0], extent[2], extent[1], extent[3]], ccrs.PlateCarree())

    data_min = 0.1
    data_max = 1.0
    interval = 0.05
    levels = np.arange(data_min, data_max + interval, interval)

    img1 = ax.contourf(lon, lat, mean_aerosol, cmap='hot_r', levels=levels, extend='both', transform=ccrs.PlateCarree())
    img2 = ax.contour(lon, lat, mean_aerosol, colors='white', levels=levels, linewidths=0.3, transform=ccrs.PlateCarree())

    plt.colorbar(img1, label='Aerosol Optical Depth 550 nm', orientation='horizontal', pad=0.05, fraction=0.05)
    plt.title(title_str, fontsize=10)

    shapefile = list(shpreader.Reader('/home/douglas/SHAPEFILE/BR_UF_2019.shp').geometries())
    ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='gray', facecolor='none', linewidth=0.3)
    ax.coastlines(resolution='10m', color='black', linewidth=0.8)
    ax.add_feature(cartopy.feature.BORDERS, edgecolor='black', linewidth=0.5)
    
    gl = ax.gridlines(crs=ccrs.PlateCarree(), color='gray', alpha=1.0, linestyle='--', linewidth=0.25, xlocs=np.arange(-180, 180, 5), ylocs=np.arange(-90, 90, 5), draw_labels=True)
    gl.top_labels = False
    gl.right_labels = False

    plt.savefig(output_filename, bbox_inches='tight', pad_inches=0, dpi=100)
    plt.close()

if __name__ == "__main__":
    # Define the path to the data files
    path = '/PUT/YOUR/PATH/data*'
    file_list = sorted(glob.glob(path))

    # Get the start and end dates
    start_date = extract_date_from_filename(file_list[0])
    end_date = extract_date_from_filename(file_list[-1])
    title_str = f"Time Averaged Map of Aerosol Optical Depth 550 nm ({start_date.strftime('%Y/%m/%d')}-{end_date.strftime('%Y/%m/%d')})"

    # Extract month for filename
    month_str = extract_month_from_filename(file_list[0])
    output_filename = f'/PUT/YOUR/PATH/AOD_MODIS_MEAN_{month_str}.png'

    # Process the data and plot
    mean_aerosol, dataset = process_files(file_list)
    plot_data(mean_aerosol, dataset, title_str, output_filename)