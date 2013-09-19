import vtk
import dolfin
def Extrude(Slope,Extrusion,Plane,Model,Sediment,Start_time,End_time,Time_step,Mesh):
	ugrid1 = vtk.vtkUnstructuredGrid()         #1.import sloped sediment and change to polydata
	gridreader1=vtk.vtkUnstructuredGridReader()
	gridreader1.SetFileName(Slope) #.pvd
	gridreader1.Update()
	ugrid1 = gridreader1.GetOutput()
	GeomFilt1 = vtk.vtkGeometryFilter()
	GeomFilt1.SetInput(ugrid1)
	GeomFilt1.Update()
	y1 = GeomFilt1.GetOutput()

	
	Extrude = vtk.vtkLinearExtrusionFilter()         #2. extrude the polydata and save it again as polydata
	Extrude.SetInput(y1)
	Extrude.SetExtrusionTypeToVectorExtrusion()	
	Extrude.SetVector(0,0,-1)
	PreliminaryExtrusion = Extrude.GetOutput()

	PE = vtk.vtkPolyData()
	PE = PreliminaryExtrusion
	PE.Update()

	ugrid2 = vtk.vtkUnstructuredGrid()                      #3. import in the top surface of the sediment below
	gridreader2=vtk.vtkXMLUnstructuredGridReader()
	gridreader2.SetFileName(Plane) # 000000.vtu
	gridreader2.Update()
	ugrid2 = gridreader2.GetOutput()

	ExtrudedPoints = PE.GetPoints()               #4. take points from the extruded polydata
	PlanePoints = ugrid2.GetPoints()                        #5. get points from surface below
	nPoints = PE.GetNumberOfPoints()              #6. for first half of points determine if above or below last surface
	Begin  = nPoints/2                                 #7. if below set as the same as bottom surface (slightly above?)
	                                              #8. set second half 
	counter = 0
	uPoints = ugrid2.GetPoints()

	for p in range(Begin,nPoints):
		y = uPoints.GetPoint(counter)[2:]
		x = ExtrudedPoints.GetPoint(p)[:2] + y
		ExtrudedPoints.SetPoint(p,x)
		counter += 1

	PE.Update()

	writer = vtk.vtkGenericDataObjectWriter()
	writer.SetFileName(Model)
	writer.SetInput(PE)
	writer.Update()
	writer.Write()
#################################################################################################################
		


	t = Start_time
	dt = Time_step
	ET = End_time
	et = ET-1
	Save = Sediment + str(t) +'000000.vtu'
	Import = Sediment + str(t)+ '_sed_slope.pvd'
	NewSave = Sediment + str(t)+ 'extruded_sed_slope.pvd'

	SedimentGrid1 = vtk.vtkUnstructuredGrid()         #1.import sloped sediment and change to polydata
	SedimentGridreader1=vtk.vtkUnstructuredGridReader()
	SedimentGridreader1.SetFileName(Import) #.pvd
	SedimentGridreader1.Update()
	SedimentGrid1 = SedimentGridreader1.GetOutput()
	GeomFilt2 = vtk.vtkGeometryFilter()
	GeomFilt2.SetInput(SedimentGrid1)
	GeomFilt2.Update()
	ExtrudeInput1 = GeomFilt2.GetOutput()

	ExtrudeSed1 = vtk.vtkLinearExtrusionFilter()         #2. extrude the polydata and save it again as polydata
	ExtrudeSed1.SetInput(ExtrudeInput1)
	ExtrudeSed1.SetExtrusionTypeToVectorExtrusion()	
	ExtrudeSed1.SetVector(0,0,-1)
	PreliminarySedExtrusion1 = ExtrudeSed1.GetOutput()

	PSE1 = vtk.vtkPolyData()
	PSE1 = PreliminarySedExtrusion1
	PSE1.Update()
		
	PreSurface1 = vtk.vtkUnstructuredGrid()                      #3. import in the top surface of the sediment below
	PSreader1=vtk.vtkGenericDataObjectReader()
	PSreader1.SetFileName(Slope) # 000000.vtu
	PSreader1.Update()
	PreSurface1 = PSreader1.GetOutput()
	ExtrudedSedPoints1 = PSE1.GetPoints()               #4. take points from the extruded polydata
	PSPoints1 = PreSurface1.GetPoints()                        #5. get points from surface below
	SedPoints1 = PSE1.GetNumberOfPoints()          #6. for first half of points determine if above or below last surface
	BeginSed1  = nPoints/2 
	EndSed1 = BeginSed1 - 1                             #7. if below set as the same as bottom surface (slightly above?
	sedcounter1 = 0					 #8. set second half 
	sedcounter2 = BeginSed1
			
	for p in range(BeginSed1,SedPoints1):
		y = PSPoints1.GetPoint(sedcounter1)[2:]
		x = ExtrudedSedPoints1.GetPoint(p)[:2] + y
		ExtrudedSedPoints1.SetPoint(p,x)
		sedcounter1 += 1
			
	writer = vtk.vtkGenericDataObjectWriter()
	writer.SetFileName(NewSave)
	writer.SetInput(PSE1)
	writer.Update()
	writer.Write()
	#print 'a'
