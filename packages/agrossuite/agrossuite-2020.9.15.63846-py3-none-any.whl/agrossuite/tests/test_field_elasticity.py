from agrossuite import agros

from .scenario import AgrosTestCase


class TestElasticityPlanar(AgrosTestCase):
    def setUp(self):  
        # model
        problem = agros.problem(clear = True)
        problem.coordinate_type = "planar"
        problem.mesh_type = "triangle"
        
        # fields
        self.elasticity = problem.field("elasticity")
        self.elasticity.analysis_type = "steadystate"
        self.elasticity.number_of_refinements = 3
        self.elasticity.polynomial_order = 3
        self.elasticity.solver = "linear"
        
        self.elasticity.add_boundary("Free", "elasticity_free_free", {"elasticity_force_x" : 0, "elasticity_force_y" : 0})
        self.elasticity.add_boundary("Fixed", "elasticity_fixed_fixed", {"elasticity_displacement_x" : 0, "elasticity_displacement_y" : 0})
        self.elasticity.add_boundary("Load", "elasticity_free_free", {"elasticity_force_x" : 0, "elasticity_force_y" : -1.2e4})
        
        self.elasticity.add_material("Material 1", {"elasticity_young_modulus" : 2e11, "elasticity_poisson_ratio" : 0.33, "elasticity_volume_force_x" : -1e6, "elasticity_volume_force_y" : 0, "elasticity_alpha" : 1e-6, "elasticity_temperature_difference" : 10})
        self.elasticity.add_material("Material 2", {"elasticity_young_modulus" : 1e11, "elasticity_poisson_ratio" : 0.33, "elasticity_volume_force_x" : 0, "elasticity_volume_force_y" : 3e4, "elasticity_alpha" : 1e-6, "elasticity_temperature_difference" : 10})
        self.elasticity.add_material("Material 3", {"elasticity_young_modulus" : 1e11, "elasticity_poisson_ratio" : 0.33, "elasticity_volume_force_x" : 0, "elasticity_volume_force_y" : 0, "elasticity_alpha" : 1e-6, "elasticity_temperature_difference" : 10})
        
        # geometry
        geometry = problem.geometry()
        
        # edges
        geometry.add_edge(1.4, 0.2, 1.6, 0.2, boundaries = {"elasticity" : "Load"})
        geometry.add_edge(1.6, 0.2, 1.6, 0, boundaries = {"elasticity" : "Free"})
        geometry.add_edge(1.6, 0, 1.4, 0, boundaries = {"elasticity" : "Free"})
        geometry.add_edge(0, 0.2, 0, 0, boundaries = {"elasticity" : "Fixed"})
        geometry.add_edge(1.4, 0.2, 1.4, 0)
        geometry.add_edge(0, 0.2, 0.6, 0.2, boundaries = {"elasticity" : "Free"})
        geometry.add_edge(0.6, 0.2, 0.6, 0)
        geometry.add_edge(0, 0, 0.6, 0, boundaries = {"elasticity" : "Free"})
        geometry.add_edge(0.6, 0, 1.4, 0, boundaries = {"elasticity" : "Free"})
        geometry.add_edge(1.4, 0.2, 0.6, 0.2, boundaries = {"elasticity" : "Free"})
        
        # labels
        geometry.add_label(0.0823077, 0.11114, materials = {"elasticity" : "Material 1"})
        geometry.add_label(1.48989, 0.108829, materials = {"elasticity" : "Material 3"})
        geometry.add_label(1.20588, 0.108829, materials = {"elasticity" : "Material 2"})
        
        # solve problem
        self.computation = problem.computation()
        self.computation.solve()
        
    def test_values(self):
        # solution
        solution = self.computation.solution("elasticity")
              
        # point value
        point = solution.local_values(1.327264, 0.041087)
        # testVonMises = agros.test("Von Mises stress", point["mises"], 1.175226e5)
        # testTresca = agros.test("Tresca stress", point["tresca"], 1.344939e5)
        self.value_test("Displacement", point["d"], 1.682194e-5)
        self.value_test("Displacement - x", point["dx"], 1.681777e-5)
        self.value_test("Displacement - y", point["dy"], -3.751169e-7, 0.1)
        # testsxx = agros.test("Stress XX", point["sxx"], 50551.83149)
        # testsyy = agros.test("Stress YY", point["syy"], 613.931457)
        # testszz = agros.test("Stress ZZ", point["szz"], -83115.298227)
        # testsxy = agros.test("Stress XY", point["sxy"], -6478.61142)
        # testexx = agros.test("Strain XX", point["exx"], 1.777773e-6)
        # testeyy = eagros.test("Strain YY", point["eyy"], 1.113599e-6)
        # testexy = agros.test("Strain XY", point["exy"], -8.616553e-8)
        
        # surface integral
        # surface = solution.surface_integrals([0])
        # testI = agros.test("Current", surface["I"], 3629.425713)
        

