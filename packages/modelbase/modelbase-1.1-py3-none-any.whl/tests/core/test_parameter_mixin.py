import unittest
import tempfile

from modelbase.ode import Model


class ModelBasicTests(unittest.TestCase):
    def test_init_empty(self):
        m = Model()
        self.assertEqual(m.parameters, {})
        self.assertEqual(m.parameters, m.initialization_parameters)
        self.assertIsNot(m.parameters, m.initialization_parameters)

    def test_init_parameters(self):
        parameters = {"k1": 1}
        m = Model(parameters=parameters)
        self.assertEqual(m.parameters, parameters)
        self.assertEqual(m.parameters, m.initialization_parameters)
        self.assertIsNot(m.parameters, m.initialization_parameters)

    def test_enter(self):
        parameters = {"k1": 1}
        m = Model(parameters=parameters)
        with m as m_dup:
            m_dup.parameters["k1"] = 2
            self.assertEqual(m_dup.parameters["k1"], 2)
            self.assertEqual(m.parameters["k1"], 1)

    def test_exit(self):
        parameters = {"k1": 1}
        m = Model(parameters=parameters)
        with m:
            m.parameters["k1"] = 2
            self.assertEqual(m.parameters["k1"], 2)
        self.assertEqual(m.parameters["k1"], 1)

    def test_copy(self):
        parameters = {"k1": 1}
        m1 = Model(parameters=parameters)
        m2 = m1.copy()
        self.assertIsNot(m1, m2)
        self.assertIsNot(m1.parameters, m2.parameters)
        self.assertEqual(m1.parameters, m2.parameters)