#####################################################################################################################


	while t <= et:
		t += dt
		pre = t -1
		Previous = Sediment +str(pre) + '_sed_slope.pvd'  
		PreviousSave = Sediment + str(pre)+ 'extruded_sed_slope.pvd'
		Import = Sediment + str(t)+ '_sed_slope.pvd'
		NewSave = Sediment + str(t)+ 'extruded_sed_slope.pvd'
		
		SedimentGrid2 = vtk.vtkUnstructuredGrid()         
		SedimentGridreader2=vtk.vtkUnstructuredGridReader()
		SedimentGridreader2.SetFileName(Import) #.pvd
		SedimentGridreader2.Update()
		SedimentGrid2 = SedimentGridreader2.GetOutput()
		GeomFilt3 = vtk.vtkGeometryFilter()
		GeomFilt3.SetInput(SedimentGrid2)
		GeomFilt3.Update()
		ExtrudeInput = GeomFilt3.GetOutput()		


		ExtrudeInput2 = GeomFilt3.GetOutput()
		ExtrudeSed2 = vtk.vtkLinearExtrusionFilter()         
		ExtrudeSed2.SetInput(ExtrudeInput2)
		ExtrudeSed2.SetExtrusionTypeToVectorExtrusion()	
		ExtrudeSed2.SetVector(0,0,-1)
		PreliminarySedExtrusion2 = ExtrudeSed2.GetOutput()
		
		PSE2 = vtk.vtkPolyData()
		PSE2 = PreliminarySedExtrusion2
		PSE2.Update()

		PreSurface2 = vtk.vtkUnstructuredGrid()                     
		PSreader2=vtk.vtkGenericDataObjectReader()
		PSreader2.SetFileName(PreviousSave) # 000000.vtu
		PSreader2.Update()
		PreSurface2 = PSreader2.GetOutput()

		Append = vtk.vtkAppendPolyData()

		Append.AddInput(PreSurface2)
		Append.AddInput(PSE2)

		DD = Append.GetOutput()
		DD.Update()

		ExtrudedSedPoints = PSE2.GetPoints()               
		PSPoints = PreSurface2.GetPoints()                       
		SedPoints = PSE2.GetNumberOfPoints()         
		BeginSed  = nPoints/2 
		EndSed = BeginSed - 1                             
		sedcounter3 = 0					
		sedcounter4 = BeginSed
		Data = DD.GetPoints()
		
		mesh = Mesh
		m = (mesh+1)**2
		c = t
		#print c, type(c)
		while c != 0:
			#print c, type(c)
			c = (c -1)
			#print c, type(c)
			e = int((c*m)*2)
			ee = int(e + m)
			#print 'c'
			for p in range(e,ee):
				A = Data.GetPoint(p+(2*m))[2:]             #New sediment height
				B = Data.GetPoint(p)[2:]			# old sediment height
				C = Data.GetPoint(p+m)[2:]          # old sediment bottom
				#print t
				if A < B:                                        #If new sediment height is less than old sediment height
					y = (Data.GetPoint(p)[:2] + Data.GetPoint(p+(2*m))[2:])
					#print 'y = ', y                                 #change the old sediment height
					Data.SetPoint(p,y)
	
				if A < C:
					x = Data.GetPoint(p+m)[:2] + Data.GetPoint(p)[2:]
					Data.SetPoint((p+m),x)
		f = int((t*m)*2+m)
		print t
		print 'f is ', f
		ff = int(f + m)
		print 'ff is ', ff
		print Data.GetPoint(0)
		for p in range(f,ff):
			print 'a'
			y = Data.GetPoint((p-3*m))[2:]
			print 'b'
			x = Data.GetPoint(p)[:2] + y
			print'c'
			Data.SetPoint(p,x)
			print 'd'


				

		writer = vtk.vtkGenericDataObjectWriter()
		writer.SetFileName(NewSave)
		writer.SetInput(DD)
		writer.Update()
		writer.Write()
		#print 'b'





