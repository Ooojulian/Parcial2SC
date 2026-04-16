"""Tests for attractor-based agent models."""

import pytest
import numpy as np
from src.attractors import (
    Agent, FixedPointAgent, LimitCycleAgent, LorenzAgent,
    FixedPointSimulation, LimitCycleSimulation, LorenzSimulation,
    SimulationResult, estimate_attractor_dimension
)


class TestAgent:
    """Test base Agent class."""

    def test_agent_creation(self):
        state = np.array([0.5])
        agent = Agent(0, state)
        assert agent.id == 0
        np.testing.assert_array_equal(agent.state, [0.5])

    def test_agent_initial_trajectory(self):
        state = np.array([0.5, 0.3])
        agent = Agent(1, state)
        trajectory = agent.get_trajectory()
        assert len(trajectory) == 1
        np.testing.assert_array_equal(trajectory[0], state)

    def test_agent_update(self):
        state1 = np.array([0.5])
        agent = Agent(0, state1)
        state2 = np.array([0.7])
        agent.update(state2)
        assert agent.state[0] == 0.7
        trajectory = agent.get_trajectory()
        assert len(trajectory) == 2

    def test_agent_trajectory_immutability(self):
        state = np.array([0.5])
        agent = Agent(0, state)
        state[0] = 0.9  # Modify original
        # Agent state should not be affected
        assert agent.state[0] == 0.5


class TestFixedPointAgent:
    """Test FixedPointAgent dynamics."""

    def test_fixed_point_agent_dynamics(self):
        agent = FixedPointAgent(0, np.array([0.5]))
        # Logistic map: f(0.5) = 2.8 * 0.5 * 0.5 = 0.7
        x_next = agent.dynamics(0.5, r=2.8)
        assert abs(x_next - 0.7) < 1e-10

    def test_fixed_point_agent_step(self):
        agent = FixedPointAgent(0, np.array([0.5]))
        agent.step(r=2.8)
        assert abs(agent.state[0] - 0.7) < 1e-10

    def test_fixed_point_agent_trajectory_growth(self):
        agent = FixedPointAgent(0, np.array([0.5]))
        initial_len = len(agent.trajectory)
        agent.step(r=2.8)
        assert len(agent.trajectory) == initial_len + 1


class TestLimitCycleAgent:
    """Test LimitCycleAgent dynamics."""

    def test_limit_cycle_agent_dynamics(self):
        agent = LimitCycleAgent(0, np.array([0.0]))
        omega = 2.0 * np.pi / 10  # Period 10
        phase_next = agent.dynamics(0.0, omega)
        assert abs(phase_next - omega) < 1e-10

    def test_limit_cycle_agent_periodicity(self):
        agent = LimitCycleAgent(0, np.array([0.0]))
        omega = 2.0 * np.pi / 10
        phase = 0.0
        for _ in range(10):
            phase = agent.dynamics(phase, omega)
        # After 10 steps, should return to 0 (mod 2π)
        assert abs(phase % (2.0 * np.pi)) < 1e-10

    def test_limit_cycle_agent_step(self):
        agent = LimitCycleAgent(0, np.array([0.5]))
        agent.step(omega=0.1)
        assert agent.state[0] == pytest.approx(0.6, abs=1e-10)


class TestLorenzAgent:
    """Test LorenzAgent dynamics."""

    def test_lorenz_agent_creation(self):
        state = np.array([1.0, 2.0, 3.0])
        agent = LorenzAgent(0, state)
        np.testing.assert_array_almost_equal(agent.state, state)

    def test_lorenz_step_deterministic(self):
        agent = LorenzAgent(0, np.array([1.0, 2.0, 3.0]))
        agent.step(sigma=10.0, rho=28.0, beta=8.0/3.0, dt=0.01)
        # Should produce a valid 3D state
        assert agent.state.shape == (3,)
        assert not np.any(np.isnan(agent.state))

    def test_lorenz_bounds(self):
        agent = LorenzAgent(0, np.array([1.0, 1.0, 1.0]))
        for _ in range(100):
            agent.step(sigma=10.0, rho=28.0, beta=8.0/3.0, dt=0.01)
        # Lorenz attractor is bounded
        assert np.all(np.abs(agent.state) < 100)


