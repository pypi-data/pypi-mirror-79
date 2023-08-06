from agrossuite import agros

from .scenario import AgrosTestCase


class TestAcousticHarmonicPlanar(AgrosTestCase):
    def setUp(self):  
        # model
        problem = agros.problem(clear = True)
        problem.coordinate_type = "planar"
        problem.mesh_type = "triangle"
        problem.frequency = 2000
        
        # fields
        self.acoustic = problem.field("acoustic")
        self.acoustic.analysis_type = "harmonic"
        self.acoustic.number_of_refinements = 2
        self.acoustic.polynomial_order = 2
        self.acoustic.solver = "linear"
        
        self.acoustic.add_boundary("Source", "acoustic_pressure", {"acoustic_pressure_real" : 0.01, "acoustic_pressure_imag" : 0})
        self.acoustic.add_boundary("Wall", "acoustic_normal_acceleration", {"acoustic_normal_acceleration_real" : 0, "acoustic_normal_acceleration_imag" : 0})
        self.acoustic.add_boundary("Matched boundary", "acoustic_impedance", {"acoustic_impedance" : 1.25*343})
        
        self.acoustic.add_material("Air", {"acoustic_speed" : 343, "acoustic_density" : 1.25})
        
        # geometry
        geometry = problem.geometry()
        
        # edges
        geometry.add_edge(-0.4, 0.05, 0.1, 0.2, boundaries = {"acoustic" : "Matched boundary"})
        geometry.add_edge(0.1, -0.2, -0.4, -0.05, boundaries = {"acoustic" : "Matched boundary"})
        geometry.add_edge(-0.4, 0.05, -0.4, -0.05, boundaries = {"acoustic" : "Matched boundary"})
        geometry.add_edge(-0.18, -0.06, -0.17, -0.05, segments = 6, boundaries = {"acoustic" : "Source"}, angle=90)
        geometry.add_edge(-0.17, -0.05, -0.18, -0.04, segments = 6, boundaries = {"acoustic" : "Source"}, angle=90)
        geometry.add_edge(-0.18, -0.04, -0.19, -0.05, segments = 6, boundaries = {"acoustic" : "Source"}, angle=90)
        geometry.add_edge(-0.19, -0.05, -0.18, -0.06, segments = 6, boundaries = {"acoustic" : "Source"}, angle=90)
        geometry.add_edge(0.1, -0.2, 0.1, 0.2, segments = 15, boundaries = {"acoustic" : "Matched boundary"}, angle=90)
        geometry.add_edge(0.03, 0.1, -0.04, -0.05, segments = 10, boundaries = {"acoustic" : "Wall"}, angle=90)
        geometry.add_edge(-0.04, -0.05, 0.08, -0.04, boundaries = {"acoustic" : "Wall"})
        geometry.add_edge(0.08, -0.04, 0.03, 0.1, boundaries = {"acoustic" : "Wall"})
        
        # labels
        geometry.add_label(-0.0814934, 0.0707097, materials = {"acoustic" : "Air"})
        geometry.add_label(-0.181474, -0.0504768)
        geometry.add_label(0.0314514, 0.0411749)
        
        # solve problem
        self.computation = problem.computation()
        self.computation.solve()
        
    def test_values(self):
        # solution
        solution = self.computation.solution("acoustic")
        
        # point value
        point = solution.local_values(-0.084614, 0.053416)
        self.value_test("Acoustic pressure", point["p"], 0.003064)
        self.value_test("Acoustic pressure - real", point["pr"], 0.002322)
        self.value_test("Acoustic pressure - imag", point["pi"], 0.001999)
        self.value_test("Acoustic sound level", point["SPL"], 40.695085, 0.07)        
                        
        # volume integral
        volume = solution.volume_integrals([0])
        self.value_test("Volume acoustic pressure - real", volume["pr"], -1.915211e-5)
        self.value_test("Volume acoustic pressure - imag", volume["pi"], -1.918928e-5)
        
        # surface integral 
        surface = solution.surface_integrals([7])
        self.value_test("Surface acoustic pressure - real", surface["pr"], 3.079084e-4)
        self.value_test("Surface acoustic pressure - imag", surface["pi"], 4.437581e-5)      
        

