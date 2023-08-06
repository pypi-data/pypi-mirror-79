# -*- encoding: utf-8 -*-

import warnings
from platform import system, release

from ..exceptions import LimitedFunctionality

def check_imports(module_names):
	_unavailable = []
	for i in module_names:
		try:
			__import__(i)
		except ImportError:
			_unavailable.append(i)

	return _unavailable

class _env_setup:
	"""Sets the OS-Options"""
	def __init__(self):
		self.OSName    = system()
		self.OSVersion = release()

		self.point_func = ['pandas', 'fiona', 'shapely', 'pyproj', 'geopandas']
		self.line_of_st = self.point_func + ['rasterio']

		self.available_libs = ['numpy']

	@property
	def _point_func(self):
		return self.point_func

	@property
	def _line_of_st(self):
		return self.line_of_st

	@property
	def _available_libs(self):
		return self.available_libs

	@property
	def is_threading_possible(self):
		if 'linux' in self.OSName.lower():
			return True
		elif 'darwin' in self.OSName.lower():
			return True
		else:
			return False # Multi-Threading Creates problem in Windows-Environment

	@property
	def is_tensorflow_available(self):
		try:
			__import__('tensorflow')
			self.available_libs.append('tensorflow')
			return True
		except ImportError:
			return False

	@property
	def is_sklearn_available(self):
		try:
			__import__('sklearn')
			self.available_libs.append('scikit-learn')
			return True
		except ImportError:
			return False

	def module_functionality(self):
		__global_options__ = ['point-function', 'line-of-sight']
		# Check what are the available pkgs - on which global-functionality is set
		AVLBL_OPTIONS = ['commons']
		for opts, libs in zip(__global_options__, [self.point_func, self.line_of_st]):
			_check = check_imports(libs)
			if not _check:
				AVLBL_OPTIONS.append(opts)
				self.available_libs += libs
			else:
				warnings.warn(f"{opts} Functionality is NOT Available, as {_check} are Required.", LimitedFunctionality)
				_input = input('Do you want to Continue? (Y/n) ')
				if (_input == 'n') or (_input == 'N'):
					raise ImportError(f'{_check} required for {opts}')

		return AVLBL_OPTIONS

OSOptions = _env_setup() # Create a Object - that can be accessed from Everywhere!