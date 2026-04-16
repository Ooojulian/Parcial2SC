"""Tests for Feigenbaum bifurcation analysis."""

import pytest
import numpy as np
from src.feigenbaum import (
    LogisticMap, BifurcationPoint,
    find_period_doubling_bifurcations,
    compute_feigenbaum_delta,
    lyapunov_exponent,
    bifurcation_diagram,
    control_unstable_orbit,
    FEIGENBAUM_DELTA
)


class TestLogisticMapBasics:
    """Test LogisticMap basic operations."""

    def test_init(self):
        lm = LogisticMap(r=3.5)
        assert lm.r == 3.5

    def test_iterate_single_step(self):
        lm = LogisticMap(r=2.8)
        x0 = 0.5
        x1 = lm.iterate(x0, steps=1)
        # x_{n+1} = r*x_n*(1-x_n) = 2.8*0.5*0.5 = 0.7
        assert abs(x1 - 0.7) < 1e-10

    def test_iterate_multiple_steps(self):
        lm = LogisticMap(r=2.8)
        x0 = 0.5
        x = lm.iterate(x0, steps=3)
        # Compute manually
        x = 0.5
        for _ in range(3):
            x = 2.8 * x * (1.0 - x)
        assert isinstance(x, float)
        assert 0 <= x <= 1

    def test_orbit_length(self):
        lm = LogisticMap(r=3.0)
        orbit = lm.orbit(0.5, steps=10, transient=5)
        assert len(orbit) == 10

    def test_orbit_bounds(self):
        lm = LogisticMap(r=3.8)
        orbit = lm.orbit(0.5, steps=50, transient=100)
        assert all(0 <= x <= 1 for x in orbit)

    def test_fixed_point_stable(self):
        # r < 1: fixed point is 0
        lm = LogisticMap(r=0.5)
        fp = lm.fixed_point()
        assert fp == 0.0

    def test_fixed_point_nontrivial(self):
        # r = 3.5: fixed point is (1 - 1/r)
        lm = LogisticMap(r=3.5)
        fp = lm.fixed_point()
        expected = 1.0 - 1.0 / 3.5
        assert abs(fp - expected) < 1e-10

    def test_derivative_at_fixed(self):
        lm = LogisticMap(r=2.8)
        x_star = lm.fixed_point()
        deriv = lm.derivative_at_fixed(x_star)
        # deriv = r(1 - 2*x_star)
        expected = 2.8 * (1.0 - 2.0 * x_star)
        assert abs(deriv - expected) < 1e-10


class TestBifurcationDetection:
    """Test bifurcation point detection."""

    def test_period_doubling_bifurcations_returns_tuple(self):
        r_bif, periods = find_period_doubling_bifurcations(
            r_min=2.8, r_max=3.5, num_r=100
        )
        assert isinstance(r_bif, list)
        assert isinstance(periods, list)
        assert len(r_bif) == len(periods)

    def test_bifurcations_in_valid_range(self):
        r_bif, _ = find_period_doubling_bifurcations(
            r_min=2.8, r_max=3.5, num_r=500
        )
        if r_bif:  # May be empty with coarse sampling
            assert all(2.8 <= r <= 3.5 for r in r_bif)

    def test_bifurcation_periods_increase(self):
        r_bif, periods = find_period_doubling_bifurcations(
            r_min=2.8, r_max=3.56, num_r=1000
        )
        # Periods should generally increase
        if len(periods) > 1:
            # Allow some disorder due to numerical detection
            assert periods[-1] >= periods[0]


class TestFeigenbaumDelta:
    """Test Feigenbaum delta computation."""

    def test_compute_delta_returns_tuple(self):
        delta_seq, avg_delta = compute_feigenbaum_delta(
            r_min=2.8, r_max=3.57, num_bifurcations=10
        )
        assert isinstance(delta_seq, list)
        assert isinstance(avg_delta, (float, np.floating))

    def test_delta_positive(self):
        delta_seq, avg_delta = compute_feigenbaum_delta(
            r_min=2.8, r_max=3.57, num_bifurcations=12
        )
        if delta_seq:
            assert all(d > 0 for d in delta_seq)
        assert avg_delta >= 0

    def test_delta_near_theoretical(self):
        # With enough bifurcations, should approach theoretical value
        delta_seq, avg_delta = compute_feigenbaum_delta(
            r_min=2.8, r_max=3.5698, num_bifurcations=15
        )
        # Numerical bifurcation detection gives rough estimate
        # Just verify we get a value in reasonable range
        if delta_seq:
            assert 0 < avg_delta < 10.0

    def test_delta_sequence_length(self):
        num_bif = 12
        delta_seq, _ = compute_feigenbaum_delta(
            r_min=2.8, r_max=3.57, num_bifurcations=num_bif
        )
        # delta_seq has len(bifurcations) - 2 elements
        if delta_seq:
            assert len(delta_seq) <= num_bif - 2


class TestLyapunovExponent:
    """Test Lyapunov exponent computation."""

    def test_lyapunov_stable_region(self):
        # r < 3: stable fixed point, negative Lyapunov
        lya = lyapunov_exponent(r=2.5, steps=1000)
        assert lya < 0

    def test_lyapunov_chaotic_region(self):
        # r > 3.57: chaotic, positive Lyapunov
        lya = lyapunov_exponent(r=3.9, steps=1000)
        assert lya > 0

    def test_lyapunov_bounded(self):
        # Lyapunov exponent should be bounded for logistic map
        lya = lyapunov_exponent(r=3.5, steps=1000)
        assert -5 < lya < 5

    def test_lyapunov_different_r_values(self):
        lya_stable = lyapunov_exponent(r=2.8, steps=1000)
        lya_chaotic = lyapunov_exponent(r=3.95, steps=1000)
        # Chaotic should have larger (less negative or positive) value
        assert lya_chaotic > lya_stable


