#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 24 08:43:13 2024

@author: douglas
"""

import wget
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def generate_url(data_dict):
    """Generate the URL for data download based on the provided parameters."""
    url = (
        f"{data_dict['endpoint']}?site={data_dict['station']}&year={data_dict['year']}&month={data_dict['month']}&day={data_dict['day']}"
        f"&year2={data_dict['year2']}&month2={data_dict['month2']}&day2={data_dict['day2']}&AOD15={data_dict['AOD15']}&AVG={data_dict['AVG']}"
    )
    return url


def download_data(url, output_file):
    """Download data from the generated URL, replacing the file if it already exists."""
    if output_file.exists():
        output_file.unlink()  # --> remove the file if it exists to avoid duplicate names
    wget.download(url, str(output_file))


def read_and_clean_data(file_path):
    """Read the data from the specified file path and clean it."""
    df = pd.read_table(file_path, delimiter=',', header=[7], index_col=1)
    df.replace(-999.0, np.nan, inplace=True)
    return df


def plot_aod_data(df, data_dict, output_plot):
    """Plot the Aerosol Optical Depth data and save the plot as a PNG file."""
   # --> you can plot other's columns (see your .txt file to identify)
    aod_columns = [
        'AOD_1640nm', 'AOD_1020nm', 'AOD_870nm',
        'AOD_675nm', 'AOD_500nm', 'AOD_551nm',
        'AOD_440nm', 'AOD_380nm', 'AOD_340nm'
    ]
    
    # --> create the plot
    fig, ax = plt.subplots(figsize=(15, 10))
    df[aod_columns].plot(ax=ax, linestyle='dotted', linewidth=2.5)
    
    # --> ajust the title and labels using the dictionary with the informations
    station_name = data_dict['station'].replace('_', ' ')
    month_name = pd.to_datetime(f"{data_dict['year']}-{data_dict['month']}-01").strftime('%B')
    ax.set_title(f'Aerosol Optical Depth Level 1.5 data for {month_name} {data_dict["year"]} - {station_name}, Brazil', fontsize=20, pad=20)
    ax.set_ylabel('Aerosol Optical Depth', fontsize=16)
    ax.set_xlabel('Day', fontsize=16)
    
    # --> gridline
    ax.tick_params(axis='both', labelsize=14)
    ax.legend(fontsize=14, loc='best')
    ax.grid(True)
    
    # --> you decide what is the limit, depends on the data and the period
    ax.set_ylim(0, 2)
    
    plt.savefig(output_plot, bbox_inches='tight', pad_inches=0, dpi=100)


def main(data_dict):
    """Main function to orchestrate the download, processing, and plotting of AOD data."""
    output_dir = Path('/PUT/YOUR/PATH/')
    output_file = output_dir / f"{data_dict['year']}{str(data_dict['month']).zfill(2)}_{data_dict['prefix']}_aod15_10.txt"
    
    initial_date = f"{data_dict['year']}{str(data_dict['month']).zfill(2)}{str(data_dict['day']).zfill(2)}"
    output_plot = output_dir / f"AOD_AERONET_{data_dict['station']}_{initial_date}.png"
    
    url = generate_url(data_dict) 
    download_data(url, output_file)
    df = read_and_clean_data(output_file)
    plot_aod_data(df, data_dict, output_plot)


data_dict = {
    'endpoint': 'https://aeronet.gsfc.nasa.gov/cgi-bin/print_web_data_v3',
    'station': 'Sao_Martinho_SONDA',
    'year': 2024,
    'month': 8,
    'day': 1,
    'year2': 2024,
    'month2': 8,
    'day2': 21,
    'AOD15': 1,
    'AVG': 10,
    'prefix': 'SM'  
}

if __name__ == "__main__":
    main(data_dict)