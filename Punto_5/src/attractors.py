"""Agent-based models for different attractors."""

from typing import List, Tuple, NamedTuple
from dataclasses import dataclass, field
import numpy as np
from numpy.typing import NDArray


@dataclass
class SimulationResult:
    """Result of attractor simulation."""
    agent_trajectories: List[NDArray]  # List of (T, d) arrays per agent
    times: NDArray  # Array of time steps
    attractor_type: str
    converged: bool
    convergence_metric: float  # Distance to attractor at end


class Agent:
    """Base agent class."""

    def __init__(self, agent_id: int, initial_state: NDArray):
        """Initialize agent."""
        self.id = agent_id
        self.state = initial_state.copy()
        self.trajectory = [initial_state.copy()]

    def update(self, new_state: NDArray):
        """Update agent state and record in trajectory."""
        self.state = new_state.copy()
        self.trajectory.append(new_state.copy())

    def get_trajectory(self) -> NDArray:
        """Get complete trajectory as array."""
        return np.array(self.trajectory)


class FixedPointAgent(Agent):
    """Agent converging to fixed point via logistic map."""

    def dynamics(self, x: float, r: float) -> float:
        """Logistic map: x_{n+1} = r*x_n(1-x_n)."""
        return r * x * (1.0 - x)

    def step(self, r: float):
        """Execute one time step."""
        new_x = self.dynamics(self.state[0], r)
        self.update(np.array([new_x]))


class FixedPointSimulation:
    """Simulate agents converging to fixed point."""

    def __init__(self, num_agents: int = 50, r: float = 2.8):
        """Initialize simulation.

        Args:
            num_agents: Number of agents
            r: Logistic map parameter (r < 3 for stable fixed point)
        """
        self.num_agents = num_agents
        self.r = r
        self.agents = []

        # Initialize agents with random initial conditions
        np.random.seed(42)  # Reproducibility
        for i in range(num_agents):
            x0 = np.array([np.random.uniform(0.1, 0.9)])
            self.agents.append(FixedPointAgent(i, x0))

    def run(self, steps: int = 200) -> SimulationResult:
        """Run simulation.

        Args:
            steps: Number of iterations

        Returns:
            SimulationResult with trajectories and convergence info
        """
        times = np.arange(steps + 1)

        for _ in range(steps):
            for agent in self.agents:
                agent.step(self.r)

        # Compute fixed point (theoretical)
        x_star = 1.0 - 1.0 / self.r if self.r > 1 else 0.0

        # Convergence metric: max distance to fixed point at end
        final_states = np.array([agent.state[0] for agent in self.agents])
        convergence = np.max(np.abs(final_states - x_star))
        converged = convergence < 0.01

        trajectories = [agent.get_trajectory() for agent in self.agents]

        return SimulationResult(
            agent_trajectories=trajectories,
            times=times,
            attractor_type="FixedPoint",
            converged=converged,
            convergence_metric=convergence
        )


class LimitCycleAgent(Agent):
    """Agent on periodic limit cycle."""

    def dynamics(self, phase: float, omega: float) -> float:
        """Phase evolution: φ_{n+1} = φ_n + ω (mod 2π)."""
        return (phase + omega) % (2.0 * np.pi)

    def step(self, omega: float):
        """Execute one time step."""
        new_phase = self.dynamics(self.state[0], omega)
        self.update(np.array([new_phase]))


class LimitCycleSimulation:
    """Simulate agents in periodic limit cycle."""

    def __init__(self, num_agents: int = 50, period: int = 10):
        """Initialize simulation.

        Args:
            num_agents: Number of agents
            period: Period of oscillation
        """
        self.num_agents = num_agents
        self.period = period
        self.omega = 2.0 * np.pi / period  # Angular frequency
        self.agents = []

        # Initialize agents with random phases
        np.random.seed(42)
        for i in range(num_agents):
            phase0 = np.array([np.random.uniform(0, 2.0 * np.pi)])
            self.agents.append(LimitCycleAgent(i, phase0))

    def run(self, steps: int = 200) -> SimulationResult:
        """Run simulation.

        Args:
            steps: Number of iterations

        Returns:
            SimulationResult with trajectories
        """
        times = np.arange(steps + 1)

        for _ in range(steps):
            for agent in self.agents:
                agent.step(self.omega)

        # Convergence: all agents should have same phase (mod period)
        # Metric: variance of phases
        final_phases = np.array([agent.state[0] for agent in self.agents])

        # Normalize to [0, 2π)
        final_phases = final_phases % (2.0 * np.pi)

        # For periodic data, compute circular variance
        sin_mean = np.mean(np.sin(final_phases))
        cos_mean = np.mean(np.cos(final_phases))
        circular_var = 1.0 - np.sqrt(sin_mean**2 + cos_mean**2)

        converged = circular_var < 0.01

        trajectories = [agent.get_trajectory() for agent in self.agents]

        return SimulationResult(
            agent_trajectories=trajectories,
            times=times,
            attractor_type="LimitCycle",
            converged=converged,
            convergence_metric=circular_var
        )


