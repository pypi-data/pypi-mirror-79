import unittest
import numpy as np

from modelbase.ode import Model


class ModelErrorTests(unittest.TestCase):
    def test_add_compound_error_non_string(self):
        m = Model()
        with self.assertRaises(TypeError):
            m._add_derived_compound(compound=tuple())
        with self.assertRaises(TypeError):
            m._add_derived_compound(compound=list())
        with self.assertRaises(TypeError):
            m._add_derived_compound(compound=dict())
        with self.assertRaises(TypeError):
            m._add_derived_compound(compound=set())
        with self.assertRaises(TypeError):
            m._add_derived_compound(compound=int())
        with self.assertRaises(TypeError):
            m._add_derived_compound(compound=float())
        with self.assertRaises(TypeError):
            m._add_derived_compound(compound=None)

    def test_add_compound_error_time(self):
        m = Model()
        with self.assertRaises(KeyError):
            m._add_derived_compound(compound="time")

    def test_add_compound_error_duplicate(self):
        m = Model()
        m._add_derived_compound(compound="x")
        with self.assertWarns(UserWarning):
            m._add_derived_compound(compound="x")


class ModelWarningsTests(unittest.TestCase):
    def test_warn_on_algebraic_module_replacement(self):
        m = Model()
        m.add_algebraic_module(
            module_name="mod1",
            function=lambda: None,
            compounds=[],
            derived_compounds=[],
            modifiers=None,
            parameters=None,
        )
        with self.assertWarns(UserWarning):
            m.add_algebraic_module(
                module_name="mod1",
                function=lambda: None,
                compounds=[],
                derived_compounds=[],
                modifiers=None,
                parameters=None,
            )


class ModelDerivedCompoundTests(unittest.TestCase):
    def test_add_derived_compound(self):
        m = Model()
        m._add_derived_compound("x")
        self.assertEqual(m.compounds, [])
        self.assertEqual(m.derived_compounds, ["x"])

    def test_add_derived_compounds(self):
        m = Model()
        m._add_derived_compounds(("x", "y"))
        self.assertEqual(m.compounds, [])
        self.assertEqual(m.derived_compounds, ["x", "y"])

    def test_remove_derived_compound(self):
        m = Model()
        m._add_derived_compounds(("x", "y"))
        m._remove_derived_compound("x")
        self.assertEqual(m.compounds, [])
        self.assertEqual(m.derived_compounds, ["y"])

    def test_remove_derived_compounds(self):
        m = Model()
        m._add_derived_compounds(("x", "y"))
        m._remove_derived_compounds(("x", "y"))
        self.assertEqual(m.compounds, [])
        self.assertEqual(m.derived_compounds, [])

    def test_get_derived_compounds(self):
        m = Model()
        m._add_derived_compounds(("x", "y"))
        self.assertEqual(m.get_derived_compounds(), ["x", "y"])

    def test_get_all_compounds(self):
        m = Model()
        m.add_compound("A")
        m._add_derived_compounds(("x", "y"))
        self.assertEqual(m.get_all_compounds(), ["A", "x", "y"])

    ############################################################################
    # Updating meta info
    ############################################################################

    def test_update_module_meta_info(self):
        m = Model()
        m.add_algebraic_module(module_name="x", function=lambda *args: args)
        m.update_module_meta_info(module="x", meta_info={"common_name": "X"})
        self.assertEqual(m.meta_info["modules"]["x"].common_name, "X")

    def test_update_module_meta_info_replacing(self):
        m = Model()
        m.add_algebraic_module(
            module_name="x", function=lambda *args: args, **{"common_name": "X1"}
        )
        m.update_module_meta_info(module="x", meta_info={"common_name": "X2"})
        self.assertEqual(m.meta_info["modules"]["x"].common_name, "X2")


