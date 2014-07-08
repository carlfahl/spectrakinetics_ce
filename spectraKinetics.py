#!/usr/bin/python

import sys
import gtk
import gobject
#from Tkinter import *
import webbrowser
try:
	from numpy import *
except ImportError:
	print "This program requires Numpy \n \
	Please download at http://www.numpy.org/ \
	If downloading a binary version make sure \
	it was built for Python", sys.version
	webbrowser.open("http://www.numpy.org")
try:
	import matplotlib.pyplot
except ImportError:
	print "This program requires the MatPlotLib package \n \
	Please download at http://matplotlib.sourceforge.net/ \n \
	If downloading a binary version make sure \
	it was built for Python", sys.version
	webbrowser.open("http://matplotlib.sourceforge.net")

try:
	import scipy.optimize
	from scipy import polyval
except ImportError:
	print "This program requires the SciPy package \n \
	Please download at http://www.scipy.org/ \
	If downloading a binary version make sure it \
	was built for Python", sys.version
	webbrowser.open("http://www.scipy.org")

import input_filters
from input_filters import *
from filters import *
from fit_functions import *
from math_functions_fr import *
from peak_find import *
from utils_fr import *

def spec_kin(infile, infileformat, outfile, dobatchfile):
	'''
	spec_kin - 

	Version 1.0 01/06/2011	

	Author: Carl A. Fahlstrom

	Copyright 2011 Fahlstrom Research LLC

	'''

	print "SpectraKinetics version 1.0\n"

        print "END USER LICENSE AGREEMENT \n\n \This software is provided to the Walker Research Group\n \
	of Montana State University for internal use and \n \
	for beta testing purposes only by Fahlstrom Research LLC\n \
	http://www.fahlstrom-research.com\n\n \
	Use of this software is restricted to one computer only.\n \
	Modification of this software without permission of Fahlstrom research LLC \n \
	is prohibited.\n\n \
	If this software is used to process data leading to publication this software must \n \
	be referenced as (SpectraKinetics by Fahlstrom Research LLC (www.fahlstrom-research.com)) \n\n \
	Use of this software implies acceptance of this agreement.\n\n \
	All input must be in quotes unless entering a number\n\n"
	
#	if not dobatchfile and infile:
#		usebatchfile = input_string("Is the input file a batch file? (y/n)")
#		if usebatchfile == 'y':
#			dobatchfile = True

#	if dobatchfile:
#		files, methods = read_batch_file(infile)
		
	more_files = True

	while more_files:
		if infile:
			orb = read_file(infile)
			infile_name = infile
			methods = get_methods_iter()
		else:
#			orb, infile_name, methods = inter_file_open()
			orb, infile_name = inter_file_open()
		# Here we will call the appropriate input filter
#		tmp = input_string("What is your file format? (wire, xps, cray, wtm, kin)")
#		if tmp == 'Wire':
#			lines, xs, ys, times = input_filter_wire(orb)
#		if tmp == 'XPS':
#			lines, xs, ys, times = input_filter_xps(orb)
		while True:
#			try:
				tmp = input_string("What is your file format? (wire, xps, cray, wtm, kin)")
				lines, xs, ys, times = getattr(input_filters, 'input_filter_'+tmp.lower())(orb)
				break
#			except:
#				print "Input a string that corresponds to a supported input file type.\nFile may not be in correct format."
		li = []

		for elem in lines:
			li.append("".join(elem))

		while True:
			tmp = input_string("Input a name for the output file:\n")

			while tmp == infile_name:
				overwrite = input_string("Are you sure you want to overwrite the input file?(y/n)")
				if overwrite == 'y':
					break
				else:
					tmp = input_string("Input a name for the output file:")

			outfile_name = tmp

			try:
				write_file(outfile_name, li)
				break
			except TypeError:
				print "Input must be a string"

		print "This file is suitable to import in Igor or Octave"

		plotflag = input_string("Do you want to plot this data now? (y/n)")

		if plotflag == 'y':
			numpfig = input_num("How may lines per figure?")
			numpfig = int(numpfig)
			offset_num = input_num("What offset would you like to apply to lines?")
			offset_num = float(offset_num)
			cum_offset = 0.0
			for i in range(len(xs)):
				if (i % numpfig) == 0:
					cum_offset = 0.0
					matplotlib.pyplot.legend()
					matplotlib.pyplot.figure()
				ar_x = array(xs[i])
				ar_y = array(ys[i]) + cum_offset
				matplotlib.pyplot.plot(ar_x, ar_y, label=times[i])
				cum_offset += offset_num
			matplotlib.pyplot.show()

		max_index = ys[len(ys)-1].index(max(ys[len(ys)-1]))
		max_val = max(ys[len(ys)-1])

		fit_flag = input_string("Would you like to fit the data to a gaussian function?(y/n)")

		if fit_flag == 'y':
			fit_data(xs, ys, 10, 300, max_index)

		kin_tr = input_string("Plot Kinetic trace of peak? (y/n)")

		if kin_tr == 'y':
