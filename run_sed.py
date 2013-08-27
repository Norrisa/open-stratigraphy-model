from sediment import *
import libspud
import sys

#should be an osml file
try: 
  libspud.load_options('test15.osml')
except:
	print "This file doesn't exist or is the wrong file type. It should be a .osml file"
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
elif ((end - start) <= time_step):
	print 'The time step is too large for the total time'
	sys.exit()
	
#create a simple testcase
model = SedimentModel()
mesh = UnitSquareMesh(mesh_int,mesh_int)
model.set_mesh(mesh)
init_cond = Expression(initial_conditions) # simple slope
init_sed = Expression('x[0]') # this gives
# total of above gives a slope of 0 to 2 (over the unit square)
model.set_initial_conditions(init_cond,init_sed)
#model.set_start_time(start)
model.set_timestep(time_step)
model.set_end_time(end)
model.set_diffusion_coeff(alpha)
model.init()
model.solve()
# answer should be 1 everywhere
plot(model.get_total_height(),interactive=True)
print model.get_total_height_array()

