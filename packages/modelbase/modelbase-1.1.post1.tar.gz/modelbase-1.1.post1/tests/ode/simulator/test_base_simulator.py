import unittest
import numpy as np

from tempfile import TemporaryDirectory
from modelbase.ode import Model, Simulator
from modelbase.ode import ratefunctions as rf


def GENERATE_RESULTS():
    parameters = {"k_in": 1, "kf": 1, "kr": 1}
    m = Model(parameters=parameters)
    m.add_compounds(["a", "b", "c1", "c2", "d1", "d2", "rate_time"])

    # Vanilla algebraic module
    m.add_algebraic_module(
        module_name="vanilla_module",
        function=lambda a: (a, 2 * a),
        compounds=["a"],
        derived_compounds=["a1", "a2"],
        modifiers=None,
        parameters=None,
    )

    # Time-dependent algebraic module
    m.add_algebraic_module(
        module_name="time_dependent_module",
        function=lambda time: (time,),
        compounds=None,
        derived_compounds=["derived_time"],
        modifiers=["time"],
        parameters=None,
    )

    # Singleton reaction
    m.add_reaction(
        rate_name="singleton_reaction",
        function=lambda k_in: k_in,
        stoichiometry={"b": 1},
        modifiers=None,
        parameters=["k_in"],
        reversible=False,
    )

    # Time-dependent reaction
    m.add_reaction(
        rate_name="time_dependent_reaction",
        function=lambda time: time,
        stoichiometry={"rate_time": 1},
        modifiers=["time"],
        parameters=None,
        reversible=False,
    )
    # Vanilla reaction
    m.add_reaction(
        rate_name="vanilla_reaction",
        function=rf.mass_action_1,
        stoichiometry={"c1": -1, "c2": 1},
        modifiers=None,
        parameters=["kf"],
        reversible=False,
    )
    # Reversible reaction
    m.add_reaction(
        rate_name="reversible_reaction",
        function=rf.reversible_mass_action_1_1,
        stoichiometry={"d1": -1, "d2": 1},
        modifiers=None,
        parameters=["kf", "kr"],
        reversible=True,
    )
    y0 = {
        "a": 1,
        "b": 1,
        "c1": 1,
        "c2": 0,
        "d1": 1,
        "d2": 0,
        "rate_time": 1,
    }
    s = Simulator(m)
    s.initialise(y0=y0)
    t, y = s.simulate(t_end=10, steps=10)
    return s.copy()


SIM = GENERATE_RESULTS()


class SimulatorBaseTests(unittest.TestCase):
    def test_init(self):
        m = Model()
        s = Simulator(m)
        self.assertEqual(s.model, m)

    def test_init_wrong_name(self):
        m = Model()
        with self.assertRaises(NotImplementedError):
            Simulator(model=m, integrator_name="something-other")

    def test_init_wrong_model_type(self):
        class TestModel:
            pass

        m_weird = TestModel()
        with self.assertRaises(NotImplementedError):
            Simulator(model=m_weird)

    def test_init_from_results(self):
        m = Model(parameters={"k_in": 1})
        m.add_compound(compound="x")
        m.add_reaction(
            rate_name="v1",
            function=rf.constant,
            stoichiometry={"x": 1},
            parameters=["k_in"],
        )
        s1 = Simulator(m)
        s1.initialise({"x": 0})
        t, y = s1.simulate(1)

        s2 = Simulator(m, **{"time": s1.time, "results": s1.results})
        np.testing.assert_array_equal(s2.time, s1.time)
        np.testing.assert_array_equal(s2.results, s1.results)

    def test_store_and_load_results_wrong_type(self):
        s = SIM.copy()
        with self.assertRaises(ValueError):
            s.store_results_to_file(filename="test", filetype="wurst")
        with self.assertRaises(ValueError):
            s.load_results_from_file(filename="test", filetype="wurst")

    def test_store_and_load_results(self):
        s = SIM.copy()
        with TemporaryDirectory() as tmpdir:
            s.store_results_to_file(filename=tmpdir + "test.json", filetype="json")
            s.load_results_from_file(filename=tmpdir + "test.json", filetype="json")
        self.assertTrue(s.time is not None)
        self.assertTrue(s.results is not None)

    def test_store_and_load_results_without_suffix(self):
        s = SIM.copy()
        with TemporaryDirectory() as tmpdir:
            s.store_results_to_file(filename=tmpdir + "test", filetype="json")
            s.load_results_from_file(filename=tmpdir + "test.json", filetype="json")
        self.assertTrue(s.time is not None)
        self.assertTrue(s.results is not None)

    def test_store_and_load_results_pickle(self):
        s = SIM.copy()
        with TemporaryDirectory() as tmpdir:
            s.store_results_to_file(filename=tmpdir + "test.p", filetype="pickle")
            s.load_results_from_file(filename=tmpdir + "test.p", filetype="pickle")
        self.assertTrue(s.time is not None)
        self.assertTrue(s.results is not None)

    def test_store_and_load_results_without_suffix_pickle(self):
        s = SIM.copy()
        with TemporaryDirectory() as tmpdir:
            s.store_results_to_file(filename=tmpdir + "test", filetype="pickle")
            s.load_results_from_file(filename=tmpdir + "test.p", filetype="pickle")
        self.assertTrue(s.time is not None)
        self.assertTrue(s.results is not None)

    def test_clear_results(self):
        s = SIM.copy()
        s.clear_results()
        self.assertFalse(s.time)
        self.assertFalse(s.results)


