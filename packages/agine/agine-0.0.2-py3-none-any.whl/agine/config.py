# -*- encoding: utf-8 -*-

'''Config File - for CONSTANTS'''
R = 6371000 # Radius of the Earth

CRS     = {'init' : 'epsg:4326'}
DATUM   = 'WGS84'
UNITS   = ['m', 'km', 'rad', 'none']
METRICS = ['euclidean', 'manhattan', 'haversine']

### --- Min. Version Requirement --- ###
def _min_ver_required_(lib_name : str) -> list:
	'''Given a Python-Library Name (required by this Module) - Returns the Min. Required Version
	This is useful, to avoid any unwanted errors, for instance:
		1. geopandas <= 0.5.0 has no Atrribute gpd.points_from_xy
		2. pyproj 1.9.6 and 2.1.0 behaves differently. Issue #202 (pyProj)
		   >> https://github.com/pyproj4/pyproj/issues/202
	To mitigate this issues, this version is invoked at init-time Option Registrations - Warning users of the Same
	TODO : Changes in the setup file, to update packages. However, this might create an Issue in Windows OS
	The Format of the Version is given as lib_nam : [version, expanded_version]
	'''
	return {
		'numpy'      : lambda : [1.18, '1.18.1'],
		# Special Libraries
		'sklearn'    : lambda : [0.21, '0.21.3'],
		'tensorflow' : lambda : [2.2, '2.2.0'], # TensorFlow 1.x has some missing attributes
		# point_func Libraries
		'fiona'      : lambda : [1.8, '1.8.6'],
		'pandas'     : lambda : [0.24, '0.24.2'],
		'pyproj'     : lambda : [2.4, '2.4.2.post1'],
		'shapely'    : lambda : [1.6, '1.6.4.post2'],
		'geopandas'  : lambda : [0.5, '0.5.0'],
		# line-of-sight Libraries
		'rasterio'   : lambda : [1.1, '1.1.2']
	}.get(lib_name, lambda : f'{lib_name} is not currently required for agine')()