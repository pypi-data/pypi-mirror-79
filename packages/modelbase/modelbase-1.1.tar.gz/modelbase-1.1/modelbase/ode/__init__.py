from .models.model import Model
from .models.labelmodel import LabelModel
from .models.linearlabelmodel import LinearLabelModel

from .simulators.simulator import _Simulate
from .simulators.labelsimulator import _LabelSimulate
from .simulators.linearlabelsimulator import _LinearLabelSimulate

from .utils import mca
from .utils import ratelaws
from .utils import ratefunctions
from .utils import algebraicfunctions


def Simulator(model, integrator_name="assimulo", **kwargs):
    """Choose the simulator class according to the model type.

    If a simulator different than assimulo is required, it can be chosen
    by the integrator argument.

    Parameters
    ----------
    model : modelbase.model
        The model instance

    Returns
    -------
    Simulate : object
        A simulate object according to the model type
    """
    if integrator_name not in ("assimulo", "scipy"):
        raise NotImplementedError(
            "Currently only {assimulo, scipy} are supported as integrators"
        )
    if isinstance(model, LabelModel):
        return _LabelSimulate(model=model, integrator_name=integrator_name, **kwargs)
    elif isinstance(model, LinearLabelModel):
        return _LinearLabelSimulate(
            model=model, integrator_name=integrator_name, **kwargs
        )
    elif isinstance(model, Model):
        return _Simulate(model=model, integrator_name=integrator_name, **kwargs)
    else:
        raise NotImplementedError