class TestElasticityAxisymmetric(AgrosTestCase):
    def setUp(self):      
        # model
        problem = agros.problem(clear = True)
        problem.coordinate_type = "axisymmetric"
        problem.mesh_type = "triangle"
        
        # fields
        self.elasticity = problem.field("elasticity")
        self.elasticity.analysis_type = "steadystate"
        self.elasticity.number_of_refinements = 2
        self.elasticity.polynomial_order = 3
        self.elasticity.solver = "linear"
        
        self.elasticity.add_boundary("Fixed", "elasticity_fixed_fixed", {"elasticity_displacement_x" : 0, "elasticity_displacement_y" : 0})
        self.elasticity.add_boundary("Free", "elasticity_free_free", {"elasticity_force_x" : 0, "elasticity_force_y" : 0})
        self.elasticity.add_boundary("Load", "elasticity_free_free", {"elasticity_force_x" : 0, "elasticity_force_y" : -10000})
        
        self.elasticity.add_material("Material 1", {"elasticity_young_modulus" : 2e+11, "elasticity_poisson_ratio" : 0.33, "elasticity_volume_force_x" : 0, "elasticity_volume_force_y" : 0, "elasticity_alpha" : 1e-7, "elasticity_temperature_difference" :  0})
        self.elasticity.add_material("Material 2", {"elasticity_young_modulus" : 1e+11, "elasticity_poisson_ratio" : 0.33, "elasticity_volume_force_x" : 0, "elasticity_volume_force_y" : 30000, "elasticity_alpha" : 1.2e-5, "elasticity_temperature_difference" :  0.5})
        self.elasticity.add_material("Material 3", {"elasticity_young_modulus" : 1e+11, "elasticity_poisson_ratio" : 0.33, "elasticity_volume_force_x" : 0, "elasticity_volume_force_y" : 0, "elasticity_alpha" : 2e-7, "elasticity_temperature_difference" : 0})
        
        # geometry
        geometry = problem.geometry()
        
        # edges
        geometry.add_edge(1.4, 0.2, 1.6, 0.2, boundaries = {"elasticity" : "Load"})
        geometry.add_edge(1.6, 0.2, 1.6, 0, boundaries = {"elasticity" : "Free"})
        geometry.add_edge(1.6, 0, 1.4, 0, boundaries = {"elasticity" : "Free"})
        geometry.add_edge(0, 0.2, 0, 0, boundaries = {"elasticity" : "Fixed"})
        geometry.add_edge(1.4, 0.2, 1.4, 0)
        geometry.add_edge(0, 0.2, 0.6, 0.2, boundaries = {"elasticity" : "Free"})
        geometry.add_edge(0.6, 0.2, 0.6, 0)
        geometry.add_edge(0, 0, 0.6, 0, boundaries = {"elasticity" : "Fixed"})
        geometry.add_edge(0.6, 0, 1.4, 0, boundaries = {"elasticity" : "Free"})
        geometry.add_edge(1.4, 0.2, 0.6, 0.2, boundaries = {"elasticity" : "Free"})
        
        # labels
        geometry.add_label(0.0823077, 0.11114, materials = {"elasticity" : "Material 1"})
        geometry.add_label(1.48989, 0.108829, materials = {"elasticity" : "Material 3"})
        geometry.add_label(1.20588, 0.108829, materials = {"elasticity" : "Material 2"})
        
        # solve problem
        self.computation = problem.computation()
        self.computation.solve()
        
    def test_values(self):
        # solution
        solution = self.computation.solution("elasticity")
                            
        # point value
        point = solution.local_values(1.369034, 0.04259)
        #testVonMises = agros.test("Von Mises stress", point["mises"], 1.69779e5)
        # testTresca = agros.test("Tresca stress", point["tresca"], 1.235475e5)
        self.value_test("Displacement", point["d"], 6.154748e-6)
        self.value_test("Displacement - x", point["dr"], 5.544176e-6)
        self.value_test("Displacement - y", point["dz"], -2.672647e-6)
        #testsrr = agros.test("Stress RR", point["sxx"], -1.132081e5)
        #testszz = agros.test("Stress ZZ", point["syy"], -1.210277e5)
        #testsaa = agros.test("Stress aa", point["szz"], -2.7248e5)
        #testtxy = agros.test("Stress RZ", point["sxy"], 39372.872587)
        #testerr = agros.test("Strain RR", point["exx"], 6.165992e-6)
        #testezz = agros.test("Strain ZZ", point["eyy"], 6.061992e-6)
        #testeaa = agros.test("Strain aa", point["ezz"], 4.049699e-6)
        #testerz = agros.test("Strain RZ", point["exy"], 5.236592e-7)
        
        # surface integral
        # surface = solution.surface_integrals([0])
        # testI = agros.test("Current", surface["I"], 3629.425713)        
