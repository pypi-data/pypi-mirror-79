from agrossuite import agros

from .scenario import AgrosTestCase


class TestMathCoeffPlanar(AgrosTestCase):
    def setUp(self):
        # model
        problem = agros.problem(clear=True)
        problem.coordinate_type = "planar"
        problem.mesh_type = "triangle"

        # fields
        self.math_coeff = problem.field("math_coeff")
        self.math_coeff.analysis_type = "steadystate"
        self.math_coeff.number_of_refinements = 2
        self.math_coeff.polynomial_order = 3
        self.math_coeff.adaptivity_type = "disabled"
        self.math_coeff.solver = "linear"

        # boundaries
        self.math_coeff.add_boundary("Source", "math_coeff_solution", {"math_coeff_solution": 1})
        self.math_coeff.add_boundary("Neumann", "math_coeff_flux", {"math_coeff_flux": 10})

        # materials
        self.math_coeff.add_material("Material", {"math_coeff_c": 2, "math_coeff_a": 3, "math_coeff_beta_x": 1, "math_coeff_beta_y": 2, "math_coeff_f": 5})

        # geometry
        geometry = problem.geometry()

        # edges
        geometry.add_edge(-0.95, 0.6, 0.45, 0.8, boundaries={"math_coeff": "Neumann"})
        geometry.add_edge(0.45, 0.8, 0.95, 0.05, boundaries={"math_coeff": "Neumann"})
        geometry.add_edge(0.95, 0.05, 0.5, -0.95, boundaries={"math_coeff": "Neumann"})
        geometry.add_edge(0.5, -0.95, -1.05, -0.3, boundaries={"math_coeff": "Neumann"})
        geometry.add_edge(-0.95, 0.6, -1.05, -0.3, boundaries={"math_coeff": "Neumann"})
        geometry.add_edge(0.1, 0.2, 0.15, -0.3, boundaries={"math_coeff": "Source"})
        geometry.add_edge(0.4, 0.15, 0.6, -0.2, boundaries={"math_coeff": "Source"})
        geometry.add_edge(0.6, -0.2, 0.15, -0.3, boundaries={"math_coeff": "Source"})
        geometry.add_edge(0.1, 0.2, 0.4, 0.15, boundaries={"math_coeff": "Source"})
        geometry.add_edge(-0.55, 0.3, -0.7, 0.1, boundaries={"math_coeff": "Source"})
        geometry.add_edge(-0.55, 0.3, -0.4, 0.2, boundaries={"math_coeff": "Source"})
        geometry.add_edge(-0.7, 0.1, -0.4, 0.2, boundaries={"math_coeff": "Source"})

        # labels
        geometry.add_label(0.350372, -0.0349351, materials={"math_coeff": "none"})
        geometry.add_label(0.270465, 0.500445, materials={"math_coeff": "Material"})
        geometry.add_label(-0.540581, 0.239645, materials={"math_coeff": "none"})

        # solve problem
        self.computation = problem.computation()
        self.computation.solve()

    def test_values(self):
        # solution
        solution = self.computation.solution("math_coeff")

        # point value
        point = solution.local_values(-6.800e-01, -2.526e-02)
        self.value_test("Solution", point["u"], 3.1225)
        self.value_test("Gradient", point["g"], 10.695858)
        self.value_test("Gradient - x", point["gx"], -4.84176)
        self.value_test("Gradient - y", point["gy"], -9.53723)
        self.value_test("Flux", point["f"], 10.695858 * 2)
        self.value_test("Flux - x", point["fx"], -4.84176 * 2)
        self.value_test("Flux - y", point["fy"], -9.53723 * 2)

        # volume integral
        volume = solution.volume_integrals([1])
        self.value_test("Solution", volume["u"], 7.07878)

        # surface integral
        surface = solution.surface_integrals([0, 1, 2, 3, 4])
        self.value_test("Gradient", surface["g"], 59.98499 / 2)
        self.value_test("Flux", surface["f"], 59.98499)


