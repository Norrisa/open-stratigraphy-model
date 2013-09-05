import vtk
import sys
sys.path.append('<<fluidity_source_path>>/python')
import vtktools

def Creating_z(Plane,Slope):
	print Plane
	print Slope
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
    
	ugrid.Update()

	writer = vtk.vtkUnstructuredGridWriter()
	writer.SetFileName(Slope)
	writer.SetInput(ugrid)
	writer.Update()
	writer.Write()

