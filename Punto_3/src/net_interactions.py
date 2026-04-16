"""
Net Interactions Model - Functional Programming Implementation.

Implements interaction dynamics using pure functional composition.
"""

from typing import Callable, List, Tuple
from functools import reduce
from dataclasses import dataclass
import numpy as np
from numpy.typing import NDArray

# Type aliases
Vector = List[float]
Matrix = List[List[float]]
ActivationFn = Callable[[float], float]
NetworkState = NDArray[np.float64]


# ============================================================================
# ACTIVATION FUNCTIONS
# ============================================================================

def identity(x: float) -> float:
    """f(x) = x"""
    return x


def relu(x: float) -> float:
    """f(x) = max(0, x)"""
    return max(0.0, x)


def sigmoid(x: float) -> float:
    """f(x) = 1 / (1 + e^(-x))"""
    return 1.0 / (1.0 + np.exp(-x))


def tanh_fn(x: float) -> float:
    """f(x) = tanh(x)"""
    return np.tanh(x)


# ============================================================================
# FUNCTIONAL COMPOSITION (Pure Functional Paradigm)
# ============================================================================

def compose(*functions):
    """
    Functional composition: (f ∘ g ∘ h)(x) = f(g(h(x)))

    Right-to-left evaluation (mathematical convention).

    Example:
        add5 = lambda x: x + 5
        mult2 = lambda x: x * 2
        f = compose(add5, mult2)
        f(3) = add5(mult2(3)) = add5(6) = 11
    """
    return reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)


# ============================================================================
# FUNCTIONAL OPERATIONS (Pure)
# ============================================================================

def activate(f: ActivationFn, state: NetworkState) -> NetworkState:
    """
    Apply activation function to each element of state.

    Pure function: no side effects.

    Args:
        f: Activation function
        state: Input state vector

    Returns:
        Activated state: [f(x_1), f(x_2), ..., f(x_N)]
    """
    return np.array([f(x) for x in state])


def weight(W: NetworkState, activated: NetworkState) -> NetworkState:
    """
    Apply weight matrix to activated state.

    φ_i = Σ_j W[i,j] * a_j

    Pure function: no side effects.

    Args:
        W: Weight matrix (N x N)
        activated: Activated state vector

    Returns:
        Weighted interactions: φ = W @ a
    """
    return W @ activated


def aggregate(weighted: NetworkState) -> float:
    """
    Aggregate weighted interactions (sum all).

    Pure function: no side effects.

    Args:
        weighted: Weighted interaction vector

    Returns:
        Scalar sum of all interactions
    """
    return float(np.sum(weighted))


def net_interaction_vector(
    W: NetworkState,
    f: ActivationFn,
    state: NetworkState
) -> NetworkState:
    """
    Compute net interaction as vector: φ(x) = W @ F(x)

    Composition: weight ∘ activate

    Args:
        W: Weight matrix
        f: Activation function
        state: Current state

    Returns:
        Net interaction vector φ = W @ F(x)
    """
    return weight(W, activate(f, state))


def net_interaction_scalar(
    W: NetworkState,
    f: ActivationFn,
    state: NetworkState
) -> float:
    """
    Compute net interaction as scalar: φ(x) = Σ(W @ F(x))

    Full composition: aggregate ∘ weight ∘ activate

    Pure functional paradigm:
      aggregate(weight(activate(f, state)))

    Args:
        W: Weight matrix
        f: Activation function
        state: Current state

    Returns:
        Scalar sum of all interactions
    """
    return aggregate(weight(W, activate(f, state)))


def net_interaction(
    W: NetworkState,
    f: ActivationFn,
    state: NetworkState
) -> NetworkState:
    """
    Compute net interaction: vector form φ(x) = W @ F(x)

    Default behavior returns vector. Use net_interaction_scalar()
    for full composition with aggregate.

    Args:
        W: Weight matrix
        f: Activation function
        state: Current state

    Returns:
        Net interaction vector
    """
    return net_interaction_vector(W, f, state)


# ============================================================================
# DYNAMICS AND CONVERGENCE
# ============================================================================

def iterate_network(
    W: NetworkState,
    f: ActivationFn,
    x0: NetworkState,
    steps: int = 100,
    noise_std: float = 0.0
) -> Tuple[List[NetworkState], bool]:
    """
    Iterate network dynamics: x(t+1) = W @ F(x(t)) + η(t).

    Args:
        W: Weight matrix
        f: Activation function
        x0: Initial state
        steps: Number of iterations
        noise_std: Standard deviation of Gaussian noise

    Returns:
        (trajectory, converged): List of states and convergence flag
    """
    trajectory = [x0.copy()]
    x = x0.copy()

    for _ in range(steps):
        # Compute next state: x(t+1) = net_interaction(x(t)) + noise
        x_next = net_interaction(W, f, x)

        if noise_std > 0:
            noise = np.random.normal(0, noise_std, len(x))
            x_next = x_next + noise

        trajectory.append(x_next)

        # Check convergence
        diff = np.max(np.abs(x_next - x))
        if diff < 1e-6:
            return trajectory, True

        x = x_next

    return trajectory, False


