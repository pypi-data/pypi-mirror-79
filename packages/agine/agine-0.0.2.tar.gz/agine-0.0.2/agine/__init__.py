# -*- encoding: utf-8 -*-

__author__       = 'Debmalya Pramanik'
__author_email__ = ""

__version__   = "0.0.1"
__copyright__ = "Copyright (c) 2020 Debmalya Pramanik"

__status__    = "dev"
__docformat__ = "camelCasing"

# Let's Check for the Dependencies
hardDependencies    = ['os', 'sys', 'math', 'random', 'numpy']
missingDependencies = []

for dependency in hardDependencies:
	try:
		__import__(dependency)
	except ImportError:
		missingDependencies.append(dependency)

if missingDependencies:
	raise ImportError('Required Dependencies {}'.format(missingDependencies))

print("Setting up agine-Environment...")
from .api import *