class LorenzAgent(Agent):
    """Agent following Lorenz system dynamics."""

    def lorenz_step(
        self,
        state: NDArray,
        sigma: float = 10.0,
        rho: float = 28.0,
        beta: float = 8.0/3.0,
        dt: float = 0.01
    ) -> NDArray:
        """RK4 integration of Lorenz system.

        dx/dt = σ(y - x)
        dy/dt = x(ρ - z) - y
        dz/dt = xy - βz
        """
        x, y, z = state

        def lorenz(s):
            sx, sy, sz = s
            dx = sigma * (sy - sx)
            dy = sx * (rho - sz) - sy
            dz = sx * sy - beta * sz
            return np.array([dx, dy, dz])

        # RK4 step
        k1 = lorenz(state)
        k2 = lorenz(state + dt/2 * k1)
        k3 = lorenz(state + dt/2 * k2)
        k4 = lorenz(state + dt * k3)

        return state + (dt/6.0) * (k1 + 2*k2 + 2*k3 + k4)

    def step(self, sigma: float = 10.0, rho: float = 28.0,
             beta: float = 8.0/3.0, dt: float = 0.01):
        """Execute one time step of Lorenz dynamics."""
        new_state = self.lorenz_step(self.state, sigma, rho, beta, dt)
        self.update(new_state)


class LorenzSimulation:
    """Simulate agents in Lorenz attractor."""

    def __init__(
        self,
        num_agents: int = 20,
        sigma: float = 10.0,
        rho: float = 28.0,
        beta: float = 8.0/3.0
    ):
        """Initialize Lorenz simulation.

        Args:
            num_agents: Number of agents
            sigma, rho, beta: Lorenz system parameters
        """
        self.num_agents = num_agents
        self.sigma = sigma
        self.rho = rho
        self.beta = beta
        self.agents = []

        # Initialize agents with random points near origin
        np.random.seed(42)
        for i in range(num_agents):
            # Start near origin with small perturbations
            state = np.array([
                np.random.uniform(-1, 1),
                np.random.uniform(-1, 1),
                np.random.uniform(-1, 1)
            ])
            self.agents.append(LorenzAgent(i, state))

    def run(self, steps: int = 2000, dt: float = 0.01) -> SimulationResult:
        """Run simulation.

        Args:
            steps: Number of iterations
            dt: Time step for integration

        Returns:
            SimulationResult with trajectories
        """
        times = np.arange(steps + 1) * dt

        for _ in range(steps):
            for agent in self.agents:
                agent.step(self.sigma, self.rho, self.beta, dt)

        # Convergence metric: spread of agents on attractor
        final_states = np.array([agent.state for agent in self.agents])

        # Distance between agents
        mean_state = np.mean(final_states, axis=0)
        spread = np.mean(np.linalg.norm(final_states - mean_state, axis=1))

        # Lorenz attractor is "converged" if all agents explore same region
        converged = spread < 10.0

        trajectories = [agent.get_trajectory() for agent in self.agents]

        return SimulationResult(
            agent_trajectories=trajectories,
            times=times,
            attractor_type="LorenzAttractor",
            converged=converged,
            convergence_metric=spread
        )


def estimate_attractor_dimension(trajectory: NDArray, delay: int = 3) -> float:
    """Estimate attractor dimension using correlation dimension.

    Args:
        trajectory: (T, d) array of points on attractor
        delay: Embedding dimension

    Returns:
        Estimated correlation dimension
    """
    if len(trajectory) < delay * 10:
        return float('nan')

    # Create delay embedding
    T = len(trajectory)
    embedded = np.zeros((T - delay, delay * trajectory.shape[1]))

    for i in range(T - delay):
        for j in range(delay):
            embedded[i, j*trajectory.shape[1]:(j+1)*trajectory.shape[1]] = trajectory[i + j]

    # Compute distances
    distances = np.zeros(len(embedded) * (len(embedded) - 1) // 2)
    idx = 0
    for i in range(len(embedded)):
        for j in range(i + 1, len(embedded)):
            distances[idx] = np.linalg.norm(embedded[i] - embedded[j])
            idx += 1

    # Count pairs within radius r
    radii = np.logspace(-2, 1, 20)
    counts = np.array([np.sum(distances <= r) for r in radii])

    # Fit log-log to estimate dimension
    valid = counts > 0
    if np.sum(valid) < 2:
        return float('nan')

    log_r = np.log(radii[valid])
    log_c = np.log(counts[valid])

    # Linear regression
    A = np.vstack([log_r, np.ones(len(log_r))]).T
    dim, _ = np.linalg.lstsq(A, log_c, rcond=None)[0]

    return dim
