# -*- coding: utf-8 -*-
# Indentation: Notepad++

'''Profiling Functions: Input Parameters: startTime, send the Start Time'''

__version__ = 1.6 # Modified to Print Elapsed Time in Hour, Minute and Seconds
__author__ = "Debmalya Pramanik"
__author_email__ = "Debmalya.Pramanik@ril.com"

import time
import math

def TimeConvert(elapsedSeconds):
	convertedTime = dict()
	for multiplier, dictKey in zip([3600, 60], ['HOURs', 'MINUTEs']):
		_val = math.floor(elapsedSeconds / multiplier)
		convertedTime[dictKey] = _val
		elapsedSeconds -= _val * multiplier
		
	convertedTime['SECONDs'] = round(elapsedSeconds, 2)
	
	return f"{convertedTime['HOURs']} Hour, {convertedTime['MINUTEs']} Minutes and {convertedTime['SECONDs']} Secs."

class profilingFunction:
	def __init__(self, funcName = '', internalFunc = False):
		self.funcName = funcName
		self.internalFunc = internalFunc
		if not self.internalFunc:
			print('Start >> {funcName}, at {cTime}'.format(funcName = self.funcName, cTime = time.ctime()))
		else:
			print('\t Start >> {funcName}, at {cTime}'.format(funcName = self.funcName, cTime = time.ctime()))
		self.startTime = time.time()
		
	@property
	def elapsedTime(self):
		endTime = time.time() - self.startTime
		if endTime >= 300:
			endTime = TimeConvert(endTime)
		else:
			endTime = f'{round(endTime, 2)} Secs.'
		return endTime
			
	def checkPoint(self):
		if not self.internalFunc:
			print('\t Completed in {endTime}'.format(endTime = self.elapsedTime))
		else:
			print('\t\t  Completed in {endTime} Seconds'.format(endTime = self.elapsedTime))
			
	def __enter__(self):
		return self
		
	def __exit__(self, type, value, traceback):
		self.checkpoint()
		pass