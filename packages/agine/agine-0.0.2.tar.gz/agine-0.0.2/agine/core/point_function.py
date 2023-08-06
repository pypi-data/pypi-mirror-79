# -*- encoding: utf-8 -*-

import warnings
import numpy as np
import pandas as pd
import geopandas as gpd

from copy import deepcopy
from tqdm import tqdm as TQ
from shapely.geometry import Point

from ..libs import *
from ..config import UNITS, CRS, METRICS
from ..commons.DistanceFunctions import HaversineDistance
from ..commons.GeographicalFunctions import create_circle_polygon
from ..exceptions import EncounteredNaN, DuplicateRecords, ZeroDistanceNeighbor, ValueWarning

### --- Helper Function(s) --- ###
def _type_of_comparison(data):
	'''Given the Data, it Finds either it Falls in:
		Case-I Execution  : returns 'single_file'; or
		Case-II Execution : returns 'multi_files'

	Also, this returns a deepcopy() of the Original Data, and checks the DataType!
	'''
	data = deepcopy(data)

	if type(data) == pd.DataFrame:
		return data, 'single_file'
	elif type(data) == list:
		for d in data: # Checking if both the Data is Correct or Not
			if type(d) != pd.DataFrame:
				raise TypeError(f'Expects data to be pd.DataFrame or [pd.DataFrame, pd.DataFrame], but got {type(d)}')
		return data, 'multi_files'
	elif type(data) == tuple:
		raise TypeError('tuple are immutable in Python. A Simple list of the Same, should fix the Problem.')

	raise TypeError(f'Expects data to be pd.DataFrame or [pd.DataFrame, pd.DataFrame], but got {type(data)}')

def _validate_data(_check_data):
	'''Validate Data according to the Requirement'''
	dSize = _check_data.shape[0]
	ValidationPassed = True
	_check_data = deepcopy(_check_data)

	_check_data.dropna(inplace = True)
	if _check_data.shape[0] != dSize:
		warnings.warn(f'Encounterd {dSize - _check_data.shape[0]} NaN-Values, Removed from Analysis', EncounteredNaN)
		dSize = _check_data.shape[0]

	_check_data.drop_duplicates(inplace = True)
	if _check_data.shape[0] != dSize:
		warnings.warn(f'Encounterd {dSize - _check_data.shape[0]} Duplicate-Values, Removed from Analysis', DuplicateRecords)

	return _check_data

def _generate_polygon_data(data, loc, max_dist_arr):
	'''Generate Polygon-Data with gpd.GeoDataFrame()'''
	_vals = np.array(list(data[loc].values))

	try:
		_circle_polygon = list(map(create_circle_polygon, _vals[:, 0], _vals[:, 1], max_dist_arr))
	except ValueError as err:
		raise ValueError(f'Possibly Data contains NaN\n{err}')
	except RuntimeError:
		# https://github.com/pyproj4/pyproj/issues/202
		# Err. Msg. : RuntimeError: b'tolerance condition error'
		raise RuntimeError(f'PyProj version <= 1.9.6 behaves differently than >= 2.1.0')

	data['polygons'] = _circle_polygon
	_PolygonData = deepcopy(gpd.GeoDataFrame(data, crs = CRS, geometry = data['polygons']))
	data.drop(columns = ['polygons'], inplace = True)

	return _PolygonData

def _generate_point_data(data, loc):
	'''Generate Point-Data with gpd.GeoDataFrame()'''
	data['points'] = data[loc].apply(lambda x: Point(x[0], x[1]))
	_PointData = deepcopy(gpd.GeoDataFrame(data, crs = CRS, geometry = data['points']))
	data.drop(columns = ['points'], inplace = True)

	return _PointData

