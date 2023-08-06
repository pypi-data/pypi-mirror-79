import unittest
import libsbml
import tempfile
import pathlib
from datetime import datetime

from modelbase.ode import Model
from modelbase.core.utils import convert_sbml_id


class BaseModelTests(unittest.TestCase):
    def test_init_empty(self):
        m = Model()
        self.assertTrue(m)
        self.assertEqual(
            m.meta_info["model"].__dict__,
            {
                "sbo": "SBO:0000062",
                "id": f"modelbase-model-{datetime.now().date().strftime('%Y-%m-%d')}",
                "name": "modelbase-model",
                "units": {
                    "per_second": {
                        "kind": 28,
                        "exponent": -1,
                        "scale": 0,
                        "multiplier": 1,
                    }
                },
                "compartments": {
                    "c": {
                        "name": "cytosol",
                        "is_constant": True,
                        "size": 1,
                        "spatial_dimensions": 3,
                        "units": "litre",
                    }
                },
                "notes": {},
            },
        )

    def test_init_meta_info(self):
        m = Model(meta_info={"name": "my-model"})
        self.assertEqual(m.meta_info["model"].name, "my-model")

    def test_enter(self):
        m = Model()
        with m as m_dup:
            self.assertIsNot(m, m_dup)

    def test_exit(self):
        m = Model()
        with m:
            m.test = 1
        with self.assertRaises(AttributeError):
            m.test

    def test_copy(self):
        m = Model()
        m_copy = m.copy()
        self.assertIsNot(m, m_copy)

    def test_add_meta_info(self):
        m = Model()
        m.update_meta_info(component="model", meta_info={"sbo": "123"})
        self.assertEqual(
            m.meta_info["model"].__dict__,
            {
                "sbo": "123",
                "id": f"modelbase-model-{datetime.now().date().strftime('%Y-%m-%d')}",
                "name": "modelbase-model",
                "units": {
                    "per_second": {
                        "kind": 28,
                        "exponent": -1,
                        "scale": 0,
                        "multiplier": 1,
                    }
                },
                "compartments": {
                    "c": {
                        "name": "cytosol",
                        "is_constant": True,
                        "size": 1,
                        "spatial_dimensions": 3,
                        "units": "litre",
                    }
                },
                "notes": {},
            },
        )


class SBMLTests(unittest.TestCase):
    def test_create_sbml_document(self):
        m = Model()
        doc = m._create_sbml_document()
        self.assertEqual(doc.getLevel(), 3)
        self.assertEqual(doc.getVersion(), 2)
        self.assertEqual(doc.getSBOTerm(), 62)

    def test_create_sbml_model(self):
        m = Model()
        doc = m._create_sbml_document()
        sbml_model = m._create_sbml_model(doc)
        self.assertEqual(
            convert_sbml_id(sbml_model.getId(), prefix="MODEL"),
            f"modelbase-model-{datetime.now().date().strftime('%Y-%m-%d')}",
        )
        self.assertEqual(
            convert_sbml_id(sbml_model.getName(), prefix="MODEL"), "modelbase-model"
        )
        self.assertEqual(sbml_model.getTimeUnits(), "second")
        self.assertEqual(sbml_model.getExtentUnits(), "mole")
        self.assertEqual(sbml_model.getSubstanceUnits(), "mole")

    def test_create_sbml_units(self):
        m = Model()
        doc = m._create_sbml_document()
        sbml_model = m._create_sbml_model(doc=doc)
        m._create_sbml_units(sbml_model)

        unit_definition = sbml_model.unit_definitions[0]
        self.assertEqual(unit_definition.getId(), "per_second")

        unit = unit_definition.getListOfUnits()[0]
        self.assertEqual(unit.getKind(), libsbml.UNIT_KIND_SECOND)
        self.assertEqual(unit.getExponent(), -1)
        self.assertEqual(unit.getScale(), 0)
        self.assertEqual(unit.getMultiplier(), 1)

    def test_create_sbml_compartments(self):
        m = Model()
        doc = m._create_sbml_document()
        sbml_model = m._create_sbml_model(doc)
        m._create_sbml_compartments(sbml_model)

        compartment = sbml_model.getListOfCompartments()[0]
        self.assertEqual(compartment.getId(), "c")
        self.assertEqual(compartment.getName(), "cytosol")
        self.assertEqual(compartment.getConstant(), True)
        self.assertEqual(compartment.getSize(), 1.0)
        self.assertEqual(compartment.getSpatialDimensions(), 3)
        self.assertEqual(compartment.getUnits(), "litre")

    def test_write_sbml_model_file(self):
        m = Model()
        with tempfile.TemporaryDirectory() as tmpdir:
            path = pathlib.Path(tmpdir) / "testfile.xml"
            m.write_sbml_model(str(path))
            self.assertTrue(path.is_file())

    def test_write_sbml_model_strin(self):
        m = Model()
        s = m.write_sbml_model()
        self.assertTrue(isinstance(s, str))
