import unittest
import numpy as np

from modelbase.ode import LinearLabelModel


class CreationTests(unittest.TestCase):
    def test_add_compound(self):
        m = LinearLabelModel()
        m.add_compound(compound="x", num_labels=3)
        self.assertEqual(m.compounds, ["x__0", "x__1", "x__2"])
        self.assertEqual(m.isotopomers, {"x": ["x__0", "x__1", "x__2"]})

    def test_add_compound_replacing(self):
        m = LinearLabelModel()
        m.add_compound(compound="x", num_labels=3)
        with self.assertWarns(UserWarning):
            m.add_compound(compound="x", num_labels=1)
        self.assertEqual(m.compounds, ["x__0"])
        self.assertEqual(m.isotopomers, {"x": ["x__0"]})

    def test_add_compound_fail_on_no_labels(self):
        m = LinearLabelModel()
        with self.assertRaises(ValueError):
            m.add_compound(compound="x", num_labels=0)

    def test_add_compounds(self):
        m = LinearLabelModel()
        m.add_compounds(compounds={"x": 1, "y": 2})
        self.assertEqual(m.compounds, ["x__0", "y__0", "y__1"])
        self.assertEqual(m.isotopomers, {"x": ["x__0"], "y": ["y__0", "y__1"]})

    def test_add_rate(self):
        m = LinearLabelModel()
        m.add_rate(rate_name="v1__1", base_name="v1", substrate="x")
        self.assertEqual(m.rates, {"v1__1": {"base_name": "v1", "substrate": "x"}})

    def test_add_rate_replacing(self):
        m = LinearLabelModel()
        m.add_rate(rate_name="v1__1", base_name="v1", substrate="x")
        with self.assertWarns(UserWarning):
            m.add_rate(rate_name="v1__1", base_name="v1", substrate="y")
            self.assertEqual(m.rates, {"v1__1": {"base_name": "v1", "substrate": "y"}})

    def test_add_reaction(self):
        m = LinearLabelModel()
        m.add_compounds({"x": 2, "y": 2})
        m.add_reaction(rate_name="v1", stoichiometry={"x": -1, "y": 1}, labelmap=[0, 1])

        self.assertEqual(
            m.stoichiometries,
            {"v1__0": {"x__0": -1, "y__0": 1}, "v1__1": {"x__1": -1, "y__1": 1}},
        )
        self.assertEqual(m.rates["v1__0"], {"base_name": "v1", "substrate": "x__0"})
        self.assertEqual(m.rates["v1__1"], {"base_name": "v1", "substrate": "x__1"})

    def test_add_reaction_replacing(self):
        m = LinearLabelModel()
        m.add_compounds({"x": 2, "y": 2})
        m = LinearLabelModel()
        m.add_compounds({"x": 2, "y": 2, "z": 2})
        m.add_reaction(rate_name="v1", stoichiometry={"x": -1, "y": 1}, labelmap=[0, 1])
        with self.assertWarns(UserWarning):
            m.add_reaction(
                rate_name="v1", stoichiometry={"x": -1, "z": 1}, labelmap=[0, 1]
            )

        self.assertEqual(
            m.stoichiometries,
            {"v1__0": {"x__0": -1, "z__0": 1}, "v1__1": {"x__1": -1, "z__1": 1}},
        )
        self.assertEqual(m.rates["v1__0"], {"base_name": "v1", "substrate": "x__0"})
        self.assertEqual(m.rates["v1__1"], {"base_name": "v1", "substrate": "x__1"})

    def test_add_reaction_influx(self):
        m = LinearLabelModel()
        m.add_compounds({"x": 1})
        with self.assertWarns(UserWarning):
            m.add_reaction(rate_name="v1", stoichiometry={"x": 1}, labelmap=[0])
        self.assertEqual(m.stoichiometries, {"v1__0": {"EXT": -1, "x__0": 1}})

    def test_add_reaction_outflux(self):
        m = LinearLabelModel()
        m.add_compounds({"x": 1})
        m.add_reaction(rate_name="v1", stoichiometry={"x": -1}, labelmap=[0])
        self.assertEqual(m.stoichiometries, {"v1__0": {"x__0": -1, "EXT": 1}})

    def test_add_reaction_fail_on_missing_labels(self):
        m = LinearLabelModel()
        m.add_compounds({"x": 2})
        with self.assertRaises(ValueError):
            m.add_reaction(rate_name="v1", stoichiometry={"x": -1}, labelmap=[0])


class GenerateY0Test(unittest.TestCase):
    def test_generate_y0(self):
        m = LinearLabelModel()
        m.add_compounds({"x": 2})
        self.assertEqual(m.generate_y0(), {"x__0": 0, "x__1": 0})

    def test_generate_y0_single(self):
        m = LinearLabelModel()
        m.add_compounds({"x": 2})
        self.assertEqual(
            m.generate_y0(initial_labels={"x": 0}), {"x__0": 1.0, "x__1": 0}
        )

    def test_generate_y0_distributed(self):
        m = LinearLabelModel()
        m.add_compounds({"x": 2})
        self.assertEqual(
            m.generate_y0(initial_labels={"x": [0, 1]}), {"x__0": 0.5, "x__1": 0.5}
        )