class ModelTests(unittest.TestCase):
    def test_add_parameter(self):
        m = Model()
        m.add_parameter(parameter_name="k1", parameter_value=1)
        self.assertEqual(m.parameters["k1"], 1)

    def test_add_parameter_fail_on_existing(self):
        m = Model()
        m.add_parameter(parameter_name="k1", parameter_value=1)
        with self.assertWarns(UserWarning):
            m.add_parameter(parameter_name="k1", parameter_value=1)

    def test_add_parameters(self):
        m = Model()
        m.add_parameters(parameters={"k1": 1, "k2": 2})
        self.assertEqual(m.parameters["k1"], 1)
        self.assertEqual(m.parameters["k2"], 2)

    def test_update_parameter(self):
        parameters = {"k1": 1}
        m = Model(parameters=parameters)
        m.update_parameter(parameter_name="k1", parameter_value=2)
        self.assertTrue(m.parameters["k1"], 2)

    def test_update_parameter_fail_on_new(self):
        m = Model()
        with self.assertWarns(UserWarning):
            m.update_parameter(parameter_name="k1", parameter_value=2)

    def test_update_parameters(self):
        m = Model()
        m.add_parameters(parameters={"k1": 1, "k2": 2})
        m.update_parameters(parameters={"k1": 2, "k2": 3})
        self.assertEqual(m.parameters["k1"], 2)
        self.assertEqual(m.parameters["k2"], 3)

    def test_add_and_update_parameter_new(self):
        m = Model()
        m.add_and_update_parameter(parameter_name="k1", parameter_value=1)
        self.assertEqual(m.parameters["k1"], 1)

    def test_add_and_update_parameter_existing(self):
        m = Model()
        m.add_parameter(parameter_name="k1", parameter_value=1)
        m.add_and_update_parameter(parameter_name="k1", parameter_value=2)
        self.assertEqual(m.parameters["k1"], 2)

    def test_add_and_update_parameters(self):
        m = Model()
        m.add_parameter(parameter_name="k1", parameter_value=1)
        m.add_and_update_parameters(parameters={"k1": 2, "k2": 3})
        self.assertEqual(m.parameters["k1"], 2)
        self.assertEqual(m.parameters["k2"], 3)

    def test_remove_parameter(self):
        parameters = {"k1": 1, "k2": 2}
        m = Model(parameters=parameters)
        m.remove_parameter(parameter_name="k1")
        self.assertEqual(m.parameters, {"k2": 2})

    def test_remove_parameters(self):
        parameters = {"k1": 1, "k2": 2}
        m = Model(parameters=parameters)
        m.remove_parameters(parameter_names=["k1", "k2"])
        self.assertEqual(m.parameters, {})

    def test_store_and_load_parameters_new_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            parameters = {"k1": 1, "k2": 2}
            m1 = Model(parameters=parameters)
            m2 = Model()
            m1.store_parameters_to_file(filename=f"{tmpdir}/test", filetype="json")
            m2.load_parameters_from_file(
                filename=f"{tmpdir}/test.json", filetype="json"
            )
            self.assertEqual(m1.parameters, m2.parameters)
        with tempfile.TemporaryDirectory() as tmpdir:
            parameters = {"k1": 1, "k2": 2}
            m1 = Model(parameters=parameters)
            m2 = Model()
            m1.store_parameters_to_file(filename=f"{tmpdir}/test.json", filetype="json")
            m2.load_parameters_from_file(
                filename=f"{tmpdir}/test.json", filetype="json"
            )
            self.assertEqual(m1.parameters, m2.parameters)

    def test_store_and_load_parameters_new_pickle(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            parameters = {"k1": 1, "k2": 2}
            m1 = Model(parameters=parameters)
            m2 = Model()
            m1.store_parameters_to_file(filename=f"{tmpdir}/test", filetype="pickle")
            m2.load_parameters_from_file(filename=f"{tmpdir}/test.p", filetype="pickle")
            self.assertEqual(m1.parameters, m2.parameters)
        with tempfile.TemporaryDirectory() as tmpdir:
            parameters = {"k1": 1, "k2": 2}
            m1 = Model(parameters=parameters)
            m2 = Model()
            m1.store_parameters_to_file(filename=f"{tmpdir}/test.p", filetype="pickle")
            m2.load_parameters_from_file(filename=f"{tmpdir}/test.p", filetype="pickle")
            self.assertEqual(m1.parameters, m2.parameters)

    def test_store_and_load_parameters_existing_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            parameters = {"k1": 1, "k2": 2}
            m1 = Model(parameters=parameters)
            m2 = Model(parameters=parameters)
            m1.store_parameters_to_file(filename=f"{tmpdir}/test", filetype="json")
            m2.load_parameters_from_file(
                filename=f"{tmpdir}/test.json", filetype="json"
            )
            self.assertEqual(m1.parameters, m2.parameters)
        with tempfile.TemporaryDirectory() as tmpdir:
            parameters = {"k1": 1, "k2": 2}
            m1 = Model(parameters=parameters)
            m2 = Model(parameters=parameters)
            m1.store_parameters_to_file(filename=f"{tmpdir}/test.json", filetype="json")
            m2.load_parameters_from_file(
                filename=f"{tmpdir}/test.json", filetype="json"
            )
            self.assertEqual(m1.parameters, m2.parameters)

    def test_store_and_load_parameters_existing_pickle(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            parameters = {"k1": 1, "k2": 2}
            m1 = Model(parameters=parameters)
            m2 = Model(parameters=parameters)
            m1.store_parameters_to_file(filename=f"{tmpdir}/test", filetype="pickle")
            m2.load_parameters_from_file(filename=f"{tmpdir}/test.p", filetype="pickle")
            self.assertEqual(m1.parameters, m2.parameters)
        with tempfile.TemporaryDirectory() as tmpdir:
            parameters = {"k1": 1, "k2": 2}
            m1 = Model(parameters=parameters)
            m2 = Model(parameters=parameters)
            m1.store_parameters_to_file(filename=f"{tmpdir}/test.p", filetype="pickle")
            m2.load_parameters_from_file(filename=f"{tmpdir}/test.p", filetype="pickle")
            self.assertEqual(m1.parameters, m2.parameters)

    def test_store_and_load_parameters_fail_on_other(self):
        m = Model()
        with self.assertRaises(ValueError):
            with tempfile.TemporaryDirectory() as tmpdir:
                m.store_parameters_to_file(filename=f"{tmpdir}/test", filetype="xml")

        with self.assertRaises(ValueError):
            with tempfile.TemporaryDirectory() as tmpdir:
                m.load_parameters_from_file(filename=f"{tmpdir}/test", filetype="xml")

    def test_restore_initialization_parameters(self):
        parameters = {"k1": 1}
        m = Model(parameters=parameters)
        m.update_parameter("k1", 5)
        m.add_parameter("k2", 2)
        m.restore_initialization_parameters()
        self.assertEqual(m.parameters["k1"], 1)
        with self.assertRaises(KeyError):
            m.parameters["k2"]

    def test_get_parameter(self):
        parameters = {"k1": 1}
        m = Model(parameters=parameters)
        self.assertEqual(m.get_parameter(parameter_name="k1"), 1)

    def test_get_parameters(self):
        parameters = {"k1": 1, "k2": 2}
        m = Model(parameters=parameters)
        self.assertEqual(m.get_parameters(), {"k1": 1, "k2": 2})

    ############################################################################
    # Updating meta info
    ############################################################################

    def test_update_parameter_meta_info(self):
        m = Model()
        m.add_parameter(parameter_name="x", parameter_value=0)
        m.update_parameter_meta_info(parameter="x", meta_info={"unit": "X"})
        self.assertEqual(m.meta_info["parameters"]["x"].unit, "X")

    def test_update_parameter_meta_info_replacing(self):
        m = Model()
        m.add_parameter(parameter_name="x", parameter_value=0, **{"unit": "X1"})
        m.update_parameter_meta_info(parameter="x", meta_info={"unit": "X2"})
        self.assertEqual(m.meta_info["parameters"]["x"].unit, "X2")


class DerivedParameterTests(unittest.TestCase):
    def test_add_derived_parameter(self):
        m = Model()
        m.add_parameters({"k_fwd": 1, "k_eq": 10})
        m.add_derived_parameter(
            parameter_name="k_bwd",
            function=lambda kf, keq: kf / keq,
            parameters=["k_fwd", "k_eq"],
        )
        self.assertEqual(m.parameters, {"k_fwd": 1, "k_eq": 10, "k_bwd": 0.1})
        self.assertEqual(m.derived_parameters["k_bwd"]["parameters"], ["k_fwd", "k_eq"])
        self.assertEqual(m._derived_from_parameters, {"k_fwd", "k_eq"})

    def test_remove_derived_parameter(self):
        m = Model()
        m.add_parameters({"k_fwd": 1, "k_eq": 10})
        m.add_derived_parameter(
            parameter_name="k_bwd",
            function=lambda kf, keq: kf / keq,
            parameters=["k_fwd", "k_eq"],
        )
        m.remove_derived_parameter("k_bwd")
        self.assertEqual(m.parameters, {"k_fwd": 1, "k_eq": 10})
        self.assertEqual(m.derived_parameters, {})
        self.assertEqual(m._derived_from_parameters, set())

    def test_remove_derived_parameter_multiple_dependencies(self):
        m = Model()
        m.add_parameters({"k_fwd": 1, "k_eq": 10})
        m.add_derived_parameter(
            parameter_name="k_bwd",
            function=lambda kf, keq: kf / keq,
            parameters=["k_fwd", "k_eq"],
        )
        m.add_derived_parameter(
            parameter_name="k_bwd2",
            function=lambda kf, keq: kf / keq,
            parameters=["k_fwd", "k_eq"],
        )
        m.remove_derived_parameter("k_bwd")
        self.assertEqual(m.parameters, {"k_fwd": 1, "k_eq": 10, "k_bwd2": 0.1})
        self.assertEqual(m._derived_from_parameters, {"k_fwd", "k_eq"})

    def test_update_derived_parameters_on_update(self):
        m = Model()
        m.add_parameters({"k_fwd": 1, "k_eq": 10})
        m.add_derived_parameter(
            parameter_name="k_bwd",
            function=lambda kf, keq: kf / keq,
            parameters=["k_fwd", "k_eq"],
        )
        m.update_parameter("k_fwd", 2)
        self.assertEqual(m.parameters["k_bwd"], 0.2)

    def test_update_derived_parameters_on_add(self):
        m = Model()
        m.add_parameters({"k_fwd": 1, "k_eq": 10})
        m.add_derived_parameter(
            parameter_name="k_bwd",
            function=lambda kf, keq: kf / keq,
            parameters=["k_fwd", "k_eq"],
        )
        with self.assertWarns(UserWarning):
            m.add_parameter("k_fwd", 2)
        self.assertEqual(m.parameters["k_bwd"], 0.2)

    def test_update_derived_parameters_on_add_and_update(self):
        m = Model()
        m.add_parameters({"k_fwd": 1, "k_eq": 10})
        m.add_derived_parameter(
            parameter_name="k_bwd",
            function=lambda kf, keq: kf / keq,
            parameters=["k_fwd", "k_eq"],
        )
        m.add_and_update_parameter("k_fwd", 2)
        self.assertEqual(m.parameters["k_bwd"], 0.2)


class SourceCodeTests(unittest.TestCase):
    def test_generate_parameters_source_code(self):
        m = Model()
        m.add_parameter("k_in", 1, **{"unit": "mM"})
        self.assertEqual(
            m._generate_parameters_source_code(include_meta_info=True),
            "m.add_parameters(parameters={'k_in': 1}, meta_info={'k_in': {'unit': 'mM'}})",
        )
        self.assertEqual(
            m._generate_parameters_source_code(include_meta_info=False),
            "m.add_parameters(parameters={'k_in': 1})",
        )


class SBMLTests(unittest.TestCase):
    def test_create_sbml_parameters_without_meta_info(self):
        m = Model()
        m.add_parameter("k_in", 1)
        doc = m._create_sbml_document()
        sbml_model = m._create_sbml_model(doc)
        m._create_sbml_parameters(sbml_model)
        parameter = sbml_model.getListOfParameters()[0]
        self.assertEqual(parameter.getId(), "k_in")
        self.assertEqual(parameter.getValue(), 1.0)
        self.assertEqual(parameter.getConstant(), True)
        self.assertEqual(parameter.getUnits(), "")

    def test_create_sbml_parameters_with_meta_info(self):
        m = Model()
        m.add_parameter("k_in", 1, **{"unit": "mM"})
        doc = m._create_sbml_document()
        sbml_model = m._create_sbml_model(doc)
        m._create_sbml_parameters(sbml_model)
        parameter = sbml_model.getListOfParameters()[0]
        self.assertEqual(parameter.getId(), "k_in")
        self.assertEqual(parameter.getValue(), 1.0)
        self.assertEqual(parameter.getConstant(), True)
        self.assertEqual(parameter.getUnits(), "mM")
