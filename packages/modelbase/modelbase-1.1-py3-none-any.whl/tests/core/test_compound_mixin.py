import unittest
from modelbase.ode import Model


class ModelErrorTests(unittest.TestCase):
    def test_add_compound_error_non_string(self):
        m = Model()
        with self.assertRaises(TypeError):
            m.add_compound(compound=tuple())
        with self.assertRaises(TypeError):
            m.add_compound(compound=list())
        with self.assertRaises(TypeError):
            m.add_compound(compound=dict())
        with self.assertRaises(TypeError):
            m.add_compound(compound=set())
        with self.assertRaises(TypeError):
            m.add_compound(compound=int())
        with self.assertRaises(TypeError):
            m.add_compound(compound=float())
        with self.assertRaises(TypeError):
            m.add_compound(compound=None)

    def test_add_compound_error_time(self):
        m = Model()
        with self.assertRaises(KeyError):
            m.add_compound(compound="time")

    def test_add_compound_error_duplicate(self):
        m = Model()
        m.add_compound(compound="x")
        with self.assertWarns(UserWarning):
            m.add_compound(compound="x")
            self.assertEqual(m.compounds, ["x"])

    def test_add_compound_duplicate(self):
        m = Model()
        m.add_compound(compound="x")
        with self.assertWarns(UserWarning):
            m.add_compound(compound="x")
        self.assertEqual(m.compounds, ["x"])

    def test_add_compound_duplicate_update_nometa(self):
        m = Model()
        m.add_compound(compound="x", **{"common_name": "A"})
        with self.assertWarns(UserWarning):
            m.add_compound(compound="x")
            self.assertEqual(m.meta_info["compounds"]["x"].common_name, None)

    def test_add_compound_duplicate_update_newmeta(self):
        m = Model()
        m.add_compound(compound="x", **{"common_name": "A"})
        with self.assertWarns(UserWarning):
            m.add_compound(compound="x", **{"common_name": "X"})
            self.assertEqual(m.meta_info["compounds"]["x"].common_name, "X")



class ModelTests(unittest.TestCase):
    """Tests for compound methods"""

    ############################################################################
    # Adding compounds
    # This should be type checked, we really only want to have compounds as
    # strings, not as everything else
    ############################################################################

    def test_add_compound_str(self):
        m = Model()
        m.add_compound(compound="x")
        self.assertEqual(m.compounds, ["x"])

    def test_add_compound_fail_on_int(self):
        m = Model()
        with self.assertRaises(TypeError):
            m.add_compound(compound=1)

    def test_add_compound_fail_on_float(self):
        m = Model()
        with self.assertRaises(TypeError):
            m.add_compound(compound=1.0)

    def test_add_compound_fail_on_list(self):
        m = Model()
        with self.assertRaises(TypeError):
            m.add_compound(compound=["a"])

    def test_add_compound_fail_on_tuple(self):
        m = Model()
        with self.assertRaises(TypeError):
            m.add_compound(compound=("a",))

    def test_add_compound_fail_on_set(self):
        m = Model()
        with self.assertRaises(TypeError):
            m.add_compound(compound={"a"})

    def test_add_compound_fail_on_dict(self):
        m = Model()
        with self.assertRaises(TypeError):
            m.add_compound(compound={"a": 1})

    def test_add_compounds_str(self):
        m = Model()
        m.add_compounds(compounds="xyz")
        self.assertEqual(m.compounds, ["x", "y", "z"])

    def test_add_compounds_tuple(self):
        m = Model()
        m.add_compounds(compounds=("x", "y", "z"))
        self.assertEqual(m.compounds, ["x", "y", "z"])

    def test_add_compounds_list(self):
        m = Model()
        m.add_compounds(compounds=["x", "y", "z"])
        self.assertEqual(m.compounds, ["x", "y", "z"])

    def test_add_compounds_set(self):
        m = Model()
        m.add_compounds(compounds={"x", "y", "z"})
        self.assertEqual(set(m.compounds), set(["x", "y", "z"]))

    def test_add_compounds_dict(self):
        m = Model()
        m.add_compounds(
            compounds=("x", "y", "z"),
            meta_info={
                "x": {"common_name": "cpd-x"},
                "y": {"common_name": "cpd-y"},
                "z": {"common_name": "cpd-z"},
            },
        )
        self.assertEqual(m.compounds, ["x", "y", "z"])
        self.assertEqual(m.meta_info["compounds"]["x"].common_name, "cpd-x")
        self.assertEqual(m.meta_info["compounds"]["y"].common_name, "cpd-y")
        self.assertEqual(m.meta_info["compounds"]["z"].common_name, "cpd-z")

    def test_add_compounds_fail_on_int(self):
        m = Model()
        with self.assertRaises(TypeError):
            m.add_compounds(compounds=1)

    def test_add_compounds_fail_on_float(self):
        m = Model()
        with self.assertRaises(TypeError):
            m.add_compounds(compounds=1.0)

    def test_add_compounds_fail_on_none(self):
        m = Model()
        with self.assertRaises(TypeError):
            m.add_compounds(compounds=None)

    def test_add_compounds_duplicate_sets(self):
        m = Model()
        m.add_compounds(compounds={"x", "y", "z"})
        with self.assertWarns(UserWarning):
            m.add_compounds(compounds={"x", "y", "z"})
            self.assertEqual(set(m.compounds), set(["x", "y", "z"]))


    ############################################################################
    # Removing compounds
    ############################################################################

    def test_remove_compound_beginning(self):
        m = Model()
        m.add_compounds(compounds=["x", "y", "z"])
        m.remove_compound(compound="x")
        self.assertEqual(m.compounds, ["y", "z"])

    def test_remove_compound_middle(self):
        m = Model()
        m.add_compounds(compounds=["x", "y", "z"])
        m.remove_compound(compound="y")
        self.assertEqual(m.compounds, ["x", "z"])

    def test_remove_compound_end(self):
        m = Model()
        m.add_compounds(compounds=["x", "y", "z"])
        m.remove_compound(compound="z")
        self.assertEqual(m.compounds, ["x", "y"])

    def test_remove_compounds_str(self):
        m = Model()
        m.add_compounds(compounds=["x", "y", "z"])
        m.remove_compounds(compounds="xy")
        self.assertEqual(m.compounds, ["z"])

    def test_remove_compounds_tuple(self):
        m = Model()
        m.add_compounds(compounds=["x", "y", "z"])
        m.remove_compounds(compounds=("x", "y"))
        self.assertEqual(m.compounds, ["z"])

    def test_remove_compounds_list(self):
        m = Model()
        m.add_compounds(compounds=["x", "y", "z"])
        m.remove_compounds(compounds=["x", "y"])
        self.assertEqual(m.compounds, ["z"])

    def test_remove_compounds_set(self):
        m = Model()
        m.add_compounds(compounds=["x", "y", "z"])
        m.remove_compounds(compounds={"x", "y"})
        self.assertEqual(m.compounds, ["z"])

    def test_remove_compounds_dict(self):
        m = Model()
        m.add_compounds(compounds=["x", "y", "z"])
        m.remove_compounds(compounds={"x": 1, "y": 1})
        self.assertEqual(m.compounds, ["z"])

    ############################################################################
    # Updating meta info
    ############################################################################

    def test_update_compound_meta_info(self):
        m = Model()
        m.add_compound(compound="x")
        m.update_compound_meta_info(compound="x", meta_info={"common_name": "X"})
        self.assertEqual(m.compounds, ["x"])
        self.assertEqual(m.meta_info["compounds"]["x"].common_name, "X")

    def test_update_compound_meta_info_replacing(self):
        m = Model()
        m.add_compound(compound="x", **{"common_name": "X1"})
        m.update_compound_meta_info(compound="x", meta_info={"common_name": "X2"})
        self.assertEqual(m.meta_info["compounds"]["x"].common_name, "X2")

    def test_update_compound_meta_info_additional(self):
        m = Model()
        m.add_compound(compound="x", **{"common_name": "X"})
        m.update_compound_meta_info(compound="x", meta_info={"compartment": "e"})
        self.assertEqual(m.meta_info["compounds"]["x"].common_name, "X")
        self.assertEqual(m.meta_info["compounds"]["x"].compartment, "e")

    ############################################################################
    # Getting compounds
    ############################################################################

    def test_get_compounds(self):
        m = Model()
        m.add_compounds(compounds=("x", "y", "z"))
        self.assertEqual(m.compounds, m.get_compounds())