### --- Main Functions --- ###
def NearestNeighbor (
		data     : pd.DataFrame or [pd.DataFrame, pd.DataFrame], # Max. of TWO DataFrame is allowed for Comparison
		num_nbr  : int = 0,
		max_dist : int = 10,
		**kwargs
	) -> pd.DataFrame:
	'''NearestNeighbor can locate (N) number of Neighbors for a given Point/Location within a Search-Area
	
	Types of Comparison
		1. Within Same-File/DataFrame : Given x-Points/Locations in a DataFrame, it searches the Nearest One, excluding SELF
		2. Within Two Different Files : Foreach Point in File-A, it searches for the Nearest One from File-B

	Thus, there can be two type(s) of Data Input: either only a single DataFrame or a List of Two DataFrames.

	Parameters
	----------
		: param data : List of DataFrame(s) for either Case-I Execution Type, or Case-II Execution Type
		               By Default, if only a Single DataFrame is Passed then Case-I is Executed, else Case-II
		               (which are auto-assigned). Default Column Names for Each of the DataFrame is as Below:
		                   >> UIN : Unique Identification No. for the Point/Location
		                   >> loc : Location of the Point either
		                            (i) Point in n-Dimension [x1, x2, x3, ... xn], where n = No. of Diemnsion; or
		                            (ii) Actual Point on Earth in the Format [longitude, latitude]
		                            Location Object can be either a list or a tuple
		: param num_nbr : Number of Neighbor to Find. By Default num_nbr = 0, representing all the Neighbors
		                  num_nbr can be (i) unitless - for Point in n-Dimensions, or (ii) with unit for others
		                  Set the Data Unit using the kwargs as Defined below
		: param max_dist : Max. Distance within which a Neighbor has to be Located. Currently it does not understand infinity!

	Keyword Arguments
	-----------------
		: param point_type  : (str) Type of the Point, either
		                      (i) 'n-dim' - Stating a n-dimensional Point
		                      (ii) 'geo-loc' - An Actual Location on the Earth
		                      Default: 'geo-loc'
		: param input_unit  : (str) Can be ['m', 'km', 'rad', 'none']. Default 'km'
		: param output_unit : (str) Can be ['m', 'km', 'rad', 'none']. Default 'km'
		: param dist_metric : (str) Distance Metric to Use ['euclidean', 'manhattan', 'haversine']
		                      If point_type == geo-loc, then by Default haversine is used, else euclidean

		Apart from this, the Column Names can be assigned on-th-go with the following Arguments:
		: param UIN : Default 'UIN'
		: param loc : Default 'loc'

		: param keep_blanks : (bool) Keep UIN which do not have any Neighbor within the Search Radius. Default True
		                      By Default, for Blank-UINs, the NBR-UIN (with other corresponding values) is set to NaN
		                      If required, this can be changed by passing a list() as given in fillna-command
		: param fillna      : (list) fillna values with required value. Format is [bool, '<value>']
		                      By Default fillna [False, np.nan]

	NOTE: The Entire workflow is with datum = WGS84 i.e. CRS = EPSG:4326 - any other System will/might Create a Problem.
	NOTE: If the Data contains any illegal chars, it is advised to remove from Analysis, as all the Values are Not Validated.
	RETURNS : pd.DataFrame of [UIN, loc, f'NBR_{UIN}', f'NBR_{loc}', 'rnk'] # where rnk = Rank is not present for num_nbr = 1
	'''
	data, _exec_type = _type_of_comparison(data)

	### --- Getting the Keyword Arguments, and Validate --- ###
	input_unit  = kwargs.get('input_unit', 'km')
	output_unit = kwargs.get('output_unit', 'km')

	if input_unit not in UNITS: raise ValueError(f'input_unit = {input_unit} is not Understood.')
	if output_unit not in UNITS: raise ValueError(f'output_unit = {output_unit} is not Understood.')

	UIN = kwargs.get('UIN', 'UIN') # the value can be anything
	loc = kwargs.get('loc', 'loc') # the value can be anything

	point_type  = kwargs.get('point_type', 'geo-loc')

	if point_type == 'geo-loc':
		dist_metric = kwargs.get('dist_metric', 'haversine')
	elif point_type == 'n-dim':
		dist_metric = kwargs.get('dist_metric', 'euclidean')
	else:
		raise ValueError(f'{point_type} is not Understood.')

	if dist_metric not in METRICS: raise ValueError(f'dist_metric = {dist_metric} is not Understood.')

	keep_blanks = kwargs.get('keep_blanks', True)
	fillna      = kwargs.get('fillna', [False, np.nan])

	### --- Minimal Validation of Data --- ###
	timer = profilingFunction(funcName = 'Generating shapely Objects')
	if _exec_type == 'single_file':
		data = _validate_data(data) # Validating Records
		max_dist_arr = [max_dist * 1000 for _ in range(data.shape[0])]

		### --- create_circle_polygon and create_points --- ###
		PointData = _generate_point_data(data, loc)
		PolygonData = _generate_polygon_data(data, loc, max_dist_arr)

	elif _exec_type == 'multi_files':
		FileA = _validate_data(data[0])
		FileB = _validate_data(data[1])
		max_dist_arr = [max_dist * 1000 for _ in range(FileA.shape[0])]

		### --- create_circle_polygon and create_points --- ###
		PointData = _generate_point_data(FileB, loc)
		PolygonData = _generate_polygon_data(FileA, loc, max_dist_arr)

	timer.checkPoint()

	### --- Generating Neighbors List --- ###
	timer = profilingFunction(funcName = 'Joining Data with gpd.sjoin()')
	all_neighbor = gpd.sjoin(PolygonData, PointData, how = 'left', op = 'contains').reset_index()
	del PolygonData, PointData # House-Keeping!

	all_neighbor.drop(columns = ['index', 'index_right', 'geometry', 'points', 'polygons'], inplace = True)
	all_neighbor.rename(columns = {
			f'{UIN}_left'  : UIN,
			f'{loc}_left'  : loc,
			f'{UIN}_right' : f'NBR_{UIN}',
			f'{loc}_right' : f'NBR_{loc}'
		}, inplace = True)

	all_neighbor = all_neighbor[all_neighbor[UIN] != all_neighbor[f'NBR_{UIN}']] # Removing Same Site(s)
	timer.checkPoint()

	### --- keep_blanks Execution --- ###
	if keep_blanks:
		print(f'NBR_{UIN} == NaN - denotes a Location w/o a Neighbor')
		if _exec_type == 'single_file':
			_blank_UIN = np.setdiff1d(data[UIN].unique(), all_neighbor[UIN].unique())
			_blank_UIN = data[data[UIN].isin(_blank_UIN)][[UIN, loc]].reset_index()

			del data # data is no Longer Required, clearing Memory!
		elif _exec_type == 'multi_files':
			_blank_UIN = np.setdiff1d(FileA[UIN].unique(), all_neighbor[UIN].unique())
			_blank_UIN = FileA[FileA[UIN].isin(_blank_UIN)][[UIN, loc]].reset_index()

			del data, FileA, FileB # data is no Longer Required, clearing Memory!

		_blank_UIN.drop(columns = ['index'], inplace = True)
		_blank_UIN['rnk'] = [0] * _blank_UIN.shape[0] # this is essential for Filtering Purposes

	startPoints  = all_neighbor[loc].values
	targetPoints = all_neighbor[f'NBR_{loc}'].values

	_calculated_distance = []
	for s, t in TQ(zip(startPoints, targetPoints), desc = f'Calculating Distance with {dist_metric} Metric'):
		_calculated_distance.append(HaversineDistance(s, t, output_unit = output_unit))

	all_neighbor[f'Calculated Distance ({output_unit})'] = _calculated_distance
	if all_neighbor[f'Calculated Distance ({output_unit})'].min() == 0:
		_zero_dist_nbr = all_neighbor[all_neighbor[f'Calculated Distance ({output_unit})'] == 0].shape[0]
		warnings.warn(f'Found {_zero_dist_nbr}/{all_neighbor[UIN].nunique()} Neighbors at 0 units Distance')

	timer = profilingFunction(funcName = 'Calculating Ranks')
	all_neighbor['rnk'] = all_neighbor.groupby([UIN])[f'Calculated Distance ({output_unit})'].rank(method = 'dense')
	if keep_blanks:
		all_neighbor = pd.concat([all_neighbor, _blank_UIN], sort = True, ignore_index = True)

	all_neighbor.sort_values(by = [UIN, 'rnk'], inplace = True)

	if fillna[0]:
		try:
			all_neighbor.fillna(fillna[1], inplace = True)
		except ValueError as err:
			warnings.warn(f'{fillna[1]} is not accepted for pd.fillna(): {err}. Converting {fillna[1]} to str({fillna[1]})')
			all_neighbor.fillna(str(fillna[1]), inplace = True)

	all_neighbor = all_neighbor[[UIN, loc, f'NBR_{UIN}', f'NBR_{loc}', f'Calculated Distance ({output_unit})', 'rnk']]
	timer.checkPoint()

	if num_nbr == 0:
		return all_neighbor

	return all_neighbor[all_neighbor.rnk <= num_nbr]