# -*- encoding: utf-8 -*-

import pyproj
import warnings
import numpy as np
from math import degrees
from shapely import geometry
from functools import partial
from shapely.ops import transform
from shapely.geometry import Point, Polygon

from ..config import R, DATUM
from ..exceptions import TypeWarning

# Check https://gis.stackexchange.com/questions/121256/ and
# Check https://gis.stackexchange.com/questions/289044/ for More Information
# NOTE : this converts everything into 'm'

def create_circle_polygon(centerLon : int or float, centerLat : int or float, radius : int or float = 10000) -> Polygon:
	'''Create a Circle from the given [longitude, latitude] with the given Radius

	: param centerLat : Center Latitude - in WGS84
	: param centerLon : Center Longitude - in WGS84

	: param radius    : Radius of the Circle, in 'm' ONLY. Default 10000 = 10 km

	Returns shapely.Polygon Object
	'''
	local_azimuthal_projection = f"+proj=aeqd +R={R} +units=m +lat_0={centerLat} +lon_0={centerLon}"

	WGS84_to_AEQD = partial( # AEQD = Azimuthal Equidistance Projection
			pyproj.transform,
			pyproj.Proj(local_azimuthal_projection),
			pyproj.Proj(f"+proj=longlat +datum={DATUM} +no_defs")
		)

	AEQD_to_WGS84 = partial(
			pyproj.transform,
			pyproj.Proj(local_azimuthal_projection),
			pyproj.Proj(f"+proj=longlat +datum={DATUM} +no_defs")
		)

	point = Point(float(centerLon), float(centerLat)) # Center-Point
	point = transform(WGS84_to_AEQD, point)

	circular_poly = point.buffer(radius)
	circular_poly = transform(AEQD_to_WGS84, circular_poly)

	return circular_poly

def calculate_bearing_angle(startPoint : tuple, targetPoint : tuple, **kwargs) -> float:
	'''Calculates the Bearing Angle b/w two Points

	Mathematically, the Bearing Angle b/w two-points is Calculated by:
		θ = atan2(sin(Δlong).cos(lat2), cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))

	: param startPoint  : Starting Point in the format (longitude, latitude)
	: param targetPoint : Target/End Point in the format (longitude, latitude)

	Keyword Arguments
		: param input_unit  : (str) Output Unit which can be ['deg', 'rad']. Default deg
		: param output_unit : (str) Output Unit which can be ['deg', 'rad']. Default deg

	Return bearing_angle (float) in desired Units.
	'''
	input_unit  = kwargs.get('input_unit', 'deg')
	output_unit = kwargs.get('output_unit', 'deg')

	if input_unit not in ['deg', 'rad']: raise ValueError(f'{input_unit} is not an accepted input_unit.')
	if output_unit not in ['deg', 'rad']: raise ValueError(f'{output_unit} is not an accepted output_unit.')

	if (type(startPoint) != tuple) or (type(targetPoint) != tuple):
		startPoint  = tuple(startPoint)
		targetPoint = tuple(targetPoint)

		warnings.warn(f'Expects tuple() got {type(targetPoint)} and {type(targetPoint)}. Working with list() is Not-Advised', TypeWarning)

	if input_unit == 'deg':
		lon1, lat1, lon2, lat2 = map(np.radians, [startPoint[0], startPoint[1], targetPoint[0], targetPoint[1]])
	else:
		lon1, lat1, lon2, lat2 = startPoint[0], startPoint[1], targetPoint[0], targetPoint[1]

	dLon = lon2 - lon1
	theta = np.arctan2(np.sin(dLon) * np.cos(lat2), np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(dLon))

	if output_unit == 'rad':
		return theta

	theta = degrees(theta)
	theta = (theta + 360) % 360

	return theta # this is in degrees

def calculate_point_at_bearing(point : tuple, distance : int or float, theta : int or float, **kwargs) -> list:
	'''Calculate the Geographich Point (lon, lat) given an Initial Point, Bearing Angle and Distance

	: param point    : Satrting/take-off Point (lon, lat)
	: param theta    : Bearing Angle at which the Point is Required
	: param distance : Required Distance b/w the startPoint and the Calculated Point. Distance Unit is in meters
	                   Change the input unit using the keyword input_distance_unit

	Keyword Arguments
		: param input_unit  : (str) Output Unit which can be ['deg', 'rad']. Default deg
		: param output_unit : (str) Output Unit which can be ['deg', 'rad']. Default deg

		: param input_distance_unit : (str) Input Distance Unit, which can be ['m', 'km']. Default 'm'
		                              **NOTE the similar argument name: input_unit and input_distance_unit

	Returns (lon, lat) in Degress
	'''
	from ..config import R # Unable to access the value R during import?

	input_unit  = kwargs.get('input_unit', 'deg')
	output_unit = kwargs.get('output_unit', 'deg')

	if input_unit not in ['deg', 'rad']: raise ValueError(f'{input_unit} is not an accepted input_unit.')
	if output_unit not in ['deg', 'rad']: raise ValueError(f'{output_unit} is not an accepted output_unit.')

	input_distance_unit = kwargs.get('input_distance_unit', 'm')
	if input_distance_unit not in ['m', 'km']: raise ValueError(f'{input_distance_unit} is not an accepted input_distance_unit.')

	if input_distance_unit == 'km':
		R /= 1000 # Change R to kilometer

	if type(point) != tuple:
		point  = tuple(point)
		warnings.warn(f'Expects tuple() got {type(point)}. Working with list() is Not-Advised', TypeWarning)

	if input_unit == 'deg':
		theta    = np.deg2rad(theta)
		lon, lat = map(np.radians, point)
	else:
		lon, lat = point

	lat2 = np.arcsin(np.sin(lat) * np.cos(distance / R) + np.cos(lat) * np.sin(distance / R) * np.cos(theta))
	lon2 = lon + np.arctan2(np.sin(theta) * np.sin(distance / R) * np.cos(lat), np.cos(distance / R) - np.sin(lat) * np.sin(lat))

	if output_unit == 'rad':
		return lon2, lat2

	lon2, lat2 = map(np.degrees, [lon2, lat2])
	return lon2, lat2 # this is in Degrees