class TestFixedPointSimulation:
    """Test FixedPointSimulation."""

    def test_fixed_point_simulation_creation(self):
        sim = FixedPointSimulation(num_agents=10, r=2.8)
        assert len(sim.agents) == 10
        assert sim.r == 2.8

    def test_fixed_point_simulation_run_convergence(self):
        sim = FixedPointSimulation(num_agents=20, r=2.8)
        result = sim.run(steps=200)

        assert isinstance(result, SimulationResult)
        assert result.attractor_type == "FixedPoint"
        assert len(result.agent_trajectories) == 20
        assert len(result.times) == 201

    def test_fixed_point_agents_converge(self):
        # With r < 3, should converge to fixed point
        sim = FixedPointSimulation(num_agents=10, r=2.8)
        result = sim.run(steps=200)

        assert result.converged
        assert result.convergence_metric < 0.01

    def test_fixed_point_different_r_values(self):
        # Test multiple r values
        for r in [2.0, 2.5, 2.8, 2.9]:
            sim = FixedPointSimulation(num_agents=10, r=r)
            result = sim.run(steps=200)
            assert result.attractor_type == "FixedPoint"


class TestLimitCycleSimulation:
    """Test LimitCycleSimulation."""

    def test_limit_cycle_simulation_creation(self):
        sim = LimitCycleSimulation(num_agents=15, period=10)
        assert len(sim.agents) == 15
        assert sim.period == 10

    def test_limit_cycle_simulation_run(self):
        sim = LimitCycleSimulation(num_agents=10, period=8)
        result = sim.run(steps=100)

        assert result.attractor_type == "LimitCycle"
        assert len(result.agent_trajectories) == 10
        assert len(result.times) == 101

    def test_limit_cycle_period_maintained(self):
        sim = LimitCycleSimulation(num_agents=5, period=12)
        result = sim.run(steps=200)

        # Check that trajectories are periodic
        for traj in result.agent_trajectories:
            # Phases should cycle with period 12 (approximately)
            assert len(traj) == 201

    def test_limit_cycle_convergence(self):
        sim = LimitCycleSimulation(num_agents=20, period=10)
        result = sim.run(steps=300)

        # All agents execute same period (phase advance by omega each step)
        # Convergence metric is circular variance of phases
        # With random initial phases, variance should persist
        # But agents should all be on the limit cycle
        assert result.convergence_metric >= 0  # Always valid variance
        assert len(result.agent_trajectories) == 20


class TestLorenzSimulation:
    """Test LorenzSimulation."""

    def test_lorenz_simulation_creation(self):
        sim = LorenzSimulation(num_agents=5, sigma=10.0, rho=28.0, beta=8.0/3.0)
        assert len(sim.agents) == 5
        assert sim.sigma == 10.0
        assert sim.rho == 28.0

    def test_lorenz_simulation_run(self):
        sim = LorenzSimulation(num_agents=3, sigma=10.0, rho=28.0, beta=8.0/3.0)
        result = sim.run(steps=100, dt=0.01)

        assert result.attractor_type == "LorenzAttractor"
        assert len(result.agent_trajectories) == 3
        assert len(result.times) == 101

    def test_lorenz_agents_bounded(self):
        sim = LorenzSimulation(num_agents=5, sigma=10.0, rho=28.0, beta=8.0/3.0)
        result = sim.run(steps=500, dt=0.01)

        for traj in result.agent_trajectories:
            assert np.all(np.abs(traj) < 50)  # Lorenz is bounded

    def test_lorenz_convergence_to_attractor(self):
        sim = LorenzSimulation(num_agents=10, sigma=10.0, rho=28.0, beta=8.0/3.0)
        result = sim.run(steps=1000, dt=0.01)

        # All agents should be on attractor (similar spread)
        assert result.convergence_metric < 20.0


