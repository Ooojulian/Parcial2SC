"""Feigenbaum constant and bifurcation analysis."""

from typing import List, Tuple
from dataclasses import dataclass
import numpy as np
from numpy.typing import NDArray


# Feigenbaum constant (theoretical)
FEIGENBAUM_DELTA = 4.669201609102990


@dataclass
class BifurcationPoint:
    """Bifurcation point data."""
    parameter: float
    period: int
    eigenvalue: float


class LogisticMap:
    """Logistic map: x_{n+1} = r*x_n(1-x_n)"""

    def __init__(self, r: float):
        """Initialize with parameter r."""
        self.r = r

    def iterate(self, x: float, steps: int = 1) -> float:
        """Iterate map steps times."""
        for _ in range(steps):
            x = self.r * x * (1.0 - x)
        return x

    def orbit(self, x0: float, steps: int = 100, transient: int = 50) -> List[float]:
        """Compute orbit, discarding transient."""
        x = x0
        for _ in range(transient):
            x = self.iterate(x)

        return [self.iterate(x) for _ in range(steps)]

    def fixed_point(self) -> float:
        """Compute fixed point (1-1/r) or 0."""
        if self.r > 1:
            return 1.0 - 1.0 / self.r
        return 0.0

    def derivative_at_fixed(self, x_star: float) -> float:
        """Derivative of map at fixed point: r(1-2x*)."""
        return self.r * (1.0 - 2.0 * x_star)


