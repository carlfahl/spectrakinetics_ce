#
# Peak Search Methods for Spectra Kinetics
#
# Copyright 2011 Fahlstrom Research LLC
#
# Author : Carl A. Fahlstrom
#
#


def peak_find(ys):
	'''
	Input to this method should be a numpy array
	'''

	from filters import dig_filter
	from utils_fr import deriv

	peak_li = []
	peak_li_filters = []

	peak_li.append(zero_cross(deriv(ys)))

	for i in xrange(2,10,2):
		filtered = dig_filter(ys, i)
		deriv_fil = deriv(filtered)
		peak_li_filters.append(zero_cross(deriv_fil))

	return peak_li, peak_li_filters

def zero_cross(data):
	'''
	Finds all zero crossings of input data
	'''

	li = []
	j = 0
	data_length = len(data)

	while j < data_length:
		while data[j] < 0:
			j += 1 
		while True:
			if data[j] < 0:
				li.append(j)
				break
			j += 1

	return li
