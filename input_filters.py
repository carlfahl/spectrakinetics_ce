#
# Input Files Program for Spectra Kinetics
#
# Copyright 2011 Fahlstrom Research LLC
#
# Author : Carl A. Fahlstrom
#
#

def input_filedir():
	'''
	'''

	import os

	while True:
		try:
			tmp = input_string("Select a file or directory: \n")
			os.path.isdir(tmp)
			break
		except TypeError:
			print "Input must be a string that corresponds to a directory"

	return tmp

def input_string(mess_st):
	'''
	'''

	print mess_st
	print "Enter 'q' to quit"

	while True:
		try:
			tmp_val = input()
			if tmp_val == 'q':
				exit()
			break
		except SyntaxError:
			print "Input must be a string"

	return tmp_val

def input_num(mess_st):
	'''
	'''

	print mess_st
	print "Enter 'q' to quit"

	while True:
		try:
			tmp_val = input()
			if tmp_val == 'q':
				exit()
			break
		except SyntaxError:
			print "Input must be a string or number"

	return tmp_val

def input_filter_wtm(orb):
	'''
	'''

def input_filter_kin(orb):
	'''
	'''

def input_filter_cray(orb):
	'''
	'''

def input_filter_xps(orb):
	'''
	'''

	xs = []

	ys = []

	for elem in orb[2:]:
		xs.append(float(elem.split()[0]))
		ys.append(float(elem.split()[1]))

	return xs, ys

def input_filter_wire(orb):
	'''
	'''

	orb2  = []

	doft = []
	
	xs = []

	ys = []

	times = []

	for i in orb:
		orb2.append(i.split())

	time = orb2[0][0]

	times.append(time)

	doft.append([])
	xs.append([])
	ys.append([])

	k = 0

	for j in orb2:
		if(j[0] != time):
			time = j[0]
			times.append(time)
			doft.append([])
			xs.append([])
			ys.append([])
			k = k + 1
			st = []
			st.append(j[0])
			st.append("\t")
			st.append(j[1])
			xs[k].append(float(j[1]))
			st.append("\t")
			st.append(j[2])
			ys[k].append(float(j[2]))
			st.append("\t")
			doft[k].append(st)
		else:
			st = []
			st.append(j[0])
			st.append("\t")
			st.append(j[1])
			xs[k].append(float(j[1]))
			st.append("\t")
			st.append(j[2])
			ys[k].append(float(j[2]))
			st.append("\t")
			doft[k].append(st)

	lines = []

	for i in range(len(doft[0])):
		line = []
		for elem in doft:
			line.extend(elem[i])
		lines.append(line)

	return lines, xs, ys, times

def read_batch_file(bfile):
	'''
	'''

	batch_lines = read_file(bfile)

	li = []
	filenames = [[]]
	filetypes = []
	methods = [[]]

	for line in bfile_lines:
		li.append(line.split())

	for elem in li:
		if elem[0][0] == '#' or "!" or "/":
			continue
		elif elem[0] == 'filename':
			filenames.append(elem[1])
#			if len(elem) > :
			continue
		elif elem[0] == 'method':
			methods.append(elem[1])
			continue
		elif elem[0] == '\n':
			newcalc = True
			filenames.append([])
			methods.append([])
		else:
			continue

	return filenames, methods

def create_batch_file():
	'''
	'''

def get_methods_inter():
	'''
	'''

	methods = {1: 'kin_trace', 2: 'filted_kin_trace', 3: 'filter', 4: 'pca', 5: '', 6: ''}

	return methods

def inter_file_open():
	'''
	'''

	import os
	from utils_fr import read_file

	print "Current directory:  ", os.getcwd(), "\n"
	print os.listdir(os.getcwd()), "\n"
	tmp = input_filedir()

	while(os.path.isdir(tmp)):
		print "Current directory:  ", os.getcwd()
		os.chdir(tmp)
		print os.listdir(os.getcwd())
		tmp = input_filedir()
				
	if(os.path.isfile(tmp)):
		infile_name = tmp
		while True:
			try:
				orb = read_file(infile_name)
				break
			except:
				print "Please input a valid filename or directory"

	return orb, infile_name