class SimulationTests(unittest.TestCase):
    def test_initialise(self):
        parameters = {"alpha": 1}
        m = Model(parameters=parameters)
        m.add_compound(compound="x")
        s = Simulator(model=m)
        s.initialise(y0={"x": 1}, test_run=False)
        self.assertEqual(s.y0, [1])

    def test_initialise_prior_results(self):
        parameters = {"alpha": 1}
        m = Model(parameters=parameters)
        m.add_compound(compound="x")
        m.add_reaction(
            rate_name="v1",
            function=lambda x, alpha: alpha * x,
            stoichiometry={"x": 1},
            modifiers=["x"],
            parameters=["alpha"],
            reversible=False,
        )
        y0 = {"x": 1}
        s = Simulator(model=m)
        s.initialise(y0=y0, test_run=False)
        s.time = [1, 2, 3]
        s.results = [1, 2, 3]

        s.initialise(y0=y0, test_run=False)
        self.assertFalse(s.time)
        self.assertFalse(s.results)

    def test_simulation_no_y0(self):
        parameters = {"alpha": 1}
        m = Model(parameters=parameters)
        m.add_compound(compound="x")
        m.add_reaction(
            rate_name="v1",
            function=lambda x, alpha: alpha * x,
            stoichiometry={"x": 1},
            modifiers=["x"],
            parameters=["alpha"],
            reversible=False,
        )
        s = Simulator(model=m)
        with self.assertRaises(AttributeError):
            s.simulate(t_end=10)

    def test_simulation_one_variable_test_run(self):
        parameters = {"alpha": 1}
        m = Model(parameters=parameters)
        m.add_compound(compound="x")
        m.add_reaction(
            rate_name="v1",
            function=lambda x, alpha: alpha * x,
            stoichiometry={"x": 1},
            modifiers=["x"],
            parameters=["alpha"],
            reversible=False,
        )
        y0 = {"x": 1}
        s = Simulator(model=m)
        s.initialise(y0=y0, test_run=True)

    def test_simulation_one_variable(self):
        parameters = {"alpha": 1}
        m = Model(parameters=parameters)
        m.add_compound(compound="x")
        m.add_reaction(
            rate_name="v1",
            function=lambda x, alpha: alpha * x,
            stoichiometry={"x": 1},
            modifiers=["x"],
            parameters=["alpha"],
            reversible=False,
        )
        y0 = {"x": 1}
        s = Simulator(model=m)
        s.initialise(y0=y0, test_run=False)
        t, y = s.simulate(t_end=10)
        self.assertTrue(np.isclose(t[-1], 10))
        self.assertTrue(np.isclose(s.time[0][-1], 10))
        self.assertTrue(np.isclose(y[-1], np.exp(10)))
        self.assertTrue(np.isclose(s.results[0][-1][0], np.exp(10)))

    def test_continuous_simulation(self):
        parameters = {"alpha": 1}
        m = Model(parameters=parameters)
        m.add_compound(compound="x")
        m.add_reaction(
            rate_name="v1",
            function=lambda x, alpha: alpha * x,
            stoichiometry={"x": 1},
            modifiers=["x"],
            parameters=["alpha"],
            reversible=False,
        )
        y0 = {"x": 1}
        s = Simulator(model=m)
        s.initialise(y0=y0, test_run=False)
        t, y = s.simulate(t_end=5, steps=5)
        self.assertTrue(np.isclose(t[-1], 5))
        self.assertTrue(np.isclose(y, np.exp(range(6)).reshape(6, 1)).all())
        self.assertTrue(np.isclose(s.time[0][-1], 5))
        self.assertTrue(np.isclose(s.results[0], np.exp(range(6)).reshape(6, 1)).all())

        t, y = s.simulate(t_end=10, steps=5)
        self.assertTrue(np.isclose(t[-1], 10))
        self.assertTrue(np.isclose(s.time[0][-1], 5))
        self.assertTrue(np.isclose(s.time[1][-1], 10))

        self.assertTrue(np.isclose(y, np.exp(range(5, 11)).reshape(6, 1)).all())
        self.assertTrue(np.isclose(s.results[0], np.exp(range(6)).reshape(6, 1)).all())
        self.assertTrue(
            np.isclose(s.results[1], np.exp(range(6, 11)).reshape(5, 1)).all()
        )
        y = s.get_results_array()
        self.assertTrue(np.isclose(y, np.exp(range(11)).reshape(11, 1)).all())

    def test_internal_results_shape(self):
        s = SIM.copy()
        self.assertEqual(s.time[0].shape, (11,))
        self.assertEqual(s.results[0].shape, (11, 7))

    def test_get_time_shape(self):
        s = SIM.copy()
        self.assertEqual(s.get_time(concatenated=True).shape, (11,))
        self.assertEqual(s.get_time(concatenated=False)[0].shape, (11,))

    def test_get_fluxes_dict_shape(self):
        s = SIM.copy()
        fluxes = s.get_fluxes_dict(concatenated=True)
        self.assertEqual(fluxes["singleton_reaction"].shape, (11,))
        self.assertEqual(fluxes["time_dependent_reaction"].shape, (11,))
        self.assertEqual(fluxes["vanilla_reaction"].shape, (11,))
        self.assertEqual(fluxes["reversible_reaction"].shape, (11,))

        fluxes = s.get_fluxes_dict(concatenated=False)[0]
        self.assertEqual(fluxes["singleton_reaction"].shape, (11,))
        self.assertEqual(fluxes["time_dependent_reaction"].shape, (11,))
        self.assertEqual(fluxes["vanilla_reaction"].shape, (11,))
        self.assertEqual(fluxes["reversible_reaction"].shape, (11,))

    def test_get_fluxes_array_shape(self):
        s = SIM.copy()
        fluxes = s.get_fluxes_array(concatenated=True)
        self.assertEqual(fluxes.shape, (11, 4))

        fluxes = s.get_fluxes_array(concatenated=False)[0]
        self.assertEqual(fluxes.shape, (11, 4))

    def test_get_fluxes_df_shape(self):
        s = SIM.copy()
        fluxes = s.get_fluxes_df(concatenated=True)
        self.assertEqual(fluxes.values.shape, (11, 4))
        self.assertEqual(
            fluxes.index.values.tolist(),
            [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
        )
        self.assertEqual(
            fluxes.columns.values.tolist(),
            [
                "singleton_reaction",
                "time_dependent_reaction",
                "vanilla_reaction",
                "reversible_reaction",
            ],
        )

        fluxes = s.get_fluxes_df(concatenated=False)[0]
        self.assertEqual(fluxes.values.shape, (11, 4))
        self.assertEqual(
            fluxes.index.values.tolist(),
            [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
        )
        self.assertEqual(
            fluxes.columns.values.tolist(),
            [
                "singleton_reaction",
                "time_dependent_reaction",
                "vanilla_reaction",
                "reversible_reaction",
            ],
        )

    def test_get_results_dict_shape(self):
        s = SIM.copy()
        res = s.get_results_dict(concatenated=True)
        self.assertEqual(res["a"].shape, (11,))
        self.assertEqual(res["b"].shape, (11,))
        self.assertEqual(res["c1"].shape, (11,))
        self.assertEqual(res["c2"].shape, (11,))
        self.assertEqual(res["d1"].shape, (11,))
        self.assertEqual(res["d2"].shape, (11,))
        self.assertEqual(res["rate_time"].shape, (11,))

        res = s.get_results_dict(concatenated=False)[0]
        self.assertEqual(res["a"].shape, (11,))
        self.assertEqual(res["b"].shape, (11,))
        self.assertEqual(res["c1"].shape, (11,))
        self.assertEqual(res["c2"].shape, (11,))
        self.assertEqual(res["d1"].shape, (11,))
        self.assertEqual(res["d2"].shape, (11,))
        self.assertEqual(res["rate_time"].shape, (11,))

    def test_get_results_array_shape(self):
        s = SIM.copy()
        self.assertEqual(s.get_results_array(concatenated=True).shape, (11, 7))
        self.assertEqual(s.get_results_array(concatenated=False)[0].shape, (11, 7))

    def test_get_results_df_shape(self):
        s = SIM.copy()
        res = s.get_results_df(concatenated=True)
        self.assertEqual(res.values.shape, (11, 7))
        self.assertEqual(
            res.index.values.tolist(),
            [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
        )
        self.assertEqual(
            res.columns.values.tolist(), ["a", "b", "c1", "c2", "d1", "d2", "rate_time"]
        )

        res = s.get_results_df(concatenated=False)[0]
        self.assertEqual(res.values.shape, (11, 7))
        self.assertEqual(
            res.index.values.tolist(),
            [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
        )
        self.assertEqual(
            res.columns.values.tolist(), ["a", "b", "c1", "c2", "d1", "d2", "rate_time"]
        )
