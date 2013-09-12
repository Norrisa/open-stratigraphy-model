from sediment import *
import libspud
import sys
import argparse

#should be an osml file


def Main():
	#Import the command line arguments and return them
	parser = argparse.ArgumentParser(description='input a file name')
	parser.add_argument('--v','--verbose', action='store_true', help="Verbose output: mainly graphics at each time step", default=False)
	parser.add_argument('file_name', help='Insert the file name of the simulation you wish to run. It should end with.osml')
	parser.add_argument('created_file_name', help='Insert the name of the file you are generating. It should end in .pvd')
	args = parser.parse_args()
	libspud.clear_options()
	file_name = args.file_name
	Verbose = args.v
	new = args.created_file_name

	return file_name, Verbose, new

def New_File(New):
	try:
		NewFile = File(New)
	except:
		print 'File name not given for new file. Use -h for more information. Hint: it should end in .pvd'
		sys.exit() 
	return NewFile
	

def Parameters(file_name):
	
	try: 
		libspud.load_options(file_name)
	except:
		print "This file doesn't exist or is the wrong file type. It should be a .osml file. Use -h for help"
		sys.exit()
		
	try:
		start = float(libspud.get_option('/diffusion_model/timestepping/start_time',))
		end = float(libspud.get_option('/diffusion_model/timestepping/end_time'))
		time_step = float(libspud.get_option('/diffusion_model/timestepping/timestep'))
		mesh_int = int(libspud.get_option('/diffusion_model/mesh/initial_mesh_size'))
		alpha = float(libspud.get_option('/diffusion_model/model_parameters/diffusion_coefficient'))
		initial_conditions = str(libspud.get_option('/diffusion_model/model_parameters/initial_conditions'))
	except: 
		print 'The information provided was incomplete, please recreate the file'
		sys.exit()
	
	if ((start-end) >= 0):
		print 'The start time is after the end time'
		sys.exit()
	elif (time_step == 0):
		print 'The time step cannot be 0'
		sys.exit()
	elif (mesh_int == 0):
		print 'The mesh has to have a size greater than 0'
		sys.exit()
	elif ((end - start) < time_step):
		print 'The time step is too large for the total time'
		sys.exit()
	return start, end, time_step, mesh_int, alpha, initial_conditions


def set_up_model(start, end, time_step, mesh_int, alpha, initial_conditions, verbose = 'false'):
	#create a simple testcase
	model = SedimentModel()
	mesh = UnitSquareMesh(mesh_int,mesh_int)
	model.set_mesh(mesh)
	try:
		init_cond = Expression(initial_conditions) # simple slope
	except:
		print 'Your initial condition was not a function'
		sys.exit()
	init_sed = Expression('x[0]') # this gives
	# total of above gives a slope of 0 to 2 (over the unit square)
	model.set_initial_conditions(init_cond,init_sed)
	model.set_start_time(start)
	model.set_timestep(time_step)
	model.set_end_time(end)
	model.set_diffusion_coeff(alpha)
	model.init()
	model.solve()
	# answer should be 1 everywhere
	#plot(model.get_total_height(),interactive=True)
	print model.get_total_height_array()
	tha = model.get_total_height_array()
	th = model.get_total_height()
	sha = model.get_sed_height_array()
	sh = model.get_sed_height()
	topha = model.get_topographic_height_array()
	toph = model.get_topographic_height()
	return tha, th, sha, sh, topha, toph


if __name__ == "__main__" :

	fname , verbose, new = Main()

	NewFile = New_File(new)

	start, end, time_step, mesh_int, alpha, initial_conditions = Parameters(fname)

	tha, th, sha, sh, topha, toph = set_up_model(start, end, time_step, mesh_int, alpha, initial_conditions, verbose)

	NewFile << toph








