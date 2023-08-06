import unittest
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from modelbase.ode import LabelModel, Simulator


def GENERATE_RESULTS():
    l = LabelModel()
    l.add_label_compounds({"x": 2, "y": 2, "z": 4})
    l.add_labelmap_reaction(
        rate_name="v1",
        function=lambda x, y: x - y,
        stoichiometry={"x": -1, "y": 1},
        labelmap=[1, 0],
        reversible=True,
    )
    l.add_labelmap_reaction(
        rate_name="v2",
        function=lambda x, y, z: x * y - z,
        stoichiometry={"x": -1, "y": -1, "z": 1},
        labelmap=[0, 1, 2, 3],
        reversible=True,
    )

    base_y0 = {"x": 2, "y": 2, "z": 4}
    y0 = l.generate_y0(base_y0=base_y0, label_positions={"x": 0})
    s = Simulator(model=l)
    s.initialise(y0=y0)
    t, y = s.simulate(t_end=100, steps=10)
    return s


SIM = GENERATE_RESULTS()


class LabelSimualtorTests(unittest.TestCase):
    def test_generate_y0(self):
        l = LabelModel()
        l.add_label_compounds({"x": 2, "y": 2, "z": 4})
        base_y0 = {"x": 2, "y": 2, "z": 4}
        s = Simulator(l)
        self.assertEqual(
            l.generate_y0(base_y0, label_positions={"x": 0}),
            s.generate_y0(base_y0, label_positions={"x": 0}),
        )

    def test_get_total_concentration(self):
        s = SIM.copy()
        np.testing.assert_array_almost_equal(
            s.get_total_concentration(compound="x"), 2.0
        )
        np.testing.assert_array_almost_equal(
            s.get_total_concentration(compound="y"), 2.0
        )
        np.testing.assert_array_almost_equal(
            s.get_total_concentration(compound="z"), 4.0
        )

    def test_get_labeled_and_unlabeled(self):
        s = SIM.copy()
        np.testing.assert_array_almost_equal(
            s.get_unlabeled_concentration(compound="x")
            + s.get_total_label_concentration(compound="x"),
            2.0,
        )
        np.testing.assert_array_almost_equal(
            s.get_unlabeled_concentration(compound="y")
            + s.get_total_label_concentration(compound="y"),
            2.0,
        )
        np.testing.assert_array_almost_equal(
            s.get_unlabeled_concentration(compound="z")
            + s.get_total_label_concentration(compound="z"),
            4.0,
        )

    def test_get_all_isotopomer_concentrations_df(self):
        s = SIM.copy()
        df = s.get_all_isotopomer_concentrations_df(compound="x")
        np.testing.assert_array_equal(
            df.index,
            [0.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0],
        )
        np.testing.assert_array_equal(df.columns, ["x__00", "x__01", "x__10", "x__11"])
        np.testing.assert_array_almost_equal(df.sum(axis=1).values, 2)

    def test_get_all_isotopomer_concentrations_dict(self):
        s = SIM.copy()
        d = s.get_all_isotopomer_concentrations_dict(compound="x")
        self.assertEqual(list(d.keys()), ["x__00", "x__01", "x__10", "x__11"])
        np.testing.assert_array_almost_equal(np.sum(list(d.values()), axis=0), 2)

    def test_get_all_isotopomer_concentrations_array(self):
        s = SIM.copy()
        arr = s.get_all_isotopomer_concentrations_array(compound="x")
        self.assertEqual(arr.shape, (11, 4))
        np.testing.assert_array_almost_equal(arr.sum(axis=1), 2)

    def test_get_concentrations_by_reg_exp_df(self):
        s = SIM.copy()
        pd.testing.assert_frame_equal(
            s.get_concentrations_by_reg_exp_df(reg_exp="x__\d+"),
            s.get_all_isotopomer_concentrations_df(compound="x"),
        )

    def test_get_concentrations_by_reg_exp_dict(self):
        s = SIM.copy()
        s.get_concentrations_by_reg_exp_dict(
            reg_exp="x__\d+"
        ).keys() == s.get_all_isotopomer_concentrations_dict(compound="x").keys()

    def test_get_concentrations_by_reg_exp_array(self):
        s = SIM.copy()
        np.testing.assert_array_equal(
            s.get_concentrations_by_reg_exp_array(reg_exp="x__\d+"),
            s.get_all_isotopomer_concentrations_array(compound="x"),
        )

    def test_get_concentration_at_positions(self):
        s = SIM.copy()
        np.testing.assert_array_almost_equal(
            (
                s.get_concentration_at_positions(compound="x", positions=0)
                + s.get_concentration_at_positions(compound="x", positions=1)
                + s.get_unlabeled_concentration(compound="x")
            ),
            2,
        )

    def test_get_concentrations_of_n_labeled_array(self):
        s = SIM.copy()
        s.get_concentrations_of_n_labeled_array(compound="x", n_labels=1)
        np.testing.assert_array_almost_equal(
            (
                s.get_concentrations_of_n_labeled_array(compound="x", n_labels=0).sum(
                    axis=1
                )
                + s.get_concentrations_of_n_labeled_array(compound="x", n_labels=1).sum(
                    axis=1
                )
                + s.get_concentrations_of_n_labeled_array(compound="x", n_labels=2).sum(
                    axis=1
                )
            ),
            2,
        )

    def test_get_concentrations_of_n_labeled_dict(self):
        s = SIM.copy()
        s.get_concentrations_of_n_labeled_dict(compound="x", n_labels=1)
        list(s.get_concentrations_of_n_labeled_dict(compound="x", n_labels=0).keys()), [
            "x__00"
        ]
        list(s.get_concentrations_of_n_labeled_dict(compound="x", n_labels=1).keys()), [
            "x__10",
            "x__01",
        ]
        list(s.get_concentrations_of_n_labeled_dict(compound="x", n_labels=2).keys()), [
            "x__11"
        ]

    def test_get_concentrations_of_n_labeled_df(self):
        s = SIM.copy()
        self.assertEqual(
            list(
                s.get_concentrations_of_n_labeled_df(compound="x", n_labels=0).columns
            ),
            ["x__00"],
        )
        self.assertEqual(
            list(
                s.get_concentrations_of_n_labeled_df(compound="x", n_labels=1).columns
            ),
            ["x__10", "x__01"],
        )
        self.assertEqual(
            list(
                s.get_concentrations_of_n_labeled_df(compound="x", n_labels=2).columns
            ),
            ["x__11"],
        )


class PlottingTests(unittest.TestCase):
    def test_plot(self):
        s = SIM.copy()
        fig, ax = s.plot()
        plt.close()

    def test_plot_label_distribution(self):
        s = SIM.copy()
        fig, ax = s.plot_label_distribution(compound="x")
        plt.close()

    def test_plot_label_distribution_grid(self):
        s = SIM.copy()
        fig, ax = s.plot_label_distribution_grid(compounds=["x", "y", "z"])
        plt.close()

    def test_plot_all_label_distributions(self):
        s = SIM.copy()
        fig, ax = s.plot_all_label_distributions()
        plt.close()