class SourceCodeTests(unittest.TestCase):
    def test_generate_compounds_source_code_single(self):
        m = Model()
        m.add_compound("x")
        self.assertEqual(
            m._generate_compounds_source_code(include_meta_info=False),
            "m.add_compounds(compounds=['x'])",
        )
        self.assertEqual(
            m._generate_compounds_source_code(include_meta_info=True),
            "m.add_compounds(compounds=['x'], meta_info={'x': {'compartment': 'c'}})",
        )

    def test_generate_compounds_source_code_multiple(self):
        m = Model()
        m.add_compounds(["x", "y"])
        self.assertEqual(
            m._generate_compounds_source_code(include_meta_info=False),
            "m.add_compounds(compounds=['x', 'y'])",
        )
        self.assertEqual(
            m._generate_compounds_source_code(include_meta_info=True),
            "m.add_compounds(compounds=['x', 'y'], meta_info={'x': {'compartment': 'c'}, 'y': {'compartment': 'c'}})",
        )


class SBMLTests(unittest.TestCase):
    def test_create_sbml_compounds_without_meta_info(self):
        m = Model()
        m.add_compound("x")
        doc = m._create_sbml_document()
        sbml_model = m._create_sbml_model(doc)
        m._create_sbml_compounds(sbml_model)

        cpd = sbml_model.getListOfSpecies()[0]
        self.assertEqual(cpd.getId(), "x")
        self.assertEqual(cpd.getName(), "")
        self.assertEqual(cpd.getCompartment(), "c")
        self.assertEqual(cpd.getCharge(), 0)
        self.assertEqual(cpd.getPlugin("fbc").getChemicalFormula(), "")
        self.assertEqual(cpd.getConstant(), False)
        self.assertEqual(cpd.getBoundaryCondition(), False)

    def test_create_sbml_compounds_with_meta_info(self):
        m = Model()
        m.add_compound(
            "x",
            **{
                "common_name": "Glucose",
                "charge": -2.0,
                "compartment": "e",
                "formula": "C6H12O6",
            }
        )

        doc = m._create_sbml_document()
        sbml_model = m._create_sbml_model(doc)
        m._create_sbml_compounds(sbml_model)

        cpd = sbml_model.getListOfSpecies()[0]
        self.assertEqual(cpd.getId(), "x")
        self.assertEqual(cpd.getName(), "Glucose")
        self.assertEqual(cpd.getCompartment(), "e")
        self.assertEqual(cpd.getPlugin("fbc").getCharge(), -2)
        self.assertEqual(cpd.getPlugin("fbc").getChemicalFormula(), "C6H12O6")
        self.assertEqual(cpd.getConstant(), False)
        self.assertEqual(cpd.getBoundaryCondition(), False)