class ModelAlgebraicModuleTests(unittest.TestCase):
    def create_minimal_model(self):
        parameters = {"keq": 1}
        m = Model(parameters=parameters)
        m.add_compound("A")
        m.add_algebraic_module(
            module_name="mod1",
            function=lambda s, keq: (s / (1 + keq), (s * keq / (1 + keq))),
            compounds=["A"],
            derived_compounds=["x", "y"],
            parameters=["keq"],
        )
        return m

    def test_initialise(self):
        modules = {
            "mod1": {
                "function": lambda s, keq: (s / (1 + keq), (s * keq / (1 + keq))),
                "compounds": ["A"],
                "derived_compounds": ["X1", "Y1"],
                "modifiers": [],
                "parameters": ["keq"],
            },
            "mod2": {
                "function": lambda s, keq: (s / (1 + keq), (s * keq / (1 + keq))),
                "compounds": ["B"],
                "derived_compounds": ["X2", "Y2"],
                "modifiers": ["time"],
                "parameters": ["keq"],
            },
        }

        m = Model(compounds=("A", "B"), algebraic_modules=modules)
        self.assertEqual(m.compounds, ["A", "B"])
        self.assertEqual(m.derived_compounds, ["X1", "Y1", "X2", "Y2"])
        self.assertEqual(m.algebraic_modules["mod1"]["function"].__name__, "mod1")
        self.assertEqual(m.algebraic_modules["mod1"]["compounds"], ["A"])
        self.assertEqual(m.algebraic_modules["mod1"]["derived_compounds"], ["X1", "Y1"])
        self.assertEqual(m.algebraic_modules["mod1"]["modifiers"], [])
        self.assertEqual(m.algebraic_modules["mod1"]["parameters"], ["keq"])

        self.assertEqual(m.algebraic_modules["mod2"]["function"].__name__, "mod2")
        self.assertEqual(m.algebraic_modules["mod2"]["compounds"], ["B"])
        self.assertEqual(m.algebraic_modules["mod2"]["derived_compounds"], ["X2", "Y2"])
        self.assertEqual(m.algebraic_modules["mod2"]["modifiers"], ["time"])
        self.assertEqual(m.algebraic_modules["mod2"]["parameters"], ["keq"])

    def test_add_algebraic_module_no_derived_compounds(self):
        parameters = {"keq": 1}
        m = Model(parameters=parameters)
        m.add_compound("A")
        m.add_algebraic_module(
            module_name="mod1",
            function=lambda s, keq: (s / (1 + keq), (s * keq / (1 + keq))),
            compounds=["A"],
            derived_compounds=None,
            parameters=["keq"],
        )
        self.assertEqual(m.compounds, ["A"])
        self.assertEqual(m.derived_compounds, [])
        self.assertEqual(m.algebraic_modules["mod1"]["compounds"], ["A"])
        self.assertEqual(m.algebraic_modules["mod1"]["derived_compounds"], [])
        self.assertEqual(m.algebraic_modules["mod1"]["parameters"], ["keq"])

    def test_add_algebraic_module(self):
        parameters = {"keq": 1}
        m = Model(parameters=parameters)
        m.add_compound("A")
        m.add_algebraic_module(
            module_name="mod1",
            function=lambda s, keq: (s / (1 + keq), (s * keq / (1 + keq))),
            compounds=["A"],
            derived_compounds=["x", "y"],
            parameters=["keq"],
        )
        self.assertEqual(m.compounds, ["A"])
        self.assertEqual(m.derived_compounds, ["x", "y"])
        self.assertEqual(m.algebraic_modules["mod1"]["function"].__name__, "mod1")
        self.assertEqual(m.algebraic_modules["mod1"]["compounds"], ["A"])
        self.assertEqual(m.algebraic_modules["mod1"]["derived_compounds"], ["x", "y"])
        self.assertEqual(m.algebraic_modules["mod1"]["parameters"], ["keq"])

    def test_update_algebraic_module(self):
        parameters = {"keq1": 1, "keq2": 2}
        m = Model(parameters=parameters)
        m.add_compounds(["A1", "A2"])
        m.add_algebraic_module(
            module_name="mod1",
            function=lambda s, keq: (s / (1 + keq), (s * keq / (1 + keq))),
            compounds=["A1"],
            derived_compounds=["x1", "y1"],
            parameters=["keq1"],
        )
        m.update_algebraic_module(
            module_name="mod1",
            function=lambda s, keq: (s / (1 + keq), (s * keq / (1 + keq))),
            compounds=["A2"],
            derived_compounds=["x2", "y2"],
            parameters=["keq2"],
        )
        self.assertEqual(m.compounds, ["A1", "A2"])
        self.assertEqual(m.derived_compounds, ["x2", "y2"])
        self.assertEqual(m.algebraic_modules["mod1"]["function"].__name__, "mod1")
        self.assertEqual(m.algebraic_modules["mod1"]["compounds"], ["A2"])
        self.assertEqual(m.algebraic_modules["mod1"]["derived_compounds"], ["x2", "y2"])
        self.assertEqual(m.algebraic_modules["mod1"]["parameters"], ["keq2"])

    def test_update_algebraic_module_nothing(self):
        parameters = {"keq": 1}
        m = Model(parameters=parameters)
        m.add_compound("A")
        m.add_algebraic_module(
            module_name="mod1",
            function=lambda s, keq: (s / (1 + keq), (s * keq / (1 + keq))),
            compounds=["A"],
            derived_compounds=["x", "y"],
            parameters=["keq"],
        )
        m.update_algebraic_module(module_name="mod1")
        self.assertEqual(m.compounds, ["A"])
        self.assertEqual(m.derived_compounds, ["x", "y"])
        self.assertEqual(m.algebraic_modules["mod1"]["function"].__name__, "mod1")
        self.assertEqual(m.algebraic_modules["mod1"]["compounds"], ["A"])
        self.assertEqual(m.algebraic_modules["mod1"]["derived_compounds"], ["x", "y"])
        self.assertEqual(m.algebraic_modules["mod1"]["parameters"], ["keq"])

    def test_add_algebraic_modules(self):
        modules = {
            "mod1": {
                "function": lambda s, keq: (s / (1 + keq), (s * keq / (1 + keq))),
                "compounds": ["A"],
                "derived_compounds": ["X1", "Y1"],
                "modifiers": [],
                "parameters": ["keq"],
            },
            "mod2": {
                "function": lambda s, keq: (s / (1 + keq), (s * keq / (1 + keq))),
                "compounds": ["B"],
                "derived_compounds": ["X2", "Y2"],
                "modifiers": ["time"],
                "parameters": ["keq"],
            },
        }

        m = Model()
        m.add_compounds(("A", "B"))
        m.add_algebraic_modules(modules)
        self.assertEqual(m.compounds, ["A", "B"])
        self.assertEqual(m.derived_compounds, ["X1", "Y1", "X2", "Y2"])
        self.assertEqual(m.algebraic_modules["mod1"]["function"].__name__, "mod1")
        self.assertEqual(m.algebraic_modules["mod1"]["compounds"], ["A"])
        self.assertEqual(m.algebraic_modules["mod1"]["derived_compounds"], ["X1", "Y1"])
        self.assertEqual(m.algebraic_modules["mod1"]["modifiers"], [])
        self.assertEqual(m.algebraic_modules["mod1"]["parameters"], ["keq"])

        self.assertEqual(m.algebraic_modules["mod2"]["function"].__name__, "mod2")
        self.assertEqual(m.algebraic_modules["mod2"]["compounds"], ["B"])
        self.assertEqual(m.algebraic_modules["mod2"]["derived_compounds"], ["X2", "Y2"])
        self.assertEqual(m.algebraic_modules["mod2"]["modifiers"], ["time"])
        self.assertEqual(m.algebraic_modules["mod2"]["parameters"], ["keq"])

    def test_remove_algebraic_module(self):
        parameters = {"keq": 1}
        m = Model(parameters=parameters)
        m.add_compound("A")
        m.add_algebraic_module(
            module_name="mod1",
            function=lambda s, keq: (s / (1 + keq), (s * keq / (1 + keq))),
            compounds=["A"],
            derived_compounds=["x", "y"],
            parameters=["keq"],
        )
        m.remove_algebraic_module(module_name="mod1")
        self.assertEqual(m.compounds, ["A"])
        self.assertEqual(m.derived_compounds, [])
        with self.assertRaises(KeyError):
            m.algebraic_modules["mod1"]

    def test_remove_algebraic_modules(self):
        parameters = {"keq": 1}
        m = Model(parameters=parameters)
        m.add_compound("A")
        m.add_algebraic_module(
            module_name="mod1",
            function=lambda s, keq: (s / (1 + keq), (s * keq / (1 + keq))),
            compounds=["A"],
            derived_compounds=["x1", "y1"],
            parameters=["keq"],
        )
        m.add_algebraic_module(
            module_name="mod2",
            function=lambda s, keq: (s / (1 + keq), (s * keq / (1 + keq))),
            compounds=["A"],
            derived_compounds=["x2", "y2"],
            parameters=["keq"],
        )
        m.remove_algebraic_modules(module_names=("mod1", "mod2"))
        self.assertEqual(m.compounds, ["A"])
        self.assertEqual(m.derived_compounds, [])
        with self.assertRaises(KeyError):
            m.algebraic_modules["mod1"]
        with self.assertRaises(KeyError):
            m.algebraic_modules["mod2"]

    def test_get_algebraic_module_compounds(self):
        m = self.create_minimal_model()
        self.assertEqual(m.get_algebraic_module_compounds(module_name="mod1"), ["A"])

    def test_get_algebraic_module_derived_compounds(self):
        m = self.create_minimal_model()
        self.assertEqual(
            m.get_algebraic_module_derived_compounds(module_name="mod1"), ["x", "y"]
        )

    def test_get_algebraic_module_parameters(self):
        m = self.create_minimal_model()
        self.assertEqual(m.get_algebraic_module_parameters(module_name="mod1"), ["keq"])

    def test_get_algebraic_module_modifiers(self):
        parameters = {"keq": 1}
        m = Model(parameters=parameters)
        m.add_compound("A")
        m.add_algebraic_module(
            module_name="mod1",
            function=lambda A, time, keq: (A / keq * time, (keq * time / A)),
            compounds=["A"],
            derived_compounds=["x", "y"],
            modifiers=["time"],
            parameters=["keq"],
        )
        self.assertEqual(m.get_algebraic_module_modifiers(module_name="mod1"), ["time"])


