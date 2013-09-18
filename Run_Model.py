from sediment import *
from run_sed import*
from converting_z import *
from Extrude import *
import libspud
import sys
import argparse
sys.path.append('<<fluidity_source_path>>/python')
import vtktools

def Main1():
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

#if __name__ == "__Main__":

fname , verbose, new = Main1()

sediment = new[:-4]
plane = new[:-4] + '000000.vtu'
slope = new[:-4] + '_slope.pvd'
extrusion = new[:-4] + '_extrusion.vtu'
model = new[:-4] + '_model.vtu'

NewFile = New_File(new)

start, end, time_step, mesh_int, alpha, initial_conditions = Parameters(fname)

tha, th, sha, sh, topha, toph = set_up_model(start, end, time_step, mesh_int, alpha, initial_conditions, sediment, verbose)

NewFile << toph

Creating_z(plane, slope, sediment, start, end, time_step)

Extrude(slope, extrusion, plane, model, sediment, start, end, time_step, mesh_int)

#writer = vtk.vtkGenericDataObjectWriter()
#writer.SetFileName(model)
#writer.SetInput(Z)
#writer.Update()
#writer.Write()

