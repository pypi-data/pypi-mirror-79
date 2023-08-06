# -*- encoding: utf-8 -*-

import warnings
import numpy as np
from math import radians

from ..config import R
from ..api import OSOptions
from ..exceptions import TypeWarning

if OSOptions.is_sklearn_available:
	from sklearn.metrics.pairwise import haversine_distances # Using SKLearn for Calculating Haversine

def EuclideanDistance(startPoint : np.ndarray, targetPoint : np.ndarray) -> float:
	'''Calculates Eculidean Distance b/w Two Points in n-Dimensional Space

	: param startPoint  : Starting Point (P)
	: param targetPoint : Target Point, or Point-Q
	'''
	if (type(startPoint) != np.ndarray) or (type(targetPoint) != np.ndarray):
		warnings.warn(f'Expects np.ndarray got {type(startPoint)} and {type(targetPoint)}, Attempting a Fix.', TypeWarning)
		startPoint  = np.array(startPoint)
		targetPoint = np.array(targetPoint)

	return np.sqrt(np.sum((startPoint - targetPoint) ** 2))

def ManhattanDistance(startPoint : np.ndarray, targetPoint : np.ndarray) -> float:
	'''Calculates Manhattan Distance b/w Two Points in n-Dimensional Space

	: param startPoint  : Starting Point (P)
	: param targetPoint : Target Point, or Point-Q
	'''
	if (type(startPoint) != np.ndarray) or (type(targetPoint) != np.ndarray):
		warnings.warn(f'Expects np.ndarray got {type(startPoint)} and {type(targetPoint)}, Attempting a Fix.', TypeWarning)
		startPoint  = np.array(startPoint)
		targetPoint = np.array(targetPoint)

	return sum([abs(i) for i in (startPoint - targetPoint)])

def HaversineDistance(startPoint : list, targetPoint : list, **kwargs) -> float:
	'''Calculate Haversine Distance

	: param startPoint  : Starting Point (P). Format [longitude, latitude]
	: param targetPoint : Target Point, or Point-Q. Format [longitude, latitude]

	Keyword Arguments
	-----------------
		: param input_unit  : (str) Unit of the Latitude and Longitude (in deg or rad). Default 'deg'
		: param output_unit : (str) Output unit (in rad, m, km). Default 'km'
	'''
	input_unit  = kwargs.get('input_unit', 'deg')
	output_unit = kwargs.get('output_unit', 'km')

	# Check argument(s)
	if input_unit not in ['deg', 'rad']:
		raise ValueError(f'{input_unit} is invalid.')

	if output_unit not in ['m', 'km', 'rad']:
		raise ValueError(f'{output_unit} is invalid.')

	if input_unit == 'deg':
		startPoint_rad  = [radians(i) for i in startPoint]
		targetPoint_rad = [radians(i) for i in targetPoint]

	if OSOptions.is_sklearn_available:
		dist = haversine_distances([startPoint_rad, targetPoint_rad])
		dist = dist[0][1] # since this returns a np.ndarray or 2x2
	else:
		dist = _haversine_wo_sklearn_(*startPoint, *targetPoint)

	if output_unit == 'rad':
		return dist
	elif output_unit == 'm':
		return dist * R

	return dist * R / 1000

def _haversine_wo_sklearn_(lon1 : int or float, lat1 : int or float, lon2 : int or float, lat2 : int or float):
	'''Calculate Haversine, if scikit-learn Package is unavailable'''
	dlat = lat2 - lat1 # delta Latitude
	dlon = lon2 - lon1 # delta Longitude

	a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2
	c = 2 * np.arcsin(np.sqrt(a)) # this is in Radian, no need to Change

	return c