def mod_one_one(x, keq):
    return (keq * x,)


def mod_one_two(x, keq):
    return keq * x, keq * x


def mod_two_one(x, y, keq):
    return (keq * (x + y),)


def mod_two_two(x, y, keq):
    return keq * (x + y), keq * (x + y)


class FullConcentrationDictTests(unittest.TestCase):
    def test_one_one(self):
        parameters = {"keq": 1}
        m = Model(parameters=parameters)
        m.add_compound("A")
        m.add_algebraic_module(
            module_name="mod",
            function=mod_one_one,
            compounds=["A"],
            derived_compounds=["x"],
            parameters=["keq"],
        )
        self.assertEqual(m._get_fcd(y={"A": 1}, t=0), {"A": 1, "time": 0, "x": 1})

    def test_one_one_array(self):
        parameters = {"keq": 1}
        m = Model(parameters=parameters)
        m.add_compound("A")
        m.add_algebraic_module(
            module_name="mod",
            function=mod_one_one,
            compounds=["A"],
            derived_compounds=["x"],
            parameters=["keq"],
        )
        fcd = m._get_fcd(y={"A": np.array([1, 2])}, t=np.array([0, 1]))
        np.testing.assert_array_equal(fcd["A"], [1, 2])
        np.testing.assert_array_equal(fcd["time"], [0, 1])
        np.testing.assert_array_equal(fcd["x"], [1, 2])

    def test_one_two(self):
        parameters = {"keq": 1}
        m = Model(parameters=parameters)
        m.add_compound("A")
        m.add_algebraic_module(
            module_name="mod",
            function=mod_one_two,
            compounds=["A"],
            derived_compounds=["x1", "x2"],
            parameters=["keq"],
        )
        self.assertEqual(
            m._get_fcd(y={"A": 1}, t=0), {"A": 1, "time": 0, "x1": 1, "x2": 1}
        )

    def test_one_two_array(self):
        parameters = {"keq": 1}
        m = Model(parameters=parameters)
        m.add_compound("A")
        m.add_algebraic_module(
            module_name="mod",
            function=mod_one_two,
            compounds=["A"],
            derived_compounds=["x1", "x2"],
            parameters=["keq"],
        )
        fcd = m._get_fcd(y={"A": np.array([1, 2])}, t=np.array([0, 1]))
        np.testing.assert_array_equal(fcd["A"], [1, 2])
        np.testing.assert_array_equal(fcd["time"], [0, 1])
        np.testing.assert_array_equal(fcd["x1"], [1, 2])
        np.testing.assert_array_equal(fcd["x2"], [1, 2])

    def test_two_one(self):
        parameters = {"keq": 1}
        m = Model(parameters=parameters)
        m.add_compounds(("A", "B"))
        m.add_algebraic_module(
            module_name="mod",
            function=mod_two_one,
            compounds=["A", "B"],
            derived_compounds=["x1"],
            parameters=["keq"],
        )
        self.assertEqual(
            m._get_fcd(y={"A": 1, "B": 1}, t=0), {"A": 1, "B": 1, "time": 0, "x1": 2}
        )

    def test_two_one_array(self):
        parameters = {"keq": 1}
        m = Model(parameters=parameters)
        m.add_compounds(("A", "B"))
        m.add_algebraic_module(
            module_name="mod",
            function=mod_two_one,
            compounds=["A", "B"],
            derived_compounds=["x1"],
            parameters=["keq"],
        )
        fcd = m._get_fcd(
            y={"A": np.array([1, 2]), "B": np.array([1, 2])}, t=np.array([0, 1])
        )
        np.testing.assert_array_equal(fcd["A"], [1, 2])
        np.testing.assert_array_equal(fcd["B"], [1, 2])
        np.testing.assert_array_equal(fcd["time"], [0, 1])
        np.testing.assert_array_equal(fcd["x1"], [2, 4])

    def test_two_two(self):
        parameters = {"keq": 1}
        m = Model(parameters=parameters)
        m.add_compounds(("A", "B"))
        m.add_algebraic_module(
            module_name="mod",
            function=mod_two_two,
            compounds=["A", "B"],
            derived_compounds=["x1", "x2"],
            parameters=["keq"],
        )
        self.assertEqual(
            m._get_fcd(y={"A": 1, "B": 1}, t=0),
            {"A": 1, "B": 1, "time": 0, "x1": 2, "x2": 2},
        )

    def test_two_two_array(self):
        parameters = {"keq": 1}
        m = Model(parameters=parameters)
        m.add_compounds(("A", "B"))
        m.add_algebraic_module(
            module_name="mod",
            function=mod_two_two,
            compounds=["A", "B"],
            derived_compounds=["x1", "x2"],
            parameters=["keq"],
        )
        fcd = m._get_fcd(
            y={"A": np.array([1, 2]), "B": np.array([1, 2])}, t=np.array([0, 1])
        )
        np.testing.assert_array_equal(fcd["A"], [1, 2])
        np.testing.assert_array_equal(fcd["B"], [1, 2])
        np.testing.assert_array_equal(fcd["time"], [0, 1])
        np.testing.assert_array_equal(fcd["x1"], [2, 4])
        np.testing.assert_array_equal(fcd["x2"], [2, 4])

    def test_one_modifier_time(self):
        parameters = {"keq": 1}
        m = Model(parameters=parameters)
        m.add_compound("A")
        m.add_algebraic_module(
            module_name="mod",
            function=mod_two_two,
            compounds=["A"],
            derived_compounds=["x1", "x2"],
            modifiers=["time"],
            parameters=["keq"],
        )
        self.assertEqual(
            m._get_fcd(y={"A": 1}, t=1), {"A": 1, "time": 1, "x1": 2, "x2": 2},
        )

    def test_one_modifier_time_array(self):
        parameters = {"keq": 1}
        m = Model(parameters=parameters)
        m.add_compounds(("A", "B"))
        m.add_algebraic_module(
            module_name="mod",
            function=mod_two_two,
            compounds=["A"],
            derived_compounds=["x1", "x2"],
            modifiers=["time"],
            parameters=["keq"],
        )
        fcd = m._get_fcd(
            y={"A": np.array([1, 2]), "B": np.array([1, 2])}, t=np.array([1, 2])
        )
        np.testing.assert_array_equal(fcd["A"], [1, 2])
        np.testing.assert_array_equal(fcd["B"], [1, 2])
        np.testing.assert_array_equal(fcd["time"], [1, 2])
        np.testing.assert_array_equal(fcd["x1"], [2, 4])
        np.testing.assert_array_equal(fcd["x2"], [2, 4])

    def test_one_non_time_modifier(self):
        parameters = {"keq": 1}
        m = Model(parameters=parameters)
        m.add_compounds(("A", "B"))
        m.add_algebraic_module(
            module_name="mod",
            function=mod_two_two,
            compounds=["A"],
            derived_compounds=["x1", "x2"],
            modifiers=["B"],
            parameters=["keq"],
        )
        self.assertEqual(
            m._get_fcd(y={"A": 1, "B": 1}, t=0),
            {"A": 1, "B": 1, "time": 0, "x1": 2, "x2": 2},
        )

    def test_one_non_time_modifier_array(self):
        parameters = {"keq": 1}
        m = Model(parameters=parameters)
        m.add_compounds(("A", "B"))
        m.add_algebraic_module(
            module_name="mod",
            function=mod_two_two,
            compounds=["A"],
            derived_compounds=["x1", "x2"],
            modifiers=["B"],
            parameters=["keq"],
        )
        fcd = m._get_fcd(
            y={"A": np.array([1, 2]), "B": np.array([1, 2])}, t=np.array([0, 1])
        )
        np.testing.assert_array_equal(fcd["A"], [1, 2])
        np.testing.assert_array_equal(fcd["B"], [1, 2])
        np.testing.assert_array_equal(fcd["time"], [0, 1])
        np.testing.assert_array_equal(fcd["x1"], [2, 4])
        np.testing.assert_array_equal(fcd["x2"], [2, 4])


