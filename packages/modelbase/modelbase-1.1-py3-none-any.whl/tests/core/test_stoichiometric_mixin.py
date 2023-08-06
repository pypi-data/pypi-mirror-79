import unittest
import numpy as np

from modelbase.ode import Model


class ModelBasicTests(unittest.TestCase):
    def test_init_empty(self):
        m = Model()
        self.assertEqual(m.compounds, [])
        self.assertEqual(m.stoichiometries, {})
        self.assertEqual(m.stoichiometries_by_compounds, {})

    def test_enter(self):
        pass

    def test_exit(self):
        pass

    def test_copy(self):
        pass


class ModelWarningsTests(unittest.TestCase):
    def test_warn_on_stoichiometry_replacement(self):
        m = Model()
        m.add_compounds(compounds=["x", "y"])
        m.add_stoichiometry(rate_name="v1", stoichiometry={"x": -1, "y": 1})
        with self.assertWarns(UserWarning):
            m.add_stoichiometry(rate_name="v1", stoichiometry={"x": -1, "y": 1})

    def test_warn_on_stoichiometry_by_compounds_replacement(self):
        m = Model()
        m.add_compounds(compounds=["x"])
        m.add_stoichiometry_by_compound(compound="x", stoichiometry={"v1": -1})
        with self.assertWarns(UserWarning):
            m.add_stoichiometry_by_compound(compound="x", stoichiometry={"v1": -1})


