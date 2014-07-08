#
# Digital Filter methods for Spectra Kinetics
#
# Copyright 2011 Fahlstrom Research LLC
#
# Author : Carl A. Fahlstrom
#
# Date : 06-26-2011
#

def dig_filter(in_data, m, filter_typ = 'cos'):
	'''
	'''

	from numpy import zeros
	from math import cos, pi

	N = len(in_data)

	ret_data = zeros(N)

	for i in range(N):
		for j in range(-m,m+1):
			if filter_typ == 'cos':
				window = (1./(2.*float(m)))*(1.+cos((pi*float(j))/float(m)))
			elif filter_typ == 'rec':
				window = (1./(2.*float(m)))
			elif filter_typ == 'tri':
				window = ((1./float(m))*(1. - (float(abs(m))/float(m))))
			if (j+i) < 0:
				continue
			elif (j+i) > N-1:
				continue
			else:
				ret_data[i] += window * in_data[j + i]

	return ret_data

