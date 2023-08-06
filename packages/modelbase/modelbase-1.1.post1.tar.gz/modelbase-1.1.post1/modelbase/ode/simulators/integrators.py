"""Write me."""

import numpy as np
import scipy.integrate as spi

try:
    from assimulo.solvers import CVode
    from assimulo.problem import Explicit_Problem
except ImportError:  # pragma: no cover
    pass
else:
    ASSIMULO_SUPPORT_FLAG = True

    class _IntegratorAssimulo:
        """Wrap around assimulo CVODE."""

        def __init__(self, rhs, y0):
            self.problem = Explicit_Problem(rhs, y0)
            self.integrator = CVode(self.problem)

        def _simulate(
            self, t_end=None, steps=None, time_points=None, **integrator_kwargs
        ):
            """Simulate.

            Parameters
            ----------
            integrator_kwargs: https://jmodelica.org/assimulo/explicit.html#cvode
                atol, default 1.0e-6
                backward
                clock_step
                discr
                display_progress
                dqrhomax
                dqtype
                external_event_detection
                inith
                linear_solver
                maxcor
                maxcorS
                maxh
                maxkrylov
                maxncf, default 10
                maxnef, default 7
                maxord
                maxsteps
                minh
                norm
                num_threads
                pbar
                precond
                report_continuosly
                rtol, default 1.0e-6
                sensmethod
                suppress_sens
                time_limit
                usejac
                usesens
                verbosity
            """
            if steps is None:
                steps = 0
            for k, v in integrator_kwargs.items():
                setattr(self.integrator, k, v)
            return self.integrator.simulate(t_end, steps, time_points)

        def _simulate_to_steady_state(
            self, tolerance, integrator_kwargs, simulation_kwargs
        ):
            for k, v in integrator_kwargs.items():
                setattr(self.integrator, k, v)
            if "max_rounds" in simulation_kwargs:
                max_rounds = simulation_kwargs["max_rounds"]
            else:
                max_rounds = 3
            self._reset()
            t_end = 1000
            for n_round in range(1, max_rounds + 1):
                try:
                    t, y = self.integrator.simulate(t_end)
                    if np.linalg.norm(y[-1] - y[-2], ord=2) < tolerance:
                        return t[-1], y[-1]
                    else:
                        t_end *= 1000
                except:  # pragma: no cover
                    raise ValueError("Could not find a steady state")
            raise ValueError("Could not find a steady state")

        def _reset(self):
            """Reset the integrator."""
            self.integrator.reset()


class _IntegratorScipy:
    """Wrapper around scipy.odeint and scipy.ode."""

    def __init__(self, rhs, y0):
        self.rhs = rhs
        self.t0 = 0
        self.y0 = y0
        self.y0_orig = y0.copy()

    def _simulate(self, t_end=None, steps=None, time_points=None, **integrator_kwargs):
        if time_points is not None:
            if time_points[0] != 0:
                t = [0]
                t.extend(time_points)
            else:
                t = time_points

        elif steps is not None:
            # Scipy counts the total amount of return points rather than
            # steps as assimulo
            steps += 1
            t = np.linspace(self.t0, t_end, steps)
        else:
            t = np.linspace(self.t0, t_end, 100)
        y = spi.odeint(func=self.rhs, y0=self.y0, t=t, tfirst=True, **integrator_kwargs)
        self.t0 = t[-1]
        self.y0 = y[-1, :]
        return t, y

    def _simulate_to_steady_state(
        self, tolerance, integrator_kwargs, simulation_kwargs
    ):
        if "step_size" in simulation_kwargs:
            step_size = simulation_kwargs["step_size"]
        else:
            step_size = 1
        if "max_steps" in simulation_kwargs:
            max_steps = simulation_kwargs["max_steps"]
        else:
            max_steps = 100000
        if "integrator" in simulation_kwargs:
            integrator = simulation_kwargs["integrator"]
        else:
            integrator = "lsoda"
        self._reset()
        integ = spi.ode(self.rhs)
        integ.set_integrator(name=integrator, **integrator_kwargs)
        integ.set_initial_value(self.y0)
        t = self.t0 + step_size
        y0 = self.y0
        for step in range(max_steps):
            y = integ.integrate(t)
            if np.linalg.norm(y - y0, ord=2) < tolerance:
                return t, y
            else:
                y0 = y
                t += step_size
        raise ValueError("Could not find a steady state")

    def _reset(self):
        self.t0 = 0
        self.y0 = self.y0_orig.copy()