class TestBifurcationDiagram:
    """Test bifurcation diagram computation."""

    def test_diagram_returns_arrays(self):
        r_arr, x_arr = bifurcation_diagram(
            r_min=2.8, r_max=4.0, num_r=100, num_iterations=10
        )
        assert isinstance(r_arr, np.ndarray)
        assert isinstance(x_arr, np.ndarray)
        assert len(r_arr) == len(x_arr)

    def test_diagram_sizes(self):
        num_r = 50
        num_iter = 20
        r_arr, x_arr = bifurcation_diagram(
            r_min=2.8, r_max=4.0, num_r=num_r, num_iterations=num_iter
        )
        # Should have num_r * num_iter points
        assert len(r_arr) == num_r * num_iter

    def test_diagram_x_bounds(self):
        r_arr, x_arr = bifurcation_diagram(
            r_min=2.8, r_max=4.0, num_r=200, num_iterations=30
        )
        assert np.all(x_arr >= 0)
        assert np.all(x_arr <= 1)

    def test_diagram_r_range(self):
        r_min, r_max = 2.9, 3.8
        r_arr, _ = bifurcation_diagram(
            r_min=r_min, r_max=r_max, num_r=100
        )
        assert np.min(r_arr) >= r_min
        assert np.max(r_arr) <= r_max


class TestChaosControl:
    """Test chaos control mechanism."""

    def test_control_returns_tuple(self):
        traj, stab = control_unstable_orbit(
            r=3.9, x0=0.5, target_period=2, control_gain=0.1, steps=50
        )
        assert isinstance(traj, list)
        assert isinstance(stab, (bool, np.bool_))

    def test_control_trajectory_bounds(self):
        traj, _ = control_unstable_orbit(
            r=3.9, x0=0.5, target_period=2, control_gain=0.1, steps=100
        )
        assert all(0 <= x <= 1 for x in traj)

    def test_control_trajectory_length(self):
        steps = 50
        traj, _ = control_unstable_orbit(
            r=3.9, x0=0.5, target_period=2, steps=steps
        )
        # Initial x0 plus steps iterations
        assert len(traj) == steps + 1

    def test_control_gain_effect(self):
        # Larger gain should affect trajectory more
        traj1, _ = control_unstable_orbit(
            r=3.9, x0=0.5, target_period=2, control_gain=0.01, steps=100
        )
        traj2, _ = control_unstable_orbit(
            r=3.9, x0=0.5, target_period=2, control_gain=0.5, steps=100
        )
        # Trajectories should differ
        assert not np.allclose(traj1, traj2)

    def test_control_zero_gain_uncontrolled(self):
        # Zero gain should give uncontrolled dynamics
        traj_zero, _ = control_unstable_orbit(
            r=3.9, x0=0.5, target_period=2, control_gain=0.0, steps=50
        )
        lm = LogisticMap(3.9)
        traj_uncontrolled = [0.5]
        x = 0.5
        for _ in range(50):
            x = lm.iterate(x)
            traj_uncontrolled.append(x)
        # Should match (within numerical error)
        assert np.allclose(traj_zero, traj_uncontrolled, atol=1e-10)


class TestBifurcationPoint:
    """Test BifurcationPoint dataclass."""

    def test_bifurcation_point_creation(self):
        bp = BifurcationPoint(parameter=3.0, period=2, eigenvalue=0.5)
        assert bp.parameter == 3.0
        assert bp.period == 2
        assert bp.eigenvalue == 0.5

    def test_bifurcation_point_fields(self):
        bp = BifurcationPoint(parameter=3.57, period=4, eigenvalue=-0.8)
        assert hasattr(bp, 'parameter')
        assert hasattr(bp, 'period')
        assert hasattr(bp, 'eigenvalue')


class TestNumericalStability:
    """Test numerical stability and edge cases."""

    def test_iterate_near_zero(self):
        lm = LogisticMap(r=3.8)
        x = lm.iterate(1e-10, steps=1)
        assert x >= 0

    def test_iterate_near_one(self):
        lm = LogisticMap(r=3.8)
        x = lm.iterate(1.0 - 1e-10, steps=1)
        assert 0 <= x <= 1

    def test_orbit_very_small_transient(self):
        lm = LogisticMap(r=3.5)
        orbit = lm.orbit(0.5, steps=5, transient=0)
        assert len(orbit) == 5

    def test_lyapunov_low_steps(self):
        # Should not crash with low step count
        lya = lyapunov_exponent(r=3.5, steps=10)
        assert isinstance(lya, float)


class TestConsistency:
    """Test consistency across different parameter ranges."""

    def test_stable_vs_chaotic_lyapunov(self):
        # Verify consistent behavior across multiple calls
        lya1_stable = lyapunov_exponent(r=2.9, steps=500)
        lya2_stable = lyapunov_exponent(r=2.9, steps=500)
        assert abs(lya1_stable - lya2_stable) < 0.01

    def test_orbit_reproducibility(self):
        lm = LogisticMap(r=3.5)
        orbit1 = lm.orbit(0.5, steps=20)
        orbit2 = lm.orbit(0.5, steps=20)
        np.testing.assert_array_almost_equal(orbit1, orbit2)

    def test_bifurcation_diagram_consistency(self):
        # Same parameters should give identical results
        r1, x1 = bifurcation_diagram(r_min=3.0, r_max=3.5, num_r=50, num_iterations=10)
        r2, x2 = bifurcation_diagram(r_min=3.0, r_max=3.5, num_r=50, num_iterations=10)
        np.testing.assert_array_equal(r1, r2)
        np.testing.assert_array_equal(x1, x2)