class ModelTests(unittest.TestCase):
    """Tests for stoichiometry methods"""

    def test_init(self):
        m = Model(
            rate_stoichiometries={"v1": {"x": -1, "y": 1}, "v2": {"x": 1, "y": -1}}
        )
        self.assertEqual(m.stoichiometries["v1"], {"x": -1, "y": 1})
        self.assertEqual(m.stoichiometries["v2"], {"x": 1, "y": -1})
        self.assertEqual(m.stoichiometries_by_compounds["x"], {"v1": -1, "v2": 1})
        self.assertEqual(m.stoichiometries_by_compounds["y"], {"v1": 1, "v2": -1})

    def test_add_stoichiometry(self):
        m = Model()
        m.add_compounds(compounds=("x", "y"))
        m.add_stoichiometry(rate_name="v1", stoichiometry={"x": -1, "y": 1})
        self.assertEqual(m.stoichiometries, {"v1": {"x": -1, "y": 1}})
        self.assertEqual(m.stoichiometries_by_compounds["x"], {"v1": -1})
        self.assertEqual(m.stoichiometries_by_compounds["y"], {"v1": 1})

    def test_add_stoichiometry_by_compound(self):
        m = Model()
        m.add_compounds(compounds=("x", "y"))
        m.add_stoichiometry_by_compound(compound="x", stoichiometry={"v1": -1})
        m.add_stoichiometry_by_compound(compound="y", stoichiometry={"v1": 1})
        self.assertEqual(m.stoichiometries, {"v1": {"x": -1, "y": 1}})
        self.assertEqual(m.stoichiometries_by_compounds["x"], {"v1": -1})
        self.assertEqual(m.stoichiometries_by_compounds["y"], {"v1": 1})

    def test_add_stoichiometries(self):
        m = Model()
        m.add_compounds(compounds=("x", "y"))
        m.add_stoichiometries(
            rate_stoichiometries={"v1": {"x": -1, "y": 1}, "v2": {"x": 1, "y": -1}}
        )
        self.assertEqual(m.stoichiometries["v1"], {"x": -1, "y": 1})
        self.assertEqual(m.stoichiometries["v2"], {"x": 1, "y": -1})
        self.assertEqual(m.stoichiometries_by_compounds["x"], {"v1": -1, "v2": 1})
        self.assertEqual(m.stoichiometries_by_compounds["y"], {"v1": 1, "v2": -1})

    def test_add_stoichiometries_by_compounds(self):
        m = Model()
        m.add_compounds(compounds=("x", "y"))
        m.add_stoichiometries_by_compounds(
            compound_stoichiometries={
                "x": {"v1": -1, "v2": 1},
                "y": {"v1": 1, "v2": -1},
            }
        )
        self.assertEqual(m.stoichiometries["v1"], {"x": -1, "y": 1})
        self.assertEqual(m.stoichiometries["v2"], {"x": 1, "y": -1})
        self.assertEqual(m.stoichiometries_by_compounds["x"], {"v1": -1, "v2": 1})
        self.assertEqual(m.stoichiometries_by_compounds["y"], {"v1": 1, "v2": -1})

    def test_remove_rate_stoichiometry(self):
        m = Model()
        m.add_compounds(compounds=("x", "y"))
        m.add_stoichiometries(
            rate_stoichiometries={"v1": {"x": -1, "y": 1}, "v2": {"x": 1, "y": -1}}
        )
        m.remove_rate_stoichiometry(rate_name="v1")
        self.assertEqual(m.stoichiometries["v2"], {"x": 1, "y": -1})
        self.assertEqual(m.stoichiometries_by_compounds["x"], {"v2": 1})
        self.assertEqual(m.stoichiometries_by_compounds["y"], {"v2": -1})

    def test_remove_rate_stoichiometries(self):
        m = Model()
        m.add_compounds(compounds=("x", "y"))
        m.add_stoichiometries(
            rate_stoichiometries={"v1": {"x": -1, "y": 1}, "v2": {"x": 1, "y": -1}}
        )
        m.remove_rate_stoichiometries(rate_names=("v1", "v2"))
        self.assertEqual(m.stoichiometries, {})
        self.assertEqual(m.stoichiometries_by_compounds, {})

    def test_remove_compound_stoichiometry(self):
        m = Model()
        m.add_compounds(compounds=("x", "y"))
        m.add_stoichiometries(
            rate_stoichiometries={"v1": {"x": -1, "y": 1}, "v2": {"x": 1, "y": -1}}
        )
        m.remove_compound_stoichiometry(compound="x")
        self.assertEqual(m.stoichiometries["v1"], {"y": 1})
        self.assertEqual(m.stoichiometries["v2"], {"y": -1})
        self.assertEqual(m.stoichiometries_by_compounds["y"], {"v1": 1, "v2": -1})

    def test_remove_compound_stoichiometries(self):
        m = Model()
        m.add_compounds(compounds=("x", "y"))
        m.add_stoichiometries(
            rate_stoichiometries={"v1": {"x": -1, "y": 1}, "v2": {"x": 1, "y": -1}}
        )
        m.remove_compound_stoichiometries(compounds=("x", "y"))
        self.assertEqual(m.stoichiometries, {})
        self.assertEqual(m.stoichiometries_by_compounds, {})

    def test_get_rate_stoichiometry(self):
        m = Model()
        m.add_compounds(compounds=("x", "y"))
        m.add_stoichiometry(rate_name="v1", stoichiometry={"x": -1, "y": 1})
        self.assertEqual(m.get_rate_stoichiometry(rate_name="v1"), {"x": -1, "y": 1})

    def test_get_compound_stoichiometry(self):
        m = Model()
        m.add_compounds(compounds=("x", "y"))
        m.add_stoichiometry(rate_name="v1", stoichiometry={"x": -1, "y": 1})
        self.assertEqual(m.get_compound_stoichiometry(compound="x"), {"v1": -1})
        self.assertEqual(m.get_compound_stoichiometry(compound="y"), {"v1": 1})

    def test_get_stoichiometries(self):
        m = Model()
        m.add_compounds(compounds=("x", "y"))
        m.add_stoichiometries(
            rate_stoichiometries={"v1": {"x": -1, "y": 1}, "v2": {"x": 1, "y": -1}}
        )
        self.assertEqual(m.stoichiometries, m.get_stoichiometries())

    def test_get_stoichiometries_by_compounds(self):
        m = Model()
        m.add_compounds(compounds=("x", "y"))
        m.add_stoichiometries(
            rate_stoichiometries={"v1": {"x": -1, "y": 1}, "v2": {"x": 1, "y": -1}}
        )
        self.assertEqual(
            m.stoichiometries_by_compounds, m.get_stoichiometries_by_compounds()
        )

    def test_get_stoichiometric_matrix(self):
        m = Model()
        m.add_compounds(("x", "y", "z"))
        m.add_stoichiometries_by_compounds(
            compound_stoichiometries={
                "x": {"v1": 1, "v2": -1},
                "y": {"v2": 1, "v3": -1},
                "z": {"v3": 1, "v4": -1},
            }
        )

        expected = np.array(
            [[1.0, -1.0, 0.0, 0.0], [0.0, 1.0, -1.0, 0.0], [0.0, 0.0, 1.0, -1.0]]
        )
        np.testing.assert_array_equal(m.get_stoichiometric_matrix(), expected)

    def test_get_stoichiometric_df(self):
        m = Model()
        m.add_compounds(("x", "y", "z"))
        m.add_stoichiometries_by_compounds(
            compound_stoichiometries={
                "x": {"v1": 1, "v2": -1},
                "y": {"v2": 1, "v3": -1},
                "z": {"v3": 1, "v4": -1},
            }
        )

        expected = np.array(
            [[1.0, -1.0, 0.0, 0.0], [0.0, 1.0, -1.0, 0.0], [0.0, 0.0, 1.0, -1.0]]
        )
        df = m.get_stoichiometric_df()
        np.testing.assert_array_equal(df.values, expected)
        self.assertEqual(df.index.to_list(), ["x", "y", "z"])
        self.assertEqual(df.columns.to_list(), ["v1", "v2", "v3", "v4"])

    def test_get_stoichiometric_matrix_sorted(self):
        m = Model()
        m.add_compounds(("x", "y", "z"))
        m.add_stoichiometries_by_compounds(
            compound_stoichiometries={
                "x": {"v1": 1, "v2": -1},
                "y": {"v2": 1, "v3": -1},
                "z": {"v3": 1, "v4": -1},
            }
        )
        m.remove_rate_stoichiometry(rate_name="v2")
        m.add_stoichiometry(rate_name="v2", stoichiometry={"x": -1, "y": 1})

        expected = np.array(
            [[1.0, -1.0, 0.0, 0.0], [0.0, 1.0, -1.0, 0.0], [0.0, 0.0, 1.0, -1.0]]
        )
        np.testing.assert_array_equal(m.get_stoichiometric_matrix(), expected)

    def test_get_stoichiometric_df_sorted(self):
        m = Model()
        m.add_compounds(("x", "y", "z"))
        m.add_stoichiometries_by_compounds(
            compound_stoichiometries={
                "x": {"v1": 1, "v2": -1},
                "y": {"v2": 1, "v3": -1},
                "z": {"v3": 1, "v4": -1},
            }
        )
        m.remove_rate_stoichiometry(rate_name="v2")
        m.add_stoichiometry(rate_name="v2", stoichiometry={"x": -1, "y": 1})

        expected = np.array(
            [[1.0, -1.0, 0.0, 0.0], [0.0, 1.0, -1.0, 0.0], [0.0, 0.0, 1.0, -1.0]]
        )
        df = m.get_stoichiometric_df()
        np.testing.assert_array_equal(df.values, expected)
        self.assertEqual(df.index.to_list(), ["x", "y", "z"])
        self.assertEqual(df.columns.to_list(), ["v1", "v2", "v3", "v4"])


class SourceCodeTests(unittest.TestCase):
    def test_generate_stoichiometries_source_code(self):
        m = Model()
        m.add_compounds(compounds=("x", "y"))
        m.add_stoichiometry(rate_name="v1", stoichiometry={"x": -1, "y": 1})
        self.assertEqual(
            m._generate_stoichiometries_source_code(),
            "m.add_stoichiometries(rate_stoichiometries={'v1': {'x': -1, 'y': 1}})",
        )


class SBMLTests(unittest.TestCase):
    def test_create_sbml_stoichiometries(self):
        m = Model()
        m.add_compounds(compounds=("x", "y"))
        m.add_stoichiometry(rate_name="v1", stoichiometry={"x": -1, "y": 1})
        doc = m._create_sbml_document()
        sbml_model = m._create_sbml_model(doc)
        m._create_sbml_stoichiometries(sbml_model)
        rxn = sbml_model.getReaction("v1")
        self.assertEqual(rxn.getId(), "v1")
        self.assertEqual(rxn.getListOfReactants()[0].getSpecies(), "x")
        self.assertEqual(rxn.getListOfProducts()[0].getSpecies(), "y")
