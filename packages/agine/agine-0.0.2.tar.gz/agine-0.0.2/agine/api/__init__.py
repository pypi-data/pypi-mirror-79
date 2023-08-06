# -*- encoding: utf-8 -*-

"""API is useful for (1) Exposing Functionalities, with init-time Option Registrations, and (2) Setting up agine-Environment"""

# (2) agine-Environment Setup
from .OSOptions import OSOptions
AVLBL_OPTIONS = OSOptions.module_functionality()
print(f'\tDetected OS            : {OSOptions.OSName}-{OSOptions.OSVersion}')
print(f'\tscikit-learn Options   : {OSOptions.is_sklearn_available}')
print(f'\tThreading Availibilty  : {OSOptions.is_threading_possible}')
print(f'\tTensorflow Availibilty : {OSOptions.is_tensorflow_available}')

### --- Check Lib-Version Requirement --- ###
import warnings
from ..config import _min_ver_required_
from ..exceptions import VersionWarning, LimitedFunctionality

try:
	import pkg_resources
	_get_available_libs = OSOptions._available_libs
	print(f'Available PKGS:      {_get_available_libs}')
	print(f'Available Functions: {AVLBL_OPTIONS}')

	for pkgName in _get_available_libs:
		_pkgVer_ = pkg_resources.get_distribution(pkgName).version
		_pkgVerF = float('.'.join(_pkgVer_.split('.')[:2]))
		_minReq_ = _min_ver_required_(pkgName)

		try:
			if _minReq_[0] > _pkgVerF:
				warnings.warn(f'{pkgName} Requires {_minReq_[1]} or Above, Got {_pkgVer_}', VersionWarning)
		except TypeError as err: # Required Improvevement, Issue #3
			warnings.warn(f'Unable to Check {pkgName}, got TypeError {err}.\nGot Version: ?{_pkgVer_}, Req.: ?{_minReq_[1]}',
				LimitedFunctionality)

	del pkg_resources, _get_available_libs, _pkgVer_, _pkgVerF, _minReq_
except ImportError:
	warnings.warn('Unable to Check pkg_versions as pkg_resources is unavailable', LimitedFunctionality)

del warnings, _min_ver_required_, VersionWarning, LimitedFunctionality

# (1) init-Time Option Registrations
from ..commons import * # this is alaways Available!

if 'point-function' in AVLBL_OPTIONS:
	from ..core.point_function import *
	from ..commons.GeographicalFunctions import * # though this is under commons, but requires Shapely and pyProj for Operations

if 'line-of-sight' in AVLBL_OPTIONS:
	pass