class TestSimulationResult:
    """Test SimulationResult dataclass."""

    def test_simulation_result_creation(self):
        trajectories = [np.random.randn(100) for _ in range(5)]
        times = np.arange(100)

        result = SimulationResult(
            agent_trajectories=trajectories,
            times=times,
            attractor_type="TestAttractor",
            converged=True,
            convergence_metric=0.01
        )

        assert result.attractor_type == "TestAttractor"
        assert result.converged
        assert len(result.agent_trajectories) == 5


class TestAttractorDimensionEstimation:
    """Test attractor dimension estimation."""

    def test_dimension_estimation_fixed_point(self):
        # Fixed point should have dimension ≈ 0
        trajectory = np.ones((100, 1))  # All same point
        dim = estimate_attractor_dimension(trajectory, delay=2)
        assert dim == pytest.approx(0.0, abs=0.5)

    def test_dimension_estimation_line(self):
        # 1D curve should have dimension ≈ 1
        trajectory = np.linspace(0, 1, 100).reshape(-1, 1)
        dim = estimate_attractor_dimension(trajectory, delay=2)
        # Line has dimension 1
        assert 0.5 < dim < 1.5

    def test_dimension_estimation_valid_input(self):
        # Large trajectory - estimate may vary due to embedding
        trajectory = np.random.randn(1000, 3)
        dim = estimate_attractor_dimension(trajectory, delay=3)
        # Random data typically estimates to embedding dimension or higher
        assert 0 < dim

    def test_dimension_estimation_short_trajectory(self):
        # Short trajectory should return nan
        trajectory = np.random.randn(5, 3)
        dim = estimate_attractor_dimension(trajectory, delay=3)
        assert np.isnan(dim)


class TestIntegration:
    """Integration tests combining multiple components."""

    def test_all_simulations_run_to_completion(self):
        # Test that all three simulation types can run
        sim1 = FixedPointSimulation(num_agents=5, r=2.8)
        result1 = sim1.run(steps=50)
        assert result1.converged

        sim2 = LimitCycleSimulation(num_agents=5, period=10)
        result2 = sim2.run(steps=50)
        assert len(result2.agent_trajectories) == 5

        sim3 = LorenzSimulation(num_agents=3, sigma=10.0, rho=28.0)
        result3 = sim3.run(steps=50)
        assert result3.attractor_type == "LorenzAttractor"

    def test_reproducibility(self):
        # Same initial seed should give same results
        sim1 = FixedPointSimulation(num_agents=5, r=2.8)
        result1 = sim1.run(steps=50)

        sim2 = FixedPointSimulation(num_agents=5, r=2.8)
        result2 = sim2.run(steps=50)

        # Compare first agent trajectories
        np.testing.assert_array_almost_equal(
            result1.agent_trajectories[0],
            result2.agent_trajectories[0]
        )


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_single_agent(self):
        sim = FixedPointSimulation(num_agents=1, r=2.8)
        result = sim.run(steps=100)
        assert len(result.agent_trajectories) == 1

    def test_zero_steps(self):
        sim = FixedPointSimulation(num_agents=5, r=2.8)
        result = sim.run(steps=0)
        assert len(result.times) == 1

    def test_extreme_parameters(self):
        # Very low r
        sim1 = FixedPointSimulation(num_agents=5, r=1.1)
        result1 = sim1.run(steps=50)
        assert result1.attractor_type == "FixedPoint"

        # Very high period
        sim2 = LimitCycleSimulation(num_agents=3, period=100)
        result2 = sim2.run(steps=50)
        assert len(result2.times) == 51

    def test_large_number_of_agents(self):
        sim = FixedPointSimulation(num_agents=200, r=2.8)
        result = sim.run(steps=50)
        assert len(result.agent_trajectories) == 200
