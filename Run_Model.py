from sediment import *
from run_sed import*
from Geom import*
from converting_z import *
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

plane = new[:-4] + '000000.vtu'
slope = new[:-4] + 'slope.pvd'
Model = new[:-4] + '_model.vtu'

NewFile = New_File(new)

start, end, time_step, mesh_int, alpha, initial_conditions = Parameters(fname)

tha, th, sha, sh, topha, toph = set_up_model(start, end, time_step, mesh_int, alpha, initial_conditions, verbose)

NewFile << toph

Creating_z(plane, slope)

Z = Create_Topo(slope,plane)

writer = vtk.vtkGenericDataObjectWriter()
writer.SetFileName(Model)
writer.SetInput(Z)
writer.Update()
writer.Write()

