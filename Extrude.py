import vtk
import dolfin
def Extrude(Slope,Extrusion,Plane,Model):
	ugrid = vtk.vtkUnstructuredGrid()
	gridreader=vtk.vtkUnstructuredGridReader()
	gridreader.SetFileName(Slope) #.pvd
	gridreader.Update()
	ugrid = gridreader.GetOutput()
	x = ugrid.GetPoints()
	GeomFilt2 = vtk.vtkGeometryFilter()
	GeomFilt2.SetInput(ugrid)
	GeomFilt2.Update()
	y = GeomFilt2.GetOutput()

	
	Extrude = vtk.vtkLinearExtrusionFilter()
	Extrude.SetInput(y)
	Extrude.SetExtrusionTypeToVectorExtrusion()	
	Extrude.SetVector(0,0,-1)
	hello = Extrude.GetOutput()
	print 'hello = ', hello

	newgrid = vtk.vtkPolyData()
	newgrid = hello
	newgrid.Update()
#	writer = vtk.vtkGenericDataObjectWriter()
#	writer.SetFileName(Extrusion) #.vtu
#	writer.SetInput(hello)
#	writer.Update()
#	writer.Write()


#	gridreader2=vtk.vtkPolyDataReader()
#	gridreader2.SetFileName(Extrusion) #same as above
#	gridreader2.Update()
#	newgrid = gridreader2.GetOutput()
#	print newgrid


	u = vtk.vtkUnstructuredGrid()
	gridreader3=vtk.vtkXMLUnstructuredGridReader()
	gridreader3.SetFileName(Plane) # 000000.vtu
	gridreader3.Update()
	u = gridreader3.GetOutput()
	print u 


	ExtrudedPoints = newgrid.GetPoints()
	PlanePoints = u.GetPoints()
	nPoints = newgrid.GetNumberOfPoints()
	Begin  = nPoints/2
	PlaneList = []
	counter = 0
	uPoints = u.GetPoints()

	for p in range(Begin,nPoints):
		y = uPoints.GetPoint(counter)[2:]
		x = ExtrudedPoints.GetPoint(p)[:2] + y
		ExtrudedPoints.SetPoint(p,x)
		counter =+ 1
		print 'x = ' , x
	
	for p in range(0,nPoints):
		x = ExtrudedPoints.GetPoint(p)
		print x
	newgrid.Update()
	return newgrid

if __name__ == '__Main__':

	writer = vtk.vtkGenericDataObjectWriter()
	writer.SetFileName(Model) # .vtu
	writer.SetInput(newgrid)
	writer.Update()
	writer.Write()





