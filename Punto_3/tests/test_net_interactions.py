"""Tests for net interactions model."""

import pytest
import numpy as np
from src.net_interactions import (
    activate, weight, aggregate, net_interaction,
    iterate_network, find_fixed_point, compute_jacobian,
    stability_analysis, analyze_network,
    identity, relu, sigmoid, tanh_fn
)


class TestActivationFunctions:
    """Test activation functions."""

    def test_identity(self):
        assert identity(0) == 0
        assert identity(5) == 5
        assert identity(-3) == -3

    def test_relu(self):
        assert relu(0) == 0
        assert relu(5) == 5
        assert relu(-3) == 0

    def test_sigmoid(self):
        assert 0 < sigmoid(0) < 1
        assert sigmoid(0) == pytest.approx(0.5)
        assert sigmoid(100) > 0.99

    def test_tanh_fn(self):
        assert tanh_fn(0) == 0
        assert -1 < tanh_fn(1) < 1


class TestFunctionalOperations:
    """Test pure functional operations."""

    def test_activate_identity(self):
        state = np.array([1.0, 2.0, 3.0])
        activated = activate(identity, state)
        np.testing.assert_array_almost_equal(activated, state)

    def test_activate_sigmoid(self):
        state = np.array([0.0, 1.0, -1.0])
        activated = activate(sigmoid, state)
        assert len(activated) == 3
        assert all(0 < a < 1 for a in activated)

    def test_weight_basic(self):
        W = np.array([
            [1.0, 0.0],
            [0.0, 1.0]
        ])
        a = np.array([2.0, 3.0])
        result = weight(W, a)
        np.testing.assert_array_almost_equal(result, [2.0, 3.0])

    def test_weight_scaling(self):
        W = np.array([
            [2.0, 0.0],
            [0.0, 3.0]
        ])
        a = np.array([1.0, 1.0])
        result = weight(W, a)
        np.testing.assert_array_almost_equal(result, [2.0, 3.0])

    def test_aggregate(self):
        v = np.array([1.0, 2.0, 3.0])
        assert aggregate(v) == 6.0

    def test_net_interaction(self):
        W = np.eye(3)
        state = np.array([1.0, 2.0, 3.0])
        phi = net_interaction(W, identity, state)
        np.testing.assert_array_almost_equal(phi, state)


class TestDynamics:
    """Test network dynamics."""

    def test_iterate_network_stable(self):
        # Identity weight matrix should converge instantly
        W = np.eye(3)
        x0 = np.array([1.0, 0.5, -0.5])
        trajectory, converged = iterate_network(W, identity, x0, steps=10)

        assert converged
        assert len(trajectory) > 0

    def test_iterate_network_steps(self):
        W = 0.1 * np.ones((2, 2))
        x0 = np.array([1.0, 1.0])
        trajectory, _ = iterate_network(W, identity, x0, steps=5)

        # Should have 6 states (initial + 5 steps)
        assert len(trajectory) == 6

    def test_find_fixed_point_identity(self):
        # For x(t+1) = x(t), any point is fixed
        W = np.eye(3)
        x0 = np.array([1.0, 2.0, 3.0])
        x_star, converged = find_fixed_point(W, identity, x0)

        assert converged
        np.testing.assert_array_almost_equal(x_star, x0, decimal=5)

    def test_find_fixed_point_converges(self):
        # Contractive system should converge
        W = 0.5 * np.ones((3, 3)) / 3
        x0 = np.array([1.0, -1.0, 0.5])
        x_star, converged = find_fixed_point(W, identity, x0)

        assert converged


class TestStabilityAnalysis:
    """Test stability analysis."""

    def test_compute_jacobian_shape(self):
        W = np.random.randn(3, 3)
        x_star = np.zeros(3)
        J = compute_jacobian(W, identity, x_star)

        assert J.shape == (3, 3)

    def test_stability_analysis_stable_identity(self):
        W = 0.5 * np.eye(3)
        x_star = np.array([0.0, 0.0, 0.0])
        lambda_max, is_stable = stability_analysis(W, identity, x_star)

        assert lambda_max < 1.0
        assert is_stable

    def test_stability_analysis_unstable(self):
        W = 2.0 * np.eye(3)
        x_star = np.array([0.0, 0.0, 0.0])
        lambda_max, is_stable = stability_analysis(W, identity, x_star)

        assert lambda_max > 1.0
        assert not is_stable


class TestNetworkAnalysis:
    """Test complete network analysis."""

    def test_analyze_network_convergence(self):
        W = 0.5 * np.eye(3)
        x0 = np.array([1.0, 0.5, -0.5])
        result = analyze_network(W, identity, x0)

        assert result.converged
        assert result.lambda_max < 1.0
        assert result.is_stable

    def test_analyze_network_multiple_activations(self):
        W = np.random.randn(2, 2) * 0.3
        x0 = np.array([0.0, 0.0])

        for f in [identity, sigmoid, tanh_fn]:
            result = analyze_network(W, f, x0)
            assert hasattr(result, 'fixed_point')
            assert hasattr(result, 'lambda_max')
            assert hasattr(result, 'is_stable')

    def test_analyze_network_returns_analysis(self):
        W = np.eye(2)
        x0 = np.array([1.0, -1.0])
        result = analyze_network(W, identity, x0)

        assert isinstance(result.fixed_point, np.ndarray)
        assert isinstance(result.converged, (bool, np.bool_))
        assert isinstance(result.lambda_max, (float, np.floating))
        assert isinstance(result.is_stable, (bool, np.bool_))
        assert isinstance(result.trajectory_length, int)


class TestFunctionalPurity:
    """Test that operations are functionally pure."""

    def test_activate_is_pure(self):
        """Same input should produce same output."""
        state = np.array([1.0, 2.0, 3.0])
        result1 = activate(sigmoid, state.copy())
        result2 = activate(sigmoid, state.copy())
        np.testing.assert_array_equal(result1, result2)

    def test_weight_is_pure(self):
        """Same input should produce same output."""
        W = np.array([[1.0, 2.0], [3.0, 4.0]])
        a = np.array([1.0, 1.0])
        result1 = weight(W.copy(), a.copy())
        result2 = weight(W.copy(), a.copy())
        np.testing.assert_array_equal(result1, result2)

    def test_no_side_effects(self):
        """Operations shouldn't modify inputs."""
        W = np.array([[1.0, 2.0], [3.0, 4.0]])
        a = np.array([1.0, 1.0])
        W_original = W.copy()
        a_original = a.copy()

        _ = weight(W, a)

        np.testing.assert_array_equal(W, W_original)
        np.testing.assert_array_equal(a, a_original)


class TestEdgeCases:
    """Test edge cases."""

    def test_single_node(self):
        W = np.array([[0.5]])
        x0 = np.array([1.0])
        result = analyze_network(W, identity, x0)
        assert len(result.fixed_point) == 1

    def test_zero_initial_state(self):
        W = np.eye(3)
        x0 = np.zeros(3)
        trajectory, _ = iterate_network(W, identity, x0)
        assert trajectory[0].sum() == 0

    def test_large_network(self):
        W = np.random.randn(10, 10) * 0.1
        x0 = np.random.randn(10)
        result = analyze_network(W, sigmoid, x0)
        assert len(result.fixed_point) == 10