class TestAcousticHarmonicAxisymmetric(AgrosTestCase):
    def setUp(self):         
        # model
        problem = agros.problem(clear = True)
        problem.coordinate_type = "axisymmetric"
        problem.mesh_type = "triangle"
        problem.frequency = 700
        
        # fields
        self.acoustic = problem.field("acoustic")
        self.acoustic.analysis_type = "harmonic"
        self.acoustic.number_of_refinements = 2
        self.acoustic.polynomial_order = 2
        self.acoustic.solver = "linear"
        
        self.acoustic.add_boundary("Wall", "acoustic_normal_acceleration", {"acoustic_normal_acceleration_real" : 0, "acoustic_normal_acceleration_imag" : 0})
        self.acoustic.add_boundary("Source acceleration", "acoustic_normal_acceleration", {"acoustic_normal_acceleration_real" : 10, "acoustic_normal_acceleration_imag" : 0})
        self.acoustic.add_boundary("Matched boundary", "acoustic_impedance", {"acoustic_impedance" : 1.25*343})
        self.acoustic.add_boundary("Source pressure", "acoustic_pressure", {"acoustic_pressure_real" : 0.2, "acoustic_pressure_imag" : 0})
            
        self.acoustic.add_material("Air", {"acoustic_density" : 1.25, "acoustic_speed" : 343})
        
        # geometry
        geometry = problem.geometry()
        
        # edges
        geometry.add_edge(0, 1.5, 1.05, 1.25, boundaries = {"acoustic" : "Wall"})
        geometry.add_edge(1.05, 1.25, 0.25, 0, boundaries = {"acoustic" : "Matched boundary"})
        geometry.add_edge(0.25, 0, 0, 0, boundaries = {"acoustic" : "Source acceleration"})
        geometry.add_edge(0, 0, 0, 0.7, boundaries = {"acoustic" : "Wall"})
        geometry.add_edge(0, 1, 0, 1.5, boundaries = {"acoustic" : "Wall"})
        geometry.add_edge(0, 0.7, 0.15, 0.85, segments = 7, boundaries = {"acoustic" : "Wall"}, angle=90)
        geometry.add_edge(0.15, 0.85, 0, 1, segments = 7, boundaries = {"acoustic" : "Wall"}, angle=90)
        geometry.add_edge(0.35, 1.15, 0.65, 1, boundaries = {"acoustic" : "Matched boundary"})
        geometry.add_edge(0.65, 1, 0.35, 0.9, boundaries = {"acoustic" : "Matched boundary"})
        geometry.add_edge(0.35, 1.15, 0.35, 0.9, boundaries = {"acoustic" : "Matched boundary"})
        geometry.add_edge(0.6, 1.2, 0.6, 1.25, boundaries = {"acoustic" : "Source pressure"})
        geometry.add_edge(0.6, 1.2, 0.65, 1.2, boundaries = {"acoustic" : "Source pressure"})
        geometry.add_edge(0.6, 1.25, 0.65, 1.2, boundaries = {"acoustic" : "Source pressure"})
        
        # labels
        geometry.add_label(0.163662, 0.383133, materials = {"acoustic" : "Air"})
        geometry.add_label(0.426096, 1.03031, materials = {"acoustic" : "none"})
        geometry.add_label(0.616273, 1.21617, materials = {"acoustic" : "none"})
        
        # solve problem
        self.computation = problem.computation()
        self.computation.solve()
        
    def test_values(self):
        # solution
        solution = self.computation.solution("acoustic")
                      
        # point value
        point = solution.local_values(0.259371, 0.876998)
        self.value_test("Acoustic pressure", point["p"], 0.49271)
        self.value_test("Acoustic pressure - real", point["pr"], 0.395866)
        self.value_test("Acoustic pressure - imag", point["pi"], 0.293348)
        self.value_test("Acoustic sound level", point["SPL"], 84.820922, 0.05)  

        # volume integral
        volume = solution.volume_integrals([0])
        self.value_test("Acoustic pressure - real", volume["pr"], -0.030632)
        self.value_test("Acoustic pressure - imag", volume["pi"], -0.010975)
        
        # surface integral 
        surface = solution.surface_integrals([0])
        self.value_test("Acoustic pressure - real", surface["pr"], 0.196756)
        self.value_test("Acoustic pressure - imag", surface["pi"], -0.324708)   


