import vtk
import sys
sys.path.append('<<fluidity_source_path>>/python')
import vtktools

def Creating_z(Plane,Slope,Sediment,Start_time,End_time,Time_step):

	vtuObject = vtktools.vtu(Plane)
	vtuObject.GetFieldNames()
	gradient = vtuObject.GetScalarField('u')
	ugrid = vtk.vtkUnstructuredGrid()
	gridreader=vtk.vtkXMLUnstructuredGridReader()
	gridreader.SetFileName(Plane)
	gridreader.Update()
	ugrid = gridreader.GetOutput()
	points = ugrid.GetPoints()

	nPoints = ugrid.GetNumberOfPoints()
	for p in range(0,nPoints):
		x = (points.GetPoint(p)[:2] + (gradient[p],))
		points.SetPoint(p,x)
		#print x
    
	ugrid.Update()
###################################################################################################################
	t = Start_time
	dt = Time_step
	et = End_time
	while t <= et:

		Import = Sediment + str(t) +'000000.vtu'
		NewSave = Sediment + str(t) + '_sed_slope.pvd'
		vtuObjectSed = vtktools.vtu(Import)
		vtuObjectSed.GetFieldNames()
		gradientSed = vtuObjectSed.GetScalarField('u')
		sedgrid = vtk.vtkUnstructuredGrid()
		sedgridreader=vtk.vtkXMLUnstructuredGridReader()
		sedgridreader.SetFileName(Import)
		sedgridreader.Update()
		sedgrid = sedgridreader.GetOutput()
		s = sedgrid.GetPoints()
	
		for p in range(0,nPoints):
			x = ((s.GetPoint(p)[0],) + (s.GetPoint(p)[1],) + ((gradientSed[p]+gradient[p]),))
			s.SetPoint(p,x)
			#print x
			
		#print t, x
#		vtuObjectSed.AddScalarField('t'),
		writer = vtk.vtkUnstructuredGridWriter()
		writer.SetFileName(NewSave)
		writer.SetInput(sedgrid)
		writer.Update()
		writer.Write()
		t += dt
	writer = vtk.vtkUnstructuredGridWriter()
	writer.SetFileName(Slope)
	writer.SetInput(ugrid)
	writer.Update()
	writer.Write()

