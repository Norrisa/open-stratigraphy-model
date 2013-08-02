from sediment import *
import re
import sys

#should be an osml file
infile = open(sys.argv[1],'r')
lines = infile.readlines()
infile.close()

#Remove the top and bottom lines of the file
del lines[:7]
del lines[11:]
#Remove the lines that do not have data in that is needed in the equation
del lines[9]
del lines[7]
del lines[6]
del lines[4]
del lines[3]

#Extract the relevent information
start_string = str(lines[0])
startg = re.search('>(.+?)<', start_string)
end_string = str(lines[1])
endg = re.search('>(.+?)<', end_string)
time_step_string = str(lines[2])
time_stepg = re.search('>(.+?)<', time_step_string)
integer_string = str(lines[3])
integerg = re.search('>(.+?)<', integer_string)
alpha_string = str(lines[4])
alphag = re.search('>(.+?)<', alpha_string)
initial_conditions_string = str(lines[5])
initial_conditionsg = re.search('>(.+?)<', initial_conditions_string)

#Convert it to the desired data type
start = float(startg.group(1)) 
end = float(endg.group(1)) 
time_step = float(time_stepg.group(1)) 
integer = int(integerg.group(1)) 
alpha = float(alphag.group(1)) 
initial_conditions = str(initial_conditionsg.group(1)) 


#create a simple testcase
model = SedimentModel()
mesh = UnitSquareMesh(integer,integer)
model.set_mesh(mesh)
init_cond = Expression(initial_conditions) # simple slope
init_sed = Expression('x[0]') # this gives
# total of above gives a slope of 0 to 2 (over the unit square)
model.set_initial_conditions(init_cond,init_sed)
model.set_end_time(end)
model.set_diffusion_coeff(alpha)
model.init()
model.solve()
# answer should be 1 everywhere
plot(model.get_total_height(),interactive=True)
print model.get_total_height_array()


