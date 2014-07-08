#
# Math Function Methods for Spectra Kinetics
#
# Copyright 2011 Fahlstrom Research LLC
#
# Author : Carl A. Fahlstrom
#
#

def gauss(x, a, b, c):
	'''
	Returns a gaussian funtion
	first input is a numpy array of x values
	second input is amplitude
	third input is 
	fourth input is 
	The return value is a numpy array
	'''

	import math
	from numpy import power,exp

	retval = a * exp(-(power((x - b),2.))/(2. * math.pow(c,2.)))

	return retval

def biexponential(offset, slope, a, b, c1, c2, ar_x):
	'''
	'''

	from numpy import zeros, polyval
	from utils_fr import find_closest_index

	res = zeros(len(ar_x))

	try:
		b_index = list(ar_x).index(b)
	except ValueError:
		b_index = find_closest_index(ar_x, b)

	baseline = polyval([slope, offset], ar_x)

	spec1 = gauss(ar_x, a, b, c1)

	spec2 = gauss(ar_x, a, b, c2)

	res[:b_index] = spec1[:b_index]
	res[b_index:] = spec2[b_index:]

	res += baseline

	return res

def offset_gauss(offset, slope, a, b, c, ar_x):
	'''
	'''

	from numpy import polyval
	
	baseline = polyval([slope, offset], ar_x)

	res = gauss(ar_x, a, b, c1)

	res += baseline

	return res

def lognorm_pdf(ar_x, mu, sigma):
	'''
	Returns a lognormal function for the specified x, mu, sigma

	This function provides the same interface as the corresponding octave function
	which is simpler to use then the scipy version.
	'''

	from math import pi, sqrt, exp, log
	from numpy import power

	pdf = (1/(ar_x * sigma * sqrt(2*pi))) * exp(-(power(log(ar_x) - mu),2) / (2 * sigma**2))

	return pdf

def lorentzian(ar_x, x_0, gamma):
	'''
	'''
	
	from math import pi
	from numpy import power

	ret = (1/pi) * ((0.5 * gamma) / (power((ar_x - x_0),2) + (0.5 * gamma) ** 2))

	return ret

def gauss_w_compton():
	'''
	'''

def half_gauss_m_gauss():
	'''
	'''

def sigmod(st_num, range, ip, time_c, ar_x):
	'''
	'''

	from math import exp
	from numpy import power

	sig = st_num + (range / (1 + power(exp(1.), -((ar_x-ip)/time_c))))

	return sig

