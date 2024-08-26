# AEROSOLS-TOOLS
This repository has the function of presenting codes for downloading and manipulating data for the visualization of AOD and CO data from different locations. The data come from:

- AERONET (Aerosol Optical Depth) - Ground-based instrument (https://aeronet.gsfc.nasa.gov/)
The AERONET is an international federation of ground based sun and sky scanning radiometer and give the aerosol optical depth data from the instruments. This code will download the data, select the optical thicknesses and finally plot for the period you chose. It is recommended that you go to the website to find out the names of the AERONET stations you want to work with.
  
- MODIS (Time Averaged Map of Aerosol Optical Depth 550 nm) - Sattelite (https://giovanni.gsfc.nasa.gov/giovanni/)
MODIS data are available in daily/monthly formats from both Terra (MOD*) and Aqua (MYD*) platforms. Go to the Giovanni website and enter the term MYD08_D3 in the search area. Be sure to login first; the same credentials from EarthData can be used. Let the plot be ‘Time Average Map’. After the search, select the desired variable, here I use “Aerosol Optical Depth 550 nm (Deep Blue, Land-only) (MYD08_D3 v6.1)”. 
  
- IASI/Metop-B (Total Column Carbon Monoxide) - Sattelite (https://iasi.aeris-data.fr/CO/)
IASI is a joint mission of EUMETSAT and the Centre National d’Etudes Spatiales (CNES, France). The authors acknowledge the AERIS data infrastructure for providing access to the IASI data in this study, ULB-LATMOS for the development of the retrieval algorithms, and Eumetsat/AC SAF for CO/O3 data production. In the case of IASI data, we have two codes, one for downloading the data and one for plotting the data. It was separated due to the fact that the data size is large, making a single code duly slow. 

- CAMS (Aerosol Optical Depth 550 nm) - Numeric Model (https://ads.atmosphere.copernicus.eu/cdsapp#!/dataset/cams-global-atmospheric-composition-forecasts?tab=form)
CAMS produces global forecasts for atmospheric composition twice a day. The forecasts consist of more than 50 chemical species (e.g. ozone, nitrogen dioxide, carbon monoxide) and seven different types of aerosol (desert dust, sea salt, organic matter, black carbon, sulphate, nitrate and ammonium aerosol). In addition, several meteorological variables are available as well. In this case, the cds API was used (Remember, to access data from the ADS, you will need first to register/login https://ads.atmosphere.copernicus.eu and obtain an API key from https://ads.atmosphere.copernicus.eu/api-how-to.). This is a unique code which downloads the data via API and plots it for the maximum forecast period (120 hours) of the numerical model.

The mainly libraries to run the codes are:
- cdsapi
- numpy
- xarray
- cartopy
- matplotlib
- wget
- pandas