#			window = input_string("In what wavelength range should the peak max be searched?")
			plot_vals, plot_vals_max = kin_trace(ys, max_index, 10)
			mk_pyplot2d(times, plot_vals, finalize=False)
			mk_pyplot2d(times, plot_vals_max)
			tr_file = input_string("Input a filename to save the peak wavelength kinetic trace")
			write_file_2(tr_file, times, plot_vals)
			tr_file_max = input_string("Input a filename to save the max value close to the peak wavelength kinetic trace")
			write_file_2(tr_file_max, times, plot_vals_max)

		kin_tr = input_string("Plot Kinetic trace of peak with cosine filtering? (y/n)")

		if kin_tr == 'y':
			plot_vals_filter = filtered_kin_trace(ys, 5, max_index, 10)
			mk_pyplot2d(times, plot_vals_filter)
			tr_file_cos = input_string("Input a filename to save the cosine filtered kinetic trace")
			write_file_2(tr_file_cos, times, plot_vals_filter)

		kin_tr = input_string("Plot Kinetic trace of peak with fitted data? (y/n)")

		if kin_tr == 'y':
			mk_pyplot2d(times, plot_vals_fitted)
			tr_file_fit = input_string("Input a filename to save the fitted data kinetic trace")
			write_file_2(tr_file_fit, times, plot_vals_fitted)

		cont = input_string("Do you want to process another file? (y/n)")

		if cont == 'y':
			more_files = True
		else:
			more_files = False

def mk_pyplot2d(x, y, leg_lab=None, xaxis_lab=None, yaxis_lab=None, finalize=True):
	'''
	function to consolidate multiple calls to a multiline ploting method
	'''

	matplotlib.pyplot.figure()
	if leg_lab:
		matplotlib.pyplot.legend()
		matplotlib.pyplot.plot(x, y, label=leg_lab)
	else:
		matplotlib.pyplot.plot(x, y)
	if xaxis_lab:
		matplotlib.pyplot.xlabel(xaxis_lab)
	if yaxis_lab:
		matplotlib.pyplot.ylabel(yaxis_lab)
	if finalize:
		matplotlib.pyplot.show()

def kin_trace(ys, max_index, window):
	'''
	'''
	plot_vals = []
	plot_vals_max = []
	for elem in ys:
		plot_vals.append(elem[max_index])
		plot_vals_max.append(max(elem[max_index-window:max_index+window]))

	return plot_vals, plot_vals_max

def setup_line_fit(xs):
	'''
	'''

	baseline_low = input_num("Input the low wavelength for the baseline fit")
	baseline_low = float(baseline_low)
	baseline_high = input_num("Input the high wavelength for the baseline fit")
	baseline_high = float(baseline_high)
	low_base_in = find_closest_index(array(xs[len(xs)-1]), baseline_low)
	high_base_in = find_closest_index(array(xs[len(xs)-1]), baseline_high)

	return low_base_in, high_base_in

def setup_gauss_fit():
	'''
	'''

def filtered_kin_trace(ys, m, max_index, window):
	'''
	'''

	plot_vals = []

	for elem in ys:
		ar = array(elem)
		filtered = dig_filter(ar, m)
		plot_vals.append(max(filtered[max_index-window:max_index+window]))

	return plot_vals



#class FileDialog:
#	'''
#	'''
#	
#	def __init__(self,root):
#	'''
#	'''



if __name__ == "__main__":
#       if len(sys.argv) == 1:
#               print_doc_string(spec_kin)
	if len(sys.argv) > 1:
		if sys.argv[1] in help_li:
			print_doc_string(spec_kin)

	opts = {'-spch':None, '-of':None, '-if':None, '-format':None, '-sl':0, '-el':0, '-cr':None, '-batch':None}
	supported_formats = ['wire', 'xps', 'cray', 'wtm', 'kin']
	if len(sys.argv) > 1:
		for elem in sys.argv[1:]:
			if elem in opts.keys():
				idex = sys.argv.index(elem)+1
				opts[elem] = sys.argv[idex]
				sys.argv.remove(sys.argv[idex])
				sys.argv.remove(elem)
	spec_kin(opts['-if'], opts['-format'], opts['-of'], opts['-batch'])
#		root = Tk()
#		FileDialog(root).pack()
#		root.mainloop()