class SimulationTests(unittest.TestCase):
    def test_get_fluxes(self):
        m = LinearLabelModel()
        m.add_compounds(compounds={"x": 2, "y": 2})
        m.add_reaction(rate_name="v1", stoichiometry={"x": -1, "y": 1}, labelmap=[0, 1])
        y0 = m.generate_y0({"x": 0})
        v_ss = {"v1": 1}
        self.assertEqual(m._get_fluxes(y=y0, v_ss=v_ss), {"v1__0": 1.0, "v1__1": 0})

    def test_get_fluxes_reverse(self):
        m = LinearLabelModel()
        m.add_compounds(compounds={"x": 2, "y": 2})
        m.add_reaction(rate_name="v1", stoichiometry={"x": -1, "y": 1}, labelmap=[1, 0])
        y0 = m.generate_y0({"x": 0})
        v_ss = {"v1": 1}

        self.assertEqual(m._get_fluxes(y=y0, v_ss=v_ss), {"v1__0": 0, "v1__1": 1.0})

    def test_get_fluxes_dict_array_df(self):
        v_ss = {"v1": 1}
        m = LinearLabelModel()
        m.add_compounds(compounds={"x": 2, "y": 2})
        m.add_reaction(rate_name="v1", stoichiometry={"x": -1, "y": 1}, labelmap=[0, 1])
        y0 = m.generate_y0({"x": 0})

        # non-dict input
        self.assertEqual(
            m.get_fluxes_dict(y=list(y0.values()), v_ss=v_ss),
            {"v1__0": 1.0, "v1__1": 0},
        )

        # dict
        self.assertEqual(m.get_fluxes_dict(y=y0, v_ss=v_ss), {"v1__0": 1.0, "v1__1": 0})

        # array
        np.testing.assert_array_equal(m.get_fluxes_array(y=y0, v_ss=v_ss), [1, 0])

        # df
        df = m.get_fluxes_df(y=y0, v_ss=v_ss)
        np.testing.assert_array_equal(df.index.values, [0])
        np.testing.assert_array_equal(df.columns.values, ["v1__0", "v1__1"])
        np.testing.assert_array_equal(df.values, [[1.0, 0.0]])

    def test_get_rhs(self):
        v_ss = {"v1": 1}
        y_ss = {"x": 2, "y": 4}

        m = LinearLabelModel()
        m.add_compounds(compounds={"x": 2, "y": 2})
        m.add_reaction(rate_name="v1", stoichiometry={"x": -1, "y": 1}, labelmap=[0, 1])
        y0 = list(m.generate_y0({"x": 0}).values())
        m._v_ss = v_ss
        m._y_ss = y_ss
        m._external_label = 1
        self.assertEqual(m._get_rhs(0, y0), [-0.5, 0.0, 0.25, 0.0])

    def test_get_rhs_reverse(self):
        v_ss = {"v1": 1}
        y_ss = {"x": 2, "y": 4}

        m = LinearLabelModel()
        m.add_compounds(compounds={"x": 2, "y": 2})
        m.add_reaction(rate_name="v1", stoichiometry={"x": -1, "y": 1}, labelmap=[1, 0])
        y0 = list(m.generate_y0({"x": 0}).values())
        m._v_ss = v_ss
        m._y_ss = y_ss
        m._external_label = 1
        self.assertEqual(m._get_rhs(0, y0), [-0.5, 0.0, 0, 0.25])

    def test_get_right_hand_side(self):
        v_ss = {"v1": 1}
        y_ss = {"x": 2, "y": 4}

        m = LinearLabelModel()
        m.add_compounds(compounds={"x": 2, "y": 2})
        m.add_reaction(rate_name="v1", stoichiometry={"x": -1, "y": 1}, labelmap=[0, 1])
        y0 = m.generate_y0({"x": 0})
        # dict input
        self.assertEqual(
            m.get_right_hand_side(y_labels=y0, y_ss=y_ss, v_ss=v_ss),
            {"x__0": -0.5, "x__1": 0.0, "y__0": 0.25, "y__1": 0.0},
        )
        # list input
        self.assertEqual(
            m.get_right_hand_side(y_labels=list(y0.values()), y_ss=y_ss, v_ss=v_ss),
            {"x__0": -0.5, "x__1": 0.0, "y__0": 0.25, "y__1": 0.0},
        )


class SBMLTests(unittest.TestCase):
    def test_create_sbml_reactions(self):
        m = LinearLabelModel()
        m.add_compounds(compounds={"x": 2, "y": 2})
        m.add_reaction(rate_name="v1", stoichiometry={"x": -1, "y": 1}, labelmap=[0, 1])

        doc = m._create_sbml_document()
        sbml_model = m._create_sbml_model(doc)
        m._create_sbml_reactions(sbml_model)
        rxn = sbml_model.getReaction("v1__0")
        self.assertEqual(rxn.getListOfReactants()[0].getSpecies(), "x__0")
        self.assertEqual(rxn.getListOfReactants()[0].getStoichiometry(), 1.0)
        self.assertEqual(rxn.getListOfProducts()[0].getSpecies(), "y__0")
        self.assertEqual(rxn.getListOfProducts()[0].getStoichiometry(), 1.0)
        self.assertEqual(rxn.getKineticLaw().getFormula(), "v1 * x__0")

        rxn = sbml_model.getReaction("v1__1")
        self.assertEqual(rxn.getListOfReactants()[0].getSpecies(), "x__1")
        self.assertEqual(rxn.getListOfReactants()[0].getStoichiometry(), 1.0)
        self.assertEqual(rxn.getListOfProducts()[0].getSpecies(), "y__1")
        self.assertEqual(rxn.getListOfProducts()[0].getStoichiometry(), 1.0)
        self.assertEqual(rxn.getKineticLaw().getFormula(), "v1 * x__1")

    def test_model_to_sbml(self):
        m = LinearLabelModel()
        m.add_compounds(compounds={"x": 2, "y": 2})
        m.add_reaction(rate_name="v1", stoichiometry={"x": -1, "y": 1}, labelmap=[0, 1])
        m._model_to_sbml()
        self.assertTrue(True)