def find_period_doubling_bifurcations(
    r_min: float = 2.8,
    r_max: float = 3.6,
    num_r: int = 10000,
    transient: int = 100,
    period_check_steps: int = 20
) -> Tuple[List[float], List[int]]:
    """
    Find period-doubling bifurcation points.

    Returns r values where period doubles (1→2→4→8→...).

    Args:
        r_min: Minimum r value
        r_max: Maximum r value
        num_r: Number of r values to scan
        transient: Steps to discard before checking period
        period_check_steps: Steps to check for period

    Returns:
        (r_bifurcations, periods): Parameter values and periods
    """
    r_values = np.linspace(r_min, r_max, num_r)
    r_bifurcations = []
    periods = []

    for r in r_values:
        logmap = LogisticMap(r)
        x = 0.5
        orbit = logmap.orbit(x, steps=period_check_steps, transient=transient)

        # Detect period by looking for repeating pattern
        for period in range(1, period_check_steps // 2):
            is_period = True
            for i in range(period_check_steps - 2 * period):
                if abs(orbit[i] - orbit[i + period]) > 1e-6:
                    is_period = False
                    break

            if is_period and period > 0:
                if len(periods) == 0 or period != periods[-1]:
                    r_bifurcations.append(r)
                    periods.append(period)
                break

    return r_bifurcations, periods


def compute_feigenbaum_delta(
    r_min: float = 2.8,
    r_max: float = 3.57,
    num_bifurcations: int = 20,
    transient: int = 100
) -> Tuple[List[float], float]:
    """
    Compute Feigenbaum delta from bifurcation sequence.

    δ = lim (r_n - r_{n-1}) / (r_{n+1} - r_n)

    Args:
        r_min: Minimum r
        r_max: Maximum r (should be near chaos threshold)
        num_bifurcations: Number of bifurcation points to find
        transient: Transient steps

    Returns:
        (delta_sequence, avg_delta): Sequence of delta values and average
    """
    r_bifurcations = []

    # Search for period-doubling bifurcations
    r_values = np.linspace(r_min, r_max, 50000)
    prev_period = 1

    for r in r_values:
        logmap = LogisticMap(r)
        x = 0.5
        orbit = logmap.orbit(x, steps=100, transient=transient)

        # Check for period
        for period in [2, 4, 8, 16, 32, 64]:
            is_period = True
            for i in range(len(orbit) - period - 1):
                if abs(orbit[i] - orbit[i + period]) > 1e-5:
                    is_period = False
                    break

            if is_period and period > prev_period:
                r_bifurcations.append(r)
                prev_period = period
                break

        if len(r_bifurcations) >= num_bifurcations:
            break

    # Compute delta sequence
    delta_sequence = []
    if len(r_bifurcations) >= 3:
        for i in range(len(r_bifurcations) - 2):
            r_n = r_bifurcations[i]
            r_n1 = r_bifurcations[i + 1]
            r_n2 = r_bifurcations[i + 2]

            if abs(r_n1 - r_n) > 1e-10:
                delta = (r_n1 - r_n) / (r_n2 - r_n1)
                delta_sequence.append(delta)

    avg_delta = np.mean(delta_sequence) if delta_sequence else 0.0
    return delta_sequence, avg_delta


def lyapunov_exponent(
    r: float,
    x0: float = 0.5,
    steps: int = 1000,
    transient: int = 100
) -> float:
    """
    Compute Lyapunov exponent λ for logistic map.

    λ = lim (1/N) Σ ln|f'(x_n)|

    Positive λ: chaotic
    Negative λ: stable
    """
    logmap = LogisticMap(r)
    x = x0

    # Transient
    for _ in range(transient):
        x = logmap.iterate(x)

    # Compute Lyapunov
    sum_ln_derivative = 0.0
    for _ in range(steps):
        x_next = logmap.iterate(x)
        deriv = r * (1.0 - 2.0 * x)

        if deriv != 0:
            sum_ln_derivative += np.log(abs(deriv))
        else:
            return 0.0

        x = x_next

    return sum_ln_derivative / steps


def bifurcation_diagram(
    r_min: float = 2.8,
    r_max: float = 4.0,
    num_r: int = 2000,
    num_iterations: int = 100,
    transient: int = 300
) -> Tuple[NDArray, NDArray]:
    """
    Compute bifurcation diagram data.

    For each r, compute orbit and return (r_values, x_values) for plotting.

    Args:
        r_min: Minimum r
        r_max: Maximum r
        num_r: Number of r values
        num_iterations: Iterations to collect (after transient)
        transient: Transient steps to discard

    Returns:
        (r_array, x_array): Arrays for plotting
    """
    r_values = np.linspace(r_min, r_max, num_r)
    r_array = []
    x_array = []

    for r in r_values:
        logmap = LogisticMap(r)
        x = 0.5
        orbit = logmap.orbit(x, steps=num_iterations, transient=transient)

        for x_val in orbit:
            r_array.append(r)
            x_array.append(x_val)

    return np.array(r_array), np.array(x_array)


def control_unstable_orbit(
    r: float,
    x0: float = 0.5,
    target_period: int = 2,
    control_gain: float = 0.1,
    steps: int = 200
) -> Tuple[List[float], bool]:
    """
    Attempt to stabilize unstable periodic orbit using feedback.

    Control law: u_n = -K(x_n - x_{n-k})  where k is target period

    Args:
        r: Parameter (chaotic regime)
        x0: Initial state
        target_period: Period to stabilize
        control_gain: Gain K
        steps: Number of steps

    Returns:
        (trajectory, stabilized): Orbit and success flag
    """
    trajectory = [x0]
    x = x0
    stabilized = False

    for n in range(steps):
        # Logistic map
        x_next_uncontrolled = r * x * (1.0 - x)

        # Control: if we have history, apply feedback
        if n >= target_period:
            x_delayed = trajectory[n - target_period]
            control = -control_gain * (x - x_delayed)
            x_next = x_next_uncontrolled + control
        else:
            x_next = x_next_uncontrolled

        # Clip to valid range
        x_next = max(0.0, min(1.0, x_next))
        trajectory.append(x_next)

        # Check if stabilized (low variance in last period)
        if n > 2 * target_period:
            recent = trajectory[-target_period:]
            variance = np.var(recent)
            if variance < 1e-5:
                stabilized = True

        x = x_next

    return trajectory, stabilized


# ============================================================================
# DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("CONSTANTE DE FEIGENBAUM δ")
    print("="*70 + "\n")

    # Compute delta
    print("Calculando bifurcaciones de periodo-doble...")
    delta_seq, avg_delta = compute_feigenbaum_delta(
        r_min=2.8, r_max=3.5698, num_bifurcations=15
    )

    print(f"\nSecuencia de δ (primeras 5): {delta_seq[:5]}")
    print(f"Delta promedio: {avg_delta:.6f}")
    print(f"Delta teórico:  {FEIGENBAUM_DELTA:.6f}")
    print(f"Error:          {abs(avg_delta - FEIGENBAUM_DELTA):.6f}")
    print()

    # Lyapunov exponents
    print("Exponentes de Lyapunov:")
    print("-" * 70)
    for r in [2.8, 3.0, 3.5, 3.57, 3.8, 4.0]:
        lya = lyapunov_exponent(r)
        status = "CAÓTICO" if lya > 0.01 else "ESTABLE"
        print(f"  r = {r:.2f}: λ = {lya:8.4f} ({status})")
    print()

    print("="*70 + "\n")