class SourceCodeTests(unittest.TestCase):
    def test_generate_source_code_one_module(self):
        parameters = {"keq": 1}
        m = Model(parameters=parameters)
        m.add_compound("A")
        m.add_algebraic_module(
            module_name="mod1",
            function=lambda s, keq: (s / (1 + keq), (s * keq / (1 + keq))),
            compounds=["A"],
            derived_compounds=["x", "y"],
            parameters=["keq"],
        )

        module_funcs, modules = m._generate_algebraic_modules_source_code()
        self.assertEqual(
            module_funcs.split("\n"),
            ["def mod1(s, keq):", "    return (s / (1 + keq), (s * keq / (1 + keq)))"],
        )

        self.assertEqual(
            modules.split("\n"),
            [
                "m.add_algebraic_module(",
                "    module_name='mod1',",
                "    function=mod1,",
                "    compounds=['A'],",
                "    derived_compounds=['x', 'y'],",
                "    modifiers=[],",
                "    parameters=['keq'],",
                ")",
            ],
        )

    def test_generate_source_code_lambda(self):
        parameters = {"keq": 1}
        m = Model(parameters=parameters)
        m.add_compound("A")
        m.add_algebraic_module(
            module_name="mod1",
            function=lambda s, k_eq: (s / (1 + k_eq), s * k_eq / (1 + k_eq)),
            compounds=["A"],
            derived_compounds=["x", "y"],
            parameters=["keq"],
        )

        module_funcs, modules = m._generate_algebraic_modules_source_code()
        self.assertEqual(
            module_funcs.split("\n"),
            [
                "def mod1(s, k_eq):",
                "    return (s / (1 + k_eq), s * k_eq / (1 + k_eq))",
            ],
        )

        self.assertEqual(
            modules.split("\n"),
            [
                "m.add_algebraic_module(",
                "    module_name='mod1',",
                "    function=mod1,",
                "    compounds=['A'],",
                "    derived_compounds=['x', 'y'],",
                "    modifiers=[],",
                "    parameters=['keq'],",
                ")",
            ],
        )


class SBMLTests(unittest.TestCase):
    def test_raise_user_warning(self):
        m = Model()
        m.add_algebraic_module(
            module_name="mod1",
            function=lambda s, keq: (s / (1 + keq), (s * keq / (1 + keq))),
            compounds=["A"],
            derived_compounds=["x", "y"],
            parameters=["keq"],
        )
        doc = m._create_sbml_document()
        sbml_model = m._create_sbml_model(doc)
        with self.assertWarns(UserWarning):
            m._create_sbml_algebraic_modules(sbml_model)
