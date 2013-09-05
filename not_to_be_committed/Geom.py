import vtk
def Create_Topo(Slope,Plane)
	ugrid = vtk.vtkUnstructuredGrid()
	gridreader=vtk.vtkUnstructuredGridReader()
	gridreader.SetFileName(Slope)
	gridreader.Update()
	ugrid = gridreader.GetOutput()
	GeomFilt1 = vtk.vtkGeometryFilter()
	GeomFilt1.SetInput(ugrid)
	GeomFilt1.Update()
	x = GeomFilt1.GetOutput()

	u = vtk.vtkUnstructuredGrid()
	bgridreader=vtk.vtkXMLUnstructuredGridReader()
	bgridreader.SetFileName(Plane)
	bgridreader.Update()
	u = bgridreader.GetOutput() 
	GeomFilt2 = vtk.vtkGeometryFilter()
	GeomFilt2.SetInput(u)
	GeomFilt2.Update()
	y = GeomFilt2.GetOutput()

	append = vtk.vtkAppendPolyData()
	append.AddInput(x)
	append.AddInput(y)
	data = append.GetOutput()
	
	d = vtk.vtkDelaunay3D()
	d.SetInput(data)
	d.Update
	d.BoundingTriangulationOff()  
	d.SetTolerance(0.01)
	d.SetAlpha(0)
	d.Update()
	z = d.GetOutput()
	return z

if __name__ == '__main__':
	z = Create_topo()
	writer = vtk.vtkGenericDataObjectWriter()
	writer.SetFileName("test31.vtu")
	writer.SetInput(z)
	writer.Update()
	writer.Write()


