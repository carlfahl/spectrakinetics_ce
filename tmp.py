#!/sw/bin/python

from numpy import *
from input_filters import read_file
from output_methods import write_file
import scipy.optimize
from math_functions_fr import sigmod
import sys

def fit_dat(argv):
	'''
	'''
	
	y_l = read_file(argv[0])
	ys = []

	for elem in y_l:
		num = float(elem)
#		if num < 0.0:
#			num = num + 360.0
		ys.append(num)

	ar_y = array(ys)
	ar_x = array(range(len(ys)))

	avg_st = mean(ar_y[:20])
	avg_end = mean(ar_y[-20:])

	avg_diff = avg_end - avg_st

	x0 = [avg_st, avg_diff, 800., 10.]
	chi2 = lambda x : resids_sq(ar_y, sigmod(x[0], x[1], x[2], x[3], ar_x)).sum()

	fit_result = scipy.optimize.fmin(chi2, x0)

	print fit_result

	fit_fun = sigmod(fit_result[0], fit_result[1], fit_result[2], fit_result[3], ar_x)

	fit_fun_li = []
	ys_li = []

	for elem in fit_fun:
		fit_fun_li.append(str(elem))

	for elem in ys:
		ys_li.append(str(elem))

	write_file(argv[1], fit_fun_li)
#	write_file(argv[2], ys_li)

def resids_sq(measured, modeled):
	'''
	'''

	return power((measured - modeled), 2.)

if __name__ == "__main__":
	fit_dat(sys.argv[1:])