class TestMathCoeffAxisymmetric(AgrosTestCase):
    def setUp(self):
        # model
        problem = agros.problem(clear=True)
        problem.coordinate_type = "axisymmetric"
        problem.mesh_type = "triangle"

        # fields
        self.math_coeff = problem.field("math_coeff")
        self.math_coeff.analysis_type = "steadystate"
        self.math_coeff.number_of_refinements = 0
        self.math_coeff.polynomial_order = 2
        self.math_coeff.solver = "linear"

        self.math_coeff.add_boundary("Dirichlet 1", "math_coeff_solution", {"math_coeff_solution": 10})
        self.math_coeff.add_boundary("Dirichlet 2", "math_coeff_solution", {"math_coeff_solution": -5})
        self.math_coeff.add_boundary("Flux", "math_coeff_flux", {"math_coeff_flux": -30})
        self.math_coeff.add_boundary("Zero flux", "math_coeff_flux", {"math_coeff_flux": 0})

        self.math_coeff.add_material("Material 1", {"math_coeff_c": 5, "math_coeff_a": 0, "math_coeff_beta_x": 5, "math_coeff_beta_y": 8, "math_coeff_f": -50})
        self.math_coeff.add_material("Material 2", {"math_coeff_c": 3, "math_coeff_a": 0, "math_coeff_beta_x": -3, "math_coeff_beta_y": 4, "math_coeff_f": 0})

        # geometry
        geometry = problem.geometry()

        # edges
        geometry.add_edge(0, 1.6, 0, 0.95, boundaries={"math_coeff": "Zero flux"})
        geometry.add_edge(0, 0.95, 0.35, 0.45, boundaries={"math_coeff": "Zero flux"})
        geometry.add_edge(0.35, 0.45, 0.25, 0, boundaries={"math_coeff": "Zero flux"})
        geometry.add_edge(0.25, 0, 0, -0.25, boundaries={"math_coeff": "Zero flux"})
        geometry.add_edge(0, -0.25, 0.9, -0.75, boundaries={"math_coeff": "Dirichlet 1"})
        geometry.add_edge(0.9, -0.75, 1.65, 0.15, boundaries={"math_coeff": "Flux"})
        geometry.add_edge(1.65, 0.15, 1.25, 1.7, boundaries={"math_coeff": "Flux"})
        geometry.add_edge(1.25, 1.7, 0, 1.6, boundaries={"math_coeff": "Dirichlet 2"})
        geometry.add_edge(0.6, 1.1, 1.15, 0.95, boundaries={"math_coeff": "Zero flux"})
        geometry.add_edge(0.95, 0.6, 0.6, 1.1, boundaries={"math_coeff": "Zero flux"})
        geometry.add_edge(1.15, 0.95, 0.95, 0.6, boundaries={"math_coeff": "Zero flux"})
        geometry.add_edge(0.35, 0.45, 1.65, 0.15)

        # labels
        geometry.add_label(0.888828, 0.877296, materials={"math_coeff": "none"})
        geometry.add_label(0.301166, 0.88379, materials={"math_coeff": "Material 1"})
        geometry.add_label(0.755711, -0.216858, materials={"math_coeff": "Material 2"})

        # solve problem
        self.computation = problem.computation()
        self.computation.solve()

    def test_values(self):
        # solution
        solution = self.computation.solution("math_coeff")

        # point value
        point = solution.local_values(1.220, 8.820e-02)
        self.value_test("Solution", point["u"], -16.28353)
        self.value_test("Gradient", point["g"], 15.85405)
        self.value_test("Gradient - r", point["gr"], -14.25501)
        self.value_test("Gradient - z", point["gz"], -6.93706)
        self.value_test("Flux", point["f"], 15.85405 * 3)
        self.value_test("Flux - r", point["fr"], -14.25501 * 3)
        self.value_test("Flux - z", point["fz"], -6.93706 * 3)

        # volume integral
        volume = solution.volume_integrals([2])
        self.value_test("Solution", volume["u"], -45.8945)

        # surface integral
        surface = solution.surface_integrals([5, 6])
        self.value_test("Gradient", surface["g"], -281.55775 / 3 - 437.52318 / 5)
        self.value_test("Flux", surface["f"], -719.08092)


