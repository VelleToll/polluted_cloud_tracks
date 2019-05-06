# polluted_cloud_tracks
Python code to detect polluted cloud pixels in satellite images

Additional information:
Velle Toll
velle.toll@ut.ee

This python code demonstrates identification of polluted and unpolluted satellite pixels
in the area of polluted cloud track.

Longitudes, latitudes, and near-infrared reflectance of MODIS satellite data for one example MODIS granule containing polluted cloud
track are given in python data arrays lats.npy,lons.npy,NIR.npy.
Centre line coordinates of the polluted cloud track (this has been hand-logged by clicking on the image of MODIS near-infrared reflectance) are given in the text file track.txt. 

Python files:

main.py - main progrm, handles data input and runs the classification code.
classification.py - demonstrates the pixel classification method.
geometry_calc.py - geometrical calculations.

numpy, shapely and matplotlib python packages are used.