#should grab points from the surface below








































#	while t <= et:
#		t += dt
#		pre = t -1
#		Save = Sediment + str(t) +'000000.vtu'
#		Import = Sediment + str(t)+ '_sed_slope.pvd'
#		Previous = Sediment +str(pre) + '_sed_slope.pvd'  
#		NewSave = Sediment + str(t)+ 'extruded_sed_slope.pvd'
#
#		SedimentGrid = vtk.vtkUnstructuredGrid()         #1.import sloped sediment and change to polydata
#		SedimentGridreader=vtk.vtkUnstructuredGridReader()
#		SedimentGridreader.SetFileName(Import) #.pvd
##		SedimentGridreader.Update()
#		SedimentGrid = SedimentGridreader.GetOutput()
#		GeomFilt3 = vtk.vtkGeometryFilter()
#		GeomFilt3.SetInput(SedimentGrid)
#		GeomFilt3.Update()
#		ExtrudeInput = GeomFilt3.GetOutput()
#
#		ExtrudeSed = vtk.vtkLinearExtrusionFilter()         #2. extrude the polydata and save it again as polydata
#		ExtrudeSed.SetInput(ExtrudeInput)
#		ExtrudeSed.SetExtrusionTypeToVectorExtrusion()	
#		ExtrudeSed.SetVector(0,0,-1)
#		PreliminarySedExtrusion = ExtrudeSed.GetOutput()
#
#		PSE = vtk.vtkPolyData()
#		PSE = PreliminarySedExtrusion
#		PSE.Update()
#		
#		PreSurface = vtk.vtkUnstructuredGrid()                      #3. import in the top surface of the sediment below
#		PSreader=vtk.vtkGenericDataObjectReader()
#		PSreader.SetFileName(Previous) # 000000.vtu
#		PSreader.Update()
#		PreSurface = PSreader.GetOutput()
#
#		ExtrudedSedPoints = PSE.GetPoints()               #4. take points from the extruded polydata
#		PSPoints = PreSurface.GetPoints()                        #5. get points from surface below
#		SedPoints = PE.GetNumberOfPoints()          #6. for first half of points determine if above or below last surface
#		BeginSed  = nPoints/2 
#		EndSed = BeginSed - 1                             #7. if below set as the same as bottom surface (slightly above?
#		sedcounter3 = 0					 #8. set second half 
#		sedcounter4 = BeginSed
#
##this is to sort out extrusions for the previous timesteps		
#		for p in range(0,EndSed):
#			
#			a = ExtrudedSedPoints.GetPoint(p)[2:]             #New sediment height
#			print a
#			b = PSPoints.GetPoint(p)[2:]			# old sediment height
#			c = PSPoints.GetPoint(sedcounter4)[2:]          # old sediment bottom
#			
#			if a < b:                                        #If new sediment height is less than old sediment height
#				y = (PSPoints.GetPoint(p)[:2], + ExtrudedSedPoints.GetPoint(p)[2:],)
#				print y                                 #change the old sediment height
#				PSPoints.SetPoint(p,y)
#
#			if a < c:
#				x = PSPoints.GetPoint(sedcounter4)[:2] + ExtrudedSedPoints.GetPoint(p)[2:]
#				PSPoints.SetPoint(sedcounter4,y)
#			y = PSPoints.GetPoint(counter)[2:]
#			x = ExtrudedSedPoints.GetPoint(p)[:2] + y
#			
#			sedcounter4 += 1
#
#		for p in range(BeginSed,SedPoints):
#			y = PSPoints.GetPoint(sedcounter3)[2:]
#			x = ExtrudedSedPoints.GetPoint(p)[:2] + y
#			ExtrudedSedPoints.SetPoint(p,x)
#			sedcounter3 += 1
#		
#		writer = vtk.vtkGenericDataObjectWriter()
#		writer.SetFileName(NewSave)
#		writer.SetInput(PSE)
#		writer.Update()
#		writer.Write()
##		
#		writer = vtk.vtkGenericDataObjectWriter()
#		writer.SetFileName('blob.pvd')
#		writer.SetInput(PSE)
#		writer.Update()
#		writer.Write()
#
#	PE.Update()
#	return PE
#
#if __name__ == '__Main__':
#
#	writer = vtk.vtkGenericDataObjectWriter()
#	writer.SetFileName(Model) # .vtu
#	writer.SetInput(PE)
#	writer.Update()
#	writer.Write()
#