class TestMathCoeffTransientPlanar(AgrosTestCase):
    def setUp(self):
        # problem
        problem = agros.problem(clear=True)
        problem.coordinate_type = "planar"
        problem.mesh_type = "triangle"
        problem.time_step_method = "fixed"
        problem.time_method_order = 2
        problem.time_total = 1.1
        problem.time_steps = 20

        # math_coeff
        self.math_coeff = problem.field("math_coeff")
        self.math_coeff.analysis_type = "transient"
        self.math_coeff.transient_initial_condition = 0
        self.math_coeff.number_of_refinements = 2
        self.math_coeff.polynomial_order = 3
        self.math_coeff.adaptivity_type = "disabled"
        self.math_coeff.solver = "linear"

        # boundaries
        self.math_coeff.add_boundary("Source 1", "math_coeff_solution", {"math_coeff_solution": {"expression": "exp(-10/5*time) - exp(-20/5*time)"}, "math_coeff_solution_time_derivative": {"expression": "-10/5*exp(-10/5*time) + 20/5*exp(-20/5*time)"}})
        self.math_coeff.add_boundary("Neumann", "math_coeff_flux", {"math_coeff_flux": 10})
        self.math_coeff.add_boundary("Source 2", "math_coeff_solution", {"math_coeff_solution": {"expression": "sin(2*pi*0.5/0.75*time)"}, "math_coeff_solution_time_derivative": {"expression": "2*pi*0.5/0.75*cos(2*pi*0.5/0.75*time)"}})

        # materials
        self.math_coeff.add_material("Material", {"math_coeff_ea": 300, "math_coeff_da": 280, "math_coeff_c": 3, "math_coeff_a": 4, "math_coeff_beta_x": 2, "math_coeff_beta_y": -2, "math_coeff_f": 5})

        # geometry
        geometry = problem.geometry()
        geometry.add_edge(-0.22, 0.055, 0.045, 0.08, boundaries={"math_coeff": "Neumann"})
        geometry.add_edge(0.045, 0.08, 0.095, 0.005, boundaries={"math_coeff": "Neumann"})
        geometry.add_edge(0.095, 0.005, 0.05, -0.095, boundaries={"math_coeff": "Neumann"})
        geometry.add_edge(0.05, -0.095, -0.215, -0.045, boundaries={"math_coeff": "Neumann"})
        geometry.add_edge(-0.22, 0.055, -0.215, -0.045, boundaries={"math_coeff": "Neumann"})
        geometry.add_edge(-0.025, 0.04, 0.015, -0.03, boundaries={"math_coeff": "Source 1"})
        geometry.add_edge(0.04, 0.015, 0.06, -0.02, boundaries={"math_coeff": "Source 1"})
        geometry.add_edge(0.06, -0.02, 0.015, -0.03, boundaries={"math_coeff": "Source 1"})
        geometry.add_edge(-0.025, 0.04, 0.04, 0.015, boundaries={"math_coeff": "Source 1"})
        geometry.add_edge(-0.16, 0.025, -0.16, -0.02, boundaries={"math_coeff": "Source 2"})
        geometry.add_edge(-0.16, 0.025, -0.09, 0.03, boundaries={"math_coeff": "Source 2"})
        geometry.add_edge(-0.09, 0.03, -0.115, -0.005, boundaries={"math_coeff": "Source 2"})
        geometry.add_edge(-0.095, -0.03, -0.115, -0.005, boundaries={"math_coeff": "Source 2"})
        geometry.add_edge(-0.16, -0.02, -0.095, -0.03, boundaries={"math_coeff": "Source 2"})

        geometry.add_label(0.0350372, -0.00349351, materials={"math_coeff": "none"})
        geometry.add_label(0.0270465, 0.0500445, materials={"math_coeff": "Material"})
        geometry.add_label(-0.150064, 0.00228808, materials={"math_coeff": "none"})

        # solve problem
        self.computation = problem.computation()
        self.computation.solve()

    def disabled_test_values(self):
        # solution
        solution = self.computation.solution("math_coeff")

        # point value
        point = solution.local_values(9.386e-01, 1.147e-01)
        self.value_test("Solution", point["u"], -0.91572, 5)
        self.value_test("Gradient", point["g"], 0.176053, 10)
        self.value_test("Gradient - r", point["gr"], 0.04536, 10)
        self.value_test("Gradient - z", point["gz"], 0.17011, 10)
        self.value_test("Flux", point["f"], 0.176053 * 3, 10)
        self.value_test("Flux - r", point["fr"], 0.04536 * 3, 10)
        self.value_test("Flux - z", point["fz"], 0.17011 * 3, 10)

        # volume integral
        volume = solution.volume_integrals([1])
        self.value_test("Solution", volume["u"], -4.29455, 10)

        # surface integral
        surface = solution.surface_integrals([4])
        self.value_test("Gradient", surface["g"], 1.33109 / 3, 10)
        self.value_test("Flux", surface["f"], 1.33109, 10)


