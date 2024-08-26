#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 10:15:01 2024

@author: douglas
"""

import wget
from pathlib import Path

def generate_url(data_dict):
    """Generate the URL for data download based on the provided parameters."""
    url = (
        f"{data_dict['endpoint']}{data_dict['year']}/{str(data_dict['month']).zfill(2)}/"
        f"{data_dict['prefix']}{data_dict['year']}{str(data_dict['month']).zfill(2)}{str(data_dict['day']).zfill(2)}_"
        f"{data_dict['suffix']}"
    )
    return url

def download_data(url, output_file):
    """Download data from the generated URL, replacing the file if it already exists."""
    if output_file.exists():
        output_file.unlink() 
    print(f"Downloading from {url}...")
    wget.download(url, str(output_file))
    print(f"\nDownloaded to {output_file}")

def main(data_dict):
    """Main function to orchestrate the download, processing, and plotting of AOD data."""
    output_dir = Path('/PUT/YOUR/PATH/')
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file_name = (
        f"{data_dict['prefix']}{data_dict['year']}{str(data_dict['month']).zfill(2)}{str(data_dict['day']).zfill(2)}_"
        f"{data_dict['suffix']}"
    )
    
    output_file = output_dir / output_file_name

    url = generate_url(data_dict)
    download_data(url, output_file)
    
data_dict = {
    'endpoint': 'https://cds-espri.ipsl.upmc.fr/iasibl2/iasi_co/V6.7.0/',
    'year': 2024,
    'month': 8,
    'day': 25,
    'prefix': 'IASI_METOPB_L2_CO_',
    'suffix': 'ULB-LATMOS_V6.7.0.nc'
}

if __name__ == "__main__":
    main(data_dict)