class TestAcousticTransientPlanar(AgrosTestCase):
    def setUp(self):          
        # problem
        problem = agros.problem(clear = True)
        problem.coordinate_type = "planar"
        problem.mesh_type = "triangle"
        #problem.time_step_method = "fixed"
        problem.time_method_tolerance = 1
        problem.time_total = 0.001
        problem.time_steps = 250
        
        # fields
        # acoustic
        self.acoustic = problem.field("acoustic")
        self.acoustic.analysis_type = "steadystates"
        self.acoustic.transient_initial_condition = 0
        self.acoustic.number_of_refinements = 0
        self.acoustic.polynomial_order = 2
        self.acoustic.solver = "linear"
        self.acoustic.adaptivity_type = "disabled"
        
        # boundaries
        self.acoustic.add_boundary("Matched bundary", "acoustic_impedance", {"acoustic_impedance" : 345*1.25 })
        self.acoustic.add_boundary("Source", "acoustic_pressure", {"acoustic_pressure_real" : { "expression" : "sin(2*pi*(time/(1.0/1000)))" }, "acoustic_pressure_time_derivative" : { "expression" : "2*pi*(1.0/(1.0/1000))*cos(2*pi*(time/(1.0/1000)))" }})
        self.acoustic.add_boundary("Hard wall", "acoustic_normal_acceleration", {"acoustic_normal_acceleration_real" : 0})
        self.acoustic.add_boundary("Soft wall", "acoustic_pressure", {"acoustic_pressure_real" : 0, "acoustic_pressure_time_derivative" : 0})
        
        # materials
        self.acoustic.add_material("Air", {"acoustic_density" : 1.25, "acoustic_speed" : 343})
        
        # geometry
        geometry = problem.geometry()
        geometry.add_edge(-0.4, 0.05, 0.1, 0.2, boundaries = {"acoustic" : "Matched bundary"})
        geometry.add_edge(0.1, -0.2, -0.4, -0.05, boundaries = {"acoustic" : "Matched bundary"})
        geometry.add_edge(-0.4, 0.05, -0.4, -0.05, boundaries = {"acoustic" : "Soft wall"})
        geometry.add_edge(-0.18, -0.06, -0.17, -0.05, angle = 90, boundaries = {"acoustic" : "Source"})
        geometry.add_edge(-0.17, -0.05, -0.18, -0.04, angle = 90, boundaries = {"acoustic" : "Source"})
        geometry.add_edge(-0.18, -0.04, -0.19, -0.05, angle = 90, boundaries = {"acoustic" : "Source"})
        geometry.add_edge(-0.19, -0.05, -0.18, -0.06, angle = 90, boundaries = {"acoustic" : "Source"})
        geometry.add_edge(0.1, -0.2, 0.1, 0.2, angle = 90, segments = 6, boundaries = {"acoustic" : "Matched bundary"})
        geometry.add_edge(0.03, 0.1, -0.04, -0.05, angle = 90, segments = 6, boundaries = {"acoustic" : "Hard wall"})
        geometry.add_edge(-0.04, -0.05, 0.08, -0.04, boundaries = {"acoustic" : "Hard wall"})
        geometry.add_edge(0.08, -0.04, 0.03, 0.1, boundaries = {"acoustic" : "Hard wall"})
        
        geometry.add_label(-0.0814934, 0.0707097, area = 10e-05, materials = {"acoustic" : "Air"})
        geometry.add_label(-0.181474, -0.0504768, materials = {"acoustic" : "none"})
        geometry.add_label(0.0314514, 0.0411749, materials = {"acoustic" : "none"})
        
        # solve problem
        self.computation = problem.computation()
        self.computation.solve()

    def disabled_test_values(self):
        # solution
        solution = self.computation.solution("acoustic")
                                      
        # point 
        point = solution.local_values(0.042132, -0.072959)
        self.value_test("Acoustic pressure", point["pr"], 0.200436)
        self.value_test("Acoustic sound level", point["SPL"], 80.018917)  

        # volume integral
        volume = solution.volume_integrals([0])
        self.value_test("Acoustic pressure - real", volume["pr"], -0.007303)
        
        # surface integral 
        surface = solution.surface_integrals([0])
        self.value_test("Acoustic pressure - real", surface["pr"], 0.068864)


