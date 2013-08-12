import re
import sys
import libspud
import unittest
sys.path.insert(0,"../")
from sediment import *
from run_sed import *

class run_sed(unittest.TestCase):  #very large input
	def test1(self):
		start, end, time_step, mesh_int, alpha, initial_conditions = Parameters('test1.osml')
		self.assertEqual(start,0)
		self.assertEqual(end,10)
		self.assertEqual(time_step,1)
		self.assertEqual(mesh_int,10)
		self.assertEqual(alpha,10000)
		self.assertEqual(initial_conditions,'x[0]')
	def test2(self):   #0's in all the times
		with self.assertRaises(SystemExit):
			set_up_model('test2.osml')

	def test3(self):
		with self.assertRaises(SystemExit):
			set_up_model('test3.osml')			
	def test4(self):
		answer = set_up_model('test4.osml')
		for i in answer:
			self.assert_(-1e-8 <i - 0.5 < 1e-8)


	def test5(self):
		with self.assertRaises(SystemExit):		
			set_up_model('test5.osml')
	def test6(self):
		answer = set_up_model('test6.osml')
		print answer
		expected = numpy.array([0,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0])
		for i in range(0,110,11):
			row = answer[i:i+11]
			self.assertAlmostEqual(numpy.allclose(row,expected),)

	def test7(self):
		#should be an osml file
		libspud.load_options('test7.osml')

		start = float(libspud.get_option('/diffusion_model/timestepping/start_time',))
		end = float(libspud.get_option('/diffusion_model/timestepping/end_time'))
		time_step = float(libspud.get_option('/diffusion_model/timestepping/timestep'))
		mesh_int = int(libspud.get_option('/diffusion_model/mesh/initial_mesh_size'))
		alpha = float(libspud.get_option('/diffusion_model/model_parameters/diffusion_coefficient'))
		initial_conditions = str(libspud.get_option('/diffusion_model/model_parameters/initial_conditions'))


		#create a simple testcase
		model = SedimentModel()
		mesh = UnitSquareMesh(mesh_int,mesh_int)
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
		answer = model.get_total_height_array()
		for i in answer:
			self.assert_(-1e-8 < i - 5.5 < 1e-8)



	def test8(self):
		#should be an osml file
		libspud.load_options('test8.osml')

		start = float(libspud.get_option('/diffusion_model/timestepping/start_time',))
		end = float(libspud.get_option('/diffusion_model/timestepping/end_time'))
		time_step = float(libspud.get_option('/diffusion_model/timestepping/timestep'))
		mesh_int = int(libspud.get_option('/diffusion_model/mesh/initial_mesh_size'))
		alpha = float(libspud.get_option('/diffusion_model/model_parameters/diffusion_coefficient'))
		initial_conditions = str(libspud.get_option('/diffusion_model/model_parameters/initial_conditions'))

		#create a simple testcase
		model = SedimentModel()
		mesh = UnitSquareMesh(mesh_int,mesh_int)
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
		answer = model.get_total_height_array()
		for i in answer:
			self.assert_(-1e-8 < i - 1 < 1e-8)


	def test9(self):
		#should be an osml file
		libspud.load_options('test9.osml')

		start = float(libspud.get_option('/diffusion_model/timestepping/start_time',))
		end = float(libspud.get_option('/diffusion_model/timestepping/end_time'))
		time_step = float(libspud.get_option('/diffusion_model/timestepping/timestep'))
		mesh_int = int(libspud.get_option('/diffusion_model/mesh/initial_mesh_size'))
		alpha = float(libspud.get_option('/diffusion_model/model_parameters/diffusion_coefficient'))
		initial_conditions = str(libspud.get_option('/diffusion_model/model_parameters/initial_conditions'))

		#create a simple testcase
		model = SedimentModel()
		mesh = UnitSquareMesh(mesh_int,mesh_int)
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
		answer = model.get_total_height_array()

	def test10(self):
		with self.assertRaises(SystemExit):
			#should be an osml file
			libspud.load_options('test10.osml')
	
			start = float(libspud.get_option('/diffusion_model/timestepping/start_time',))
			end = float(libspud.get_option('/diffusion_model/timestepping/end_time'))
			time_step = float(libspud.get_option('/diffusion_model/timestepping/timestep'))
			mesh_int = int(libspud.get_option('/diffusion_model/mesh/initial_mesh_size'))
			alpha = float(libspud.get_option('/diffusion_model/model_parameters/diffusion_coefficient'))
			initial_conditions = str(libspud.get_option('/diffusion_model/model_parameters/initial_conditions'))
	
	
	
			#create a simple testcase
			model = SedimentModel()
			mesh = UnitSquareMesh(mesh_int,mesh_int)
			model.set_mesh(mesh)
			try:
				init_cond = Expression(initial_conditions) # simple slope
			except:
				print 'Your initial condition was not a function'
				sys.exit()
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
			answer = model.get_total_height_array()


	def test11(self):
		#should be an osml file
		libspud.load_options('test11.osml')

		start = float(libspud.get_option('/diffusion_model/timestepping/start_time',))
		end = float(libspud.get_option('/diffusion_model/timestepping/end_time'))
		time_step = float(libspud.get_option('/diffusion_model/timestepping/timestep'))
		mesh_int = int(libspud.get_option('/diffusion_model/mesh/initial_mesh_size'))
		alpha = float(libspud.get_option('/diffusion_model/model_parameters/diffusion_coefficient'))
		initial_conditions = str(libspud.get_option('/diffusion_model/model_parameters/initial_conditions'))


		#create a simple testcase
		model = SedimentModel()
		mesh = UnitSquareMesh(mesh_int,mesh_int)
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
		answer = model.get_total_height_array()


	def test12(self):
		with self.assertRaises(SystemExit):
			#should be an osml file
			try: 
				libspud.load_options('test12.osml')
			except:
				print "This file doesn't exist or is the wrong file type. It should be a .osml file"
				sys.exit()
			start = float(libspud.get_option('/diffusion_model/timestepping/start_time',))
			end = float(libspud.get_option('/diffusion_model/timestepping/end_time'))
			time_step = float(libspud.get_option('/diffusion_model/timestepping/timestep'))
			mesh_int = int(libspud.get_option('/diffusion_model/mesh/initial_mesh_size'))
			alpha = float(libspud.get_option('/diffusion_model/model_parameters/diffusion_coefficient'))
			initial_conditions = str(libspud.get_option('/diffusion_model/model_parameters/initial_conditions'))
	
	
	
			#create a simple testcase
			model = SedimentModel()
			mesh = UnitSquareMesh(mesh_int,mesh_int)
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
			answer = model.get_total_height_array()
	
	def test13(self):
		with self.assertRaises(SystemExit):
			#should be an osml file
			try: 
				libspud.load_options('test12.osml')
			except:
				print "This file doesn't exist or is the wrong file type. It should be a .osml file"
				sys.exit()

			start = float(libspud.get_option('/diffusion_model/timestepping/start_time',))
			end = float(libspud.get_option('/diffusion_model/timestepping/end_time'))
			time_step = float(libspud.get_option('/diffusion_model/timestepping/timestep'))
			mesh_int = int(libspud.get_option('/diffusion_model/mesh/initial_mesh_size'))
			alpha = float(libspud.get_option('/diffusion_model/model_parameters/diffusion_coefficient'))
			initial_conditions = str(libspud.get_option('/diffusion_model/model_parameters/initial_conditions'))
	
	
			#create a simple testcase
			model = SedimentModel()
			mesh = UnitSquareMesh(mesh_int,mesh_int)
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
			answer = model.get_total_height_array()


	def test14(self):
		with self.assertRaises(SystemExit):
			#should be an osml file
			libspud.load_options('test14.osml')
	
			start = float(libspud.get_option('/diffusion_model/timestepping/start_time',))
			end = float(libspud.get_option('/diffusion_model/timestepping/end_time'))
			time_step = float(libspud.get_option('/diffusion_model/timestepping/timestep'))
			mesh_int = int(libspud.get_option('/diffusion_model/mesh/initial_mesh_size'))
			alpha = float(libspud.get_option('/diffusion_model/model_parameters/diffusion_coefficient'))
			initial_conditions = str(libspud.get_option('/diffusion_model/model_parameters/initial_conditions'))
			if ((start-end) >= 0):
				print 'The start time is after the end time'
				sys.exit()
			elif (time_step == 0):
				print 'The time step cannot be 0'
				sys.exit()
		
	

			#create a simple testcase
			model = SedimentModel()
			mesh = UnitSquareMesh(mesh_int,mesh_int)
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
			answer = model.get_total_height_array()

	def test15(self):
		with self.assertRaises(SystemExit):
			#should be an osml file
			libspud.load_options('test15.osml')
	
			start = float(libspud.get_option('/diffusion_model/timestepping/start_time',))
			end = float(libspud.get_option('/diffusion_model/timestepping/end_time'))
			time_step = float(libspud.get_option('/diffusion_model/timestepping/timestep'))
			mesh_int = int(libspud.get_option('/diffusion_model/mesh/initial_mesh_size'))
			alpha = float(libspud.get_option('/diffusion_model/model_parameters/diffusion_coefficient'))
			initial_conditions = str(libspud.get_option('/diffusion_model/model_parameters/initial_conditions'))

			if ((start-end) >= 0):
				print 'The start time is after the end time'
				sys.exit()
			elif (time_step == 0):
				print 'The time step cannot be 0'
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
			model.set_end_time(end)
			model.set_diffusion_coeff(alpha)
			model.init()
			model.solve()
			# answer should be 1 everywhere
			plot(model.get_total_height(),interactive=True)
			answer = model.get_total_height_array()

	def test16(self):
		#should be an osml file
		libspud.load_options('test16.osml')

		start = float(libspud.get_option('/diffusion_model/timestepping/start_time',))
		end = float(libspud.get_option('/diffusion_model/timestepping/end_time'))
		time_step = float(libspud.get_option('/diffusion_model/timestepping/timestep'))
		mesh_int = int(libspud.get_option('/diffusion_model/mesh/initial_mesh_size'))
		alpha = float(libspud.get_option('/diffusion_model/model_parameters/diffusion_coefficient'))
		initial_conditions = str(libspud.get_option('/diffusion_model/model_parameters/initial_conditions'))


		#create a simple testcase
		model = SedimentModel()
		mesh = UnitSquareMesh(mesh_int,mesh_int)
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
		answer = model.get_total_height_array()
		for i in answer:
			self.assert_(-1e-8 < i - 1 < 1e-8)


	def test17(self):
		with self.assertRaises(SystemExit):
			#should be an osml file
			libspud.clear_options()
			try: 
				libspud.load_options('test17.osml')
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
			print start
			print end
			print time_step
			print mesh_int
			print alpha
			print initial_conditions

			
			#create a simple testcase
			model = SedimentModel()
			mesh = UnitSquareMesh(mesh_int,mesh_int)
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
			answer = model.get_total_height_array()

	def test18(self):
		with self.assertRaises(SystemExit):
			set_up_model('test1.osml')


if __name__ == "__main__":

    unittest.main()












