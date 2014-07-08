#
# Input Files Program for Spectra Kinetics
#
# Copyright 2011 Fahlstrom Research LLC
#
# Author : Carl A. Fahlstrom
#
#

def fit_linear(measured_x, measured_y, lo, hi):
	'''
	'''

	from numpy import polyval, power, linspace, polyfit
	import scipy.optimize

#	print len(measured_x), len(measured_y), lo, hi

	spacing = 1

	if hi < lo:
		spacing = -1

	try_line = lambda slope, b : polyval([slope, b], measured_x)

	resids = lambda x : measured_y[lo:hi:spacing] - try_line(x[0], x[1])[lo:hi:spacing]
	resids_sq = lambda x : power(measured_y[lo:hi:spacing] - try_line(x[0], x[1])[lo:hi:spacing], 2.)
	chi2 = lambda x : power(measured_y[lo:hi:spacing] - try_line(x[0], x[1])[lo:hi:spacing], 2.).sum()

	min_data = min(measured_y[1:-1])

#	resid_val = chi2([0, min_data])
#	print resid_val
#	resid_val2 = chi2([0.01, min_data])

#	if resid_val2 > resid_val:
#		rising_edge = True

#	for i in linspace(0.01, 0.5, 40):
#		new_resid_val = chi2([i, min_data])
#		if (new_resid_val > resid_val2):
#			low_slope = old_slope
#			break
#		old_slope = i
#		resid_val2 = new_resid_val

#	offset_resids = []

#	for i in linspace(min_data-20., min_data+20., 40):
#		offset_resids.append(chi2([low_slope, i]))
#		low_offset_index = offset_resids.index(min(offset_resids))
#		low_offset = linspace(min_data-20., min_data+20., 40)[low_offset_index]

#	x0 = [low_slope, low_offset]

	x0 = [0., min_data]	

	x_final = scipy.optimize.fmin(chi2, x0)

#	print x_final[0], x_final[1]

#	final_line = try_line(x_final[0], x_final[1])

	return x_final


def fit_data(xs, ys, low_base_in, high_base_in, max_index):
	'''
	'''

	from utils_fr import find_closest_index
	from math_functions_fr import biexponential
	from numpy import array
	import scipy
	from scipy import polyval
	import matplotlib

	plot_fit_flag, fit_wave_low, fit_wave_high = inter_fit_setup()
	plot_vals_fitted = []
	fit_low_in = find_closest_index(array(xs[len(xs)-1]), fit_wave_low)
	fit_high_in = find_closest_index(array(xs[len(xs)-1]), fit_wave_high)
	for i in range(len(xs)):
		line_fit = fit_linear(array(xs[i]), array(ys[i]), \
				low_base_in, high_base_in)
		line_tmp = polyval([line_fit[0], line_fit[1]], array(xs[i]))
		a_est = array(ys[i])[max_index] - line_tmp[max_index]
		if plot_fit_flag == 'y':
			matplotlib.pyplot.figure()
			matplotlib.pyplot.plot(array(xs[i]), array(ys[i]))
		x0 = [line_fit[1], line_fit[0], a_est, array(xs[i])[max_index], 50., 50.]
		chi2 = lambda x : resids_sq(array(ys[len(ys)-1][fit_low_in:fit_high_in]), biexponential(x[0], x[1], x[2], x[3], x[4], x[5], array(xs[i]))[fit_low_in:fit_high_in]).sum()
		fit_result = scipy.optimize.fmin(chi2, x0)
#		fit_resultb = scipy.optimize.fmin_l_bfgs_b(chi2, x0, approx_grad=True, bounds=[(0,max_val), (0,10.), \
#								(0,max_val), (0,len(ys[0])), (0,100.), (0,100.)])
#		fit_resultc = scipy.optimize.fmin_cg(chi2, x0)
#		fit_resulta = scipy.optimize.anneal(chi2, x0)
#		fit_resultls = scipy.optimize.leastsq(chi2, x0)
		new_bi = biexponential(fit_result[0], fit_result[1], fit_result[2], fit_result[3], \
					fit_result[4], fit_result[5], array(xs[i]))
		plot_vals_fitted.append(fit_result[2])
		if plot_fit_flag == 'y':
			matplotlib.pyplot.plot(array(xs[i]), new_bi)
	matplotlib.pyplot.show()

def fit_sigmoid(xs, ys):
	'''
	'''

	from math_functions_fr import sigmod

	x0 = [100., 50., 800., 10.]
	chi2 = lambda x : resids_sq(array(ys[len(ys)-1][fit_low_in:fit_high_in]), biexponential(x[0], x[1], x[2], x[3], x[4], x[5], array(xs[i]))[fit_low_in:fit_high_in]).sum()
	

def inter_fit_setup():
	'''
	'''

	from input_filters import input_string, input_num

	plot_fit_flag = input_string("Would you like to plot each of the fits?(y/n)")
	fit_wave_low = input_num("Input the low wavelength to fit data")
	fit_wave_low = float(fit_wave_low)
	fit_wave_high = input_num("Input the high wavelength to fit data")
	fit_wave_high = float(fit_wave_high)

	return plot_fit_flag, fit_wave_low, fit_wave_high

def resids_sq(measured, modeled):
	'''
	'''

	from numpy import power

	return power((measured - modeled), 2.)