class TestAcousticTransientAxisymmetric(AgrosTestCase):
    def setUp(self):                 
        # problem
        problem = agros.problem(clear = True)
        problem.coordinate_type = "axisymmetric"
        problem.mesh_type = "triangle"
        problem.time_step_method = "fixed"
        problem.time_method_order = 2
        problem.time_total = 0.008
        problem.time_steps = 200
        
        # fields
        # acoustic
        self.acoustic = problem.field("acoustic")
        self.acoustic.analysis_type = "steadystate"
        self.acoustic.transient_initial_condition = 0
        self.acoustic.number_of_refinements = 2
        self.acoustic.polynomial_order = 2
        self.acoustic.adaptivity_type = "disabled"
        self.acoustic.solver = "linear"
        
        # boundaries
        self.acoustic.add_boundary("Wall", "acoustic_normal_acceleration", {"acoustic_normal_acceleration_real" : 0})
        self.acoustic.add_boundary("Source", "acoustic_pressure", {"acoustic_pressure_real" : { "expression" : "sin(2*pi*(time/(1.0/500)))" }, "acoustic_pressure_time_derivative" : { "expression" : "2*pi*(1.0/(1.0/500))*cos(2*pi*(time/(1.0/500)))" }})
        self.acoustic.add_boundary("Matched boundary", "acoustic_impedance", {"acoustic_impedance" : { "expression" : "345*1.25" }})
        self.acoustic.add_boundary("Pressure", "acoustic_pressure", {"acoustic_pressure_real" : 0, "acoustic_pressure_time_derivative" : 0})
        
        # materials
        self.acoustic.add_material("Air", {"acoustic_density" : 1.25, "acoustic_speed" : 343})
        
        # geometry
        geometry = problem.geometry()
        geometry.add_edge(0, -0.8, 0.5, -1.05, boundaries = {"acoustic" : "Wall"})
        geometry.add_edge(0.5, -1.05, 0.6, -1.05, boundaries = {"acoustic" : "Source"})
        geometry.add_edge(0.6, -1.05, 0.9, -0.55, boundaries = {"acoustic" : "Wall"})
        geometry.add_edge(0.2, -0.25, 0.9, -0.55, angle = 60, boundaries = {"acoustic" : "Wall"})
        geometry.add_edge(0.5, 0.15, 0.2, -0.25, angle = 60, boundaries = {"acoustic" : "Wall"})
        geometry.add_edge(0.5, 0.15, 0.65, 0.65, boundaries = {"acoustic" : "Wall"})
        geometry.add_edge(0.65, 0.65, 1.5, 1.2, boundaries = {"acoustic" : "Wall"})
        geometry.add_edge(1.5, 1.2, 0, 1.2, angle = 90, boundaries = {"acoustic" : "Matched boundary"})
        geometry.add_edge(0, 1.2, 0, 1, boundaries = {"acoustic" : "Wall"})
        geometry.add_edge(0, 1, 0.2, 0.55, boundaries = {"acoustic" : "Wall"})
        geometry.add_edge(0.2, 0.55, 0, -0.8, boundaries = {"acoustic" : "Wall"})
        geometry.add_edge(0.4, 0.8, 0.5, 0.9, angle = 90, boundaries = {"acoustic" : "Pressure"})
        geometry.add_edge(0.5, 0.9, 0.4, 1, angle = 90, boundaries = {"acoustic" : "Pressure"})
        geometry.add_edge(0.3, 0.9, 0.4, 0.8, angle = 90, boundaries = {"acoustic" : "Pressure"})
        geometry.add_edge(0.4, 1, 0.3, 0.9, angle = 90, boundaries = {"acoustic" : "Pressure"})
        
        geometry.add_label(0.663165, 1.16386, materials = {"acoustic" : "Air"})
        geometry.add_label(0.387614, 0.929226, materials = {"acoustic" : "none"})
        
        # solve problem
        self.computation = problem.computation()
        self.computation.solve()

    def disabled_test_values(self):
        # solution
        solution = self.computation.solution("acoustic")
               
        # point value
        point = solution.local_values(0.413503,0.499528)
        self.value_test("Acoustic pressure", point["pr"], 0.106095)
        self.value_test("Acoustic sound level", point["SPL"], 74.49331591294518)  

        # volume integral
        volume = solution.volume_integrals([0])
        self.value_test("Acoustic pressure - volume", volume["pr"], -0.22339)
                        
        # surface integral 
        surface = solution.surface_integrals([0])
        self.value_test("Acoustic pressure - surface", surface["pr"], -0.13398, 0.04)