class TestMathCoeffTransientAxisymmetric(AgrosTestCase):
    def setUp(self):
        # model
        problem = agros.problem(clear=True)
        problem.coordinate_type = "axisymmetric"
        problem.mesh_type = "triangle"
        problem.time_step_method = "adaptive"
        problem.time_method_order = 2
        problem.time_total = 4
        problem.time_method_tolerance = 0.05

        # fields
        self.math_coeff = problem.field("math_coeff")
        self.math_coeff.analysis_type = "transient"
        self.math_coeff.number_of_refinements = 3
        self.math_coeff.polynomial_order = 3
        self.math_coeff.solver = "linear"

        self.math_coeff.add_boundary("Dirichlet 1", "math_coeff_solution", {"math_coeff_solution": {"expression": "1.0*sin(2*pi*1.0/5*time)"}, "math_coeff_solution_time_derivative": {"expression": "2*pi*1.0/5*cos(2*pi*1.0/5*time)"}})
        self.math_coeff.add_boundary("Dirichlet 2", "math_coeff_solution", {"math_coeff_solution": 0, "math_coeff_solution_time_derivative": 0})
        self.math_coeff.add_boundary("Zero flux", "math_coeff_flux", {"math_coeff_flux": 0})

        # materials
        self.math_coeff.add_material("Material 1", {"math_coeff_ea": 1, "math_coeff_da": 2, "math_coeff_c": 5, "math_coeff_a": 2, "math_coeff_beta_x": 5, "math_coeff_beta_y": 8, "math_coeff_f": -5})
        self.math_coeff.add_material("Material 2", {"math_coeff_ea": 1, "math_coeff_da": 4, "math_coeff_c": 3, "math_coeff_a": 0, "math_coeff_beta_x": -3, "math_coeff_beta_y": 4, "math_coeff_f": 0})

        # geometry
        geometry = problem.geometry()
        geometry.add_edge(0, 1.6, 0, 0.95, boundaries={"math_coeff": "Zero flux"})
        geometry.add_edge(0, 0.95, 0.35, 0.45, boundaries={"math_coeff": "Zero flux"})
        geometry.add_edge(0.35, 0.45, 0.25, 0, boundaries={"math_coeff": "Zero flux"})
        geometry.add_edge(0.25, 0, 0.45, -0.35, boundaries={"math_coeff": "Zero flux"})
        geometry.add_edge(0.45, -0.35, 0.9, -0.75, boundaries={"math_coeff": "Dirichlet 1"})
        geometry.add_edge(0.9, -0.75, 1.4, 0.8, boundaries={"math_coeff": "Zero flux"})
        geometry.add_edge(1.4, 0.8, 1.25, 1.7, boundaries={"math_coeff": "Zero flux"})
        geometry.add_edge(1.25, 1.7, 0, 1.6, boundaries={"math_coeff": "Dirichlet 2"})
        geometry.add_edge(0.35, 0.45, 1.4, 0.8)

        geometry.add_label(0.301166, 0.88379, materials={"math_coeff": "Material 1"})
        geometry.add_label(0.755711, -0.216858, materials={"math_coeff": "Material 2"})

        # solve problem
        self.computation = problem.computation()
        self.computation.solve()

    def disabled_test_values(self):
        # solution
        solution = self.computation.solution("math_coeff")

        # point value
        point = solution.local_values(9.386e-01, 1.147e-01)
        self.value_test("Solution", point["u"], -0.91572, 5)
        self.value_test("Gradient", point["g"], 0.176053, 10)
        self.value_test("Gradient - r", point["gr"], 0.04536, 10)
        self.value_test("Gradient - z", point["gz"], 0.17011, 10)
        self.value_test("Flux", point["f"], 0.176053 * 3, 10)
        self.value_test("Flux - r", point["fr"], 0.04536 * 3, 10)
        self.value_test("Flux - z", point["fz"], 0.17011 * 3, 10)

        # volume integral
        volume = solution.volume_integrals([1])
        self.value_test("Solution", volume["u"], -4.29455, 10)

        # surface integral
        surface = solution.surface_integrals([4])
        self.value_test("Gradient", surface["g"], 1.33109 / 3, 10)
        self.value_test("Flux", surface["f"], 1.33109, 10)