def find_fixed_point(
    W: NetworkState,
    f: ActivationFn,
    x0: NetworkState,
    max_iter: int = 1000,
    tol: float = 1e-8
) -> Tuple[NetworkState, bool]:
    """
    Find fixed point x* where F(x*) = x* using fixed-point iteration.

    x(t+1) = W @ F(x(t))

    Args:
        W: Weight matrix
        f: Activation function
        x0: Initial guess
        max_iter: Maximum iterations
        tol: Convergence tolerance

    Returns:
        (fixed_point, converged): Found fixed point and convergence flag
    """
    x = x0.copy()

    for iteration in range(max_iter):
        x_next = net_interaction(W, f, x)

        # Check convergence
        diff = np.max(np.abs(x_next - x))
        if diff < tol:
            return x_next, True

        x = x_next

    return x, False


# ============================================================================
# STABILITY ANALYSIS
# ============================================================================

def compute_jacobian(
    W: NetworkState,
    f: ActivationFn,
    x_star: NetworkState,
    eps: float = 1e-6
) -> NetworkState:
    """
    Compute Jacobian matrix at fixed point using numerical differentiation.

    J[i,j] = ∂F_i/∂x_j|_{x*}

    Args:
        W: Weight matrix
        f: Activation function
        x_star: Fixed point
        eps: Small perturbation for finite differences

    Returns:
        Jacobian matrix (N x N)
    """
    N = len(x_star)
    J = np.zeros((N, N))

    # Compute F(x)
    F_x = net_interaction(W, f, x_star)

    # Finite differences for each column
    for j in range(N):
        x_perturb = x_star.copy()
        x_perturb[j] += eps

        F_x_perturb = net_interaction(W, f, x_perturb)

        J[:, j] = (F_x_perturb - F_x) / eps

    return J


def stability_analysis(
    W: NetworkState,
    f: ActivationFn,
    x_star: NetworkState
) -> Tuple[float, bool]:
    """
    Analyze stability of fixed point.

    Computes largest eigenvalue of Jacobian.
    - λ_max < 1: stable (attracting)
    - λ_max > 1: unstable (repelling)
    - λ_max = 1: bifurcation

    Args:
        W: Weight matrix
        f: Activation function
        x_star: Fixed point

    Returns:
        (lambda_max, is_stable): Largest eigenvalue and stability flag
    """
    J = compute_jacobian(W, f, x_star)
    eigenvalues = np.linalg.eigvals(J)
    lambda_max = np.max(np.abs(eigenvalues))

    is_stable = lambda_max < 1.0

    return lambda_max, is_stable


# ============================================================================
# ANALYSIS AND VISUALIZATION
# ============================================================================

@dataclass
class NetworkAnalysis:
    """Results of net interactions analysis."""

    fixed_point: NetworkState
    converged: bool
    lambda_max: float
    is_stable: bool
    trajectory_length: int
    final_state: NetworkState


def analyze_network(
    W: NetworkState,
    f: ActivationFn,
    x0: NetworkState,
    name: str = "Network"
) -> NetworkAnalysis:
    """
    Complete analysis of network dynamics.

    Args:
        W: Weight matrix
        f: Activation function
        x0: Initial state
        name: Network name for reporting

    Returns:
        NetworkAnalysis with all results
    """
    # Find fixed point
    x_star, converged = find_fixed_point(W, f, x0)

    # Get trajectory
    trajectory, _ = iterate_network(W, f, x0, steps=100)

    # Stability analysis
    lambda_max, is_stable = stability_analysis(W, f, x_star)

    return NetworkAnalysis(
        fixed_point=x_star,
        converged=converged,
        lambda_max=lambda_max,
        is_stable=is_stable,
        trajectory_length=len(trajectory),
        final_state=trajectory[-1] if trajectory else x0
    )


# ============================================================================
# DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("NET INTERACTIONS - FUNCTIONAL PROGRAMMING")
    print("="*70 + "\n")

    # Create simple 3-node network
    N = 3
    W = np.array([
        [0.0, 0.5, -0.3],
        [0.4, 0.0, 0.6],
        [-0.2, 0.5, 0.0]
    ])

    print("Weight Matrix W:")
    print(W)
    print()

    # Test with identity activation
    print("Test 1: Identity Activation")
    print("-" * 70)
    x0 = np.array([1.0, -0.5, 0.8])
    print(f"Initial state: {x0}")

    result = analyze_network(W, identity, x0)
    print(f"Fixed point: {result.fixed_point}")
    print(f"Converged: {result.converged}")
    print(f"λ_max: {result.lambda_max:.4f}")
    print(f"Stable: {result.is_stable}")
    print()

    # Test with sigmoid activation
    print("Test 2: Sigmoid Activation")
    print("-" * 70)
    x0_sig = np.array([0.0, 0.0, 0.0])
    result_sig = analyze_network(W, sigmoid, x0_sig)
    print(f"Initial state: {x0_sig}")
    print(f"Fixed point: {result_sig.fixed_point}")
    print(f"λ_max: {result_sig.lambda_max:.4f}")
    print(f"Stable: {result_sig.is_stable}")
    print()

    # Test with tanh activation
    print("Test 3: Tanh Activation")
    print("-" * 70)
    x0_tanh = np.array([0.5, -0.5, 0.3])
    result_tanh = analyze_network(W, tanh_fn, x0_tanh)
    print(f"Initial state: {x0_tanh}")
    print(f"Fixed point: {result_tanh.fixed_point}")
    print(f"λ_max: {result_tanh.lambda_max:.4f}")
    print(f"Stable: {result_tanh.is_stable}")
    print()

    print("="*70 + "\n")
