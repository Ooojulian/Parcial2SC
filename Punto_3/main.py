#!/usr/bin/env python3
"""Main execution for Punto 3: Net Interactions."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.net_interactions import (
    analyze_network, iterate_network, identity, sigmoid, tanh_fn
)
import numpy as np
import matplotlib.pyplot as plt

def plot_convergence_comparison(W, x0_1, x0_2, x0_3):
    """
    Plot convergence trajectories for all three activation functions.
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    # Test 1: Identity
    traj_1, _ = iterate_network(W, identity, x0_1, steps=50)
    traj_1_array = np.array(traj_1)

    axes[0].plot(traj_1_array[:, 0], label='x₁(t)', linewidth=2)
    axes[0].plot(traj_1_array[:, 1], label='x₂(t)', linewidth=2)
    axes[0].plot(traj_1_array[:, 2], label='x₃(t)', linewidth=2)
    axes[0].axhline(y=0, color='k', linestyle='--', alpha=0.3)
    axes[0].set_xlabel('Time step', fontsize=11)
    axes[0].set_ylabel('State value', fontsize=11)
    axes[0].set_title('Identity Activation', fontsize=12, fontweight='bold')
    axes[0].legend(fontsize=10)
    axes[0].grid(True, alpha=0.3)

    # Test 2: Sigmoid
    traj_2, _ = iterate_network(W, sigmoid, x0_2, steps=50)
    traj_2_array = np.array(traj_2)

    axes[1].plot(traj_2_array[:, 0], label='x₁(t)', linewidth=2)
    axes[1].plot(traj_2_array[:, 1], label='x₂(t)', linewidth=2)
    axes[1].plot(traj_2_array[:, 2], label='x₃(t)', linewidth=2)
    axes[1].set_xlabel('Time step', fontsize=11)
    axes[1].set_ylabel('State value', fontsize=11)
    axes[1].set_title('Sigmoid Activation', fontsize=12, fontweight='bold')
    axes[1].legend(fontsize=10)
    axes[1].grid(True, alpha=0.3)

    # Test 3: Tanh
    traj_3, _ = iterate_network(W, tanh_fn, x0_3, steps=50)
    traj_3_array = np.array(traj_3)

    axes[2].plot(traj_3_array[:, 0], label='x₁(t)', linewidth=2)
    axes[2].plot(traj_3_array[:, 1], label='x₂(t)', linewidth=2)
    axes[2].plot(traj_3_array[:, 2], label='x₃(t)', linewidth=2)
    axes[2].axhline(y=0, color='k', linestyle='--', alpha=0.3)
    axes[2].set_xlabel('Time step', fontsize=11)
    axes[2].set_ylabel('State value', fontsize=11)
    axes[2].set_title('Tanh Activation', fontsize=12, fontweight='bold')
    axes[2].legend(fontsize=10)
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('results/convergence_comparison.png', dpi=150, bbox_inches='tight')
    print("   ✓ Saved: results/convergence_comparison.png")
    plt.close()


def plot_phase_plane(W, x0, activation_fn, func_name, steps=100):
    """
    Plot phase plane trajectory (2D projection: x1 vs x2).
    """
    traj, _ = iterate_network(W, activation_fn, x0, steps=steps)
    traj_array = np.array(traj)

    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot trajectory
    ax.plot(traj_array[:, 0], traj_array[:, 1], 'b-', linewidth=2, alpha=0.7, label='Trajectory')

    # Mark initial and final points
    ax.plot(traj_array[0, 0], traj_array[0, 1], 'go', markersize=10, label='Start', zorder=5)
    ax.plot(traj_array[-1, 0], traj_array[-1, 1], 'r*', markersize=15, label='End (Fixed Point)', zorder=5)

    # Add arrows to show direction
    for i in range(0, len(traj_array)-1, max(1, len(traj_array)//10)):
        dx = traj_array[i+1, 0] - traj_array[i, 0]
        dy = traj_array[i+1, 1] - traj_array[i, 1]
        ax.arrow(traj_array[i, 0], traj_array[i, 1], dx, dy,
                head_width=0.05, head_length=0.04, fc='blue', ec='blue', alpha=0.5)

    ax.set_xlabel('x₁(t)', fontsize=12)
    ax.set_ylabel('x₂(t)', fontsize=12)
    ax.set_title(f'Phase Plane Trajectory - {func_name} Activation', fontsize=13, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'results/phase_plane_{func_name.lower()}.png', dpi=150, bbox_inches='tight')
    print(f"   ✓ Saved: results/phase_plane_{func_name.lower()}.png")
    plt.close()


def plot_eigenvalue_stability(lambda_max_1, lambda_max_2, lambda_max_3):
    """
    Plot eigenvalue magnitudes for stability analysis.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    activations = ['Identity', 'Sigmoid', 'Tanh']
    lambda_maxes = [lambda_max_1, lambda_max_2, lambda_max_3]
    colors = ['red' if lm > 1 else 'green' for lm in lambda_maxes]

    bars = ax.bar(activations, lambda_maxes, color=colors, alpha=0.7, edgecolor='black', linewidth=2)

    # Add stability threshold line
    ax.axhline(y=1.0, color='black', linestyle='--', linewidth=2, label='Stability Boundary (λ_max = 1)')

    # Add value labels on bars
    for bar, lm in zip(bars, lambda_maxes):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{lm:.4f}',
                ha='center', va='bottom', fontsize=11, fontweight='bold')

    ax.set_ylabel('Maximum Eigenvalue (λ_max)', fontsize=12)
    ax.set_title('Stability Analysis: Eigenvalue Spectrum', fontsize=13, fontweight='bold')
    ax.set_ylim(0, 1.2)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('results/eigenvalue_stability.png', dpi=150, bbox_inches='tight')
    print("   ✓ Saved: results/eigenvalue_stability.png")
    plt.close()


if __name__ == "__main__":
    # Create results directory
    Path("results").mkdir(exist_ok=True)

    print("\n" + "="*70)
    print("PUNTO 3: INTERACCIÓN EN SISTEMAS COMPLEJOS")
    print("Modelo de Net Interactions - Programación Funcional")
    print("="*70 + "\n")

    # Network setup
    W = np.array([
        [0.0, 0.5, -0.3],
        [0.4, 0.0, 0.6],
        [-0.2, 0.5, 0.0]
    ])

    print("RED: 3 nodos con matriz de pesos W")
    print("="*70)
    print(W)
    print()

    # Test 1: Identity
    print("\n[TEST 1] Activación Identidad")
    print("-"*70)
    x0_1 = np.array([1.0, -0.5, 0.8])
    result_1 = analyze_network(W, identity, x0_1)
    print(f"Estado inicial:   {x0_1}")
    print(f"Punto fijo:       {result_1.fixed_point}")
    print(f"Convergió:        {result_1.converged}")
    print(f"λ_max:            {result_1.lambda_max:.4f}")
    print(f"Estable:          {result_1.is_stable}")

    # Test 2: Sigmoid
    print("\n[TEST 2] Activación Sigmoid")
    print("-"*70)
    x0_2 = np.array([0.0, 0.0, 0.0])
    result_2 = analyze_network(W, sigmoid, x0_2)
    print(f"Estado inicial:   {x0_2}")
    print(f"Punto fijo:       {result_2.fixed_point}")
    print(f"Convergió:        {result_2.converged}")
    print(f"λ_max:            {result_2.lambda_max:.4f}")
    print(f"Estable:          {result_2.is_stable}")

    # Test 3: Tanh
    print("\n[TEST 3] Activación Tanh")
    print("-"*70)
    x0_3 = np.array([0.5, -0.5, 0.3])
    result_3 = analyze_network(W, tanh_fn, x0_3)
    print(f"Estado inicial:   {x0_3}")
    print(f"Punto fijo:       {result_3.fixed_point}")
    print(f"Convergió:        {result_3.converged}")
    print(f"λ_max:            {result_3.lambda_max:.4f}")
    print(f"Estable:          {result_3.is_stable}")

    print("\n" + "="*70)
    print("\n[GENERANDO VISUALIZACIONES]")
    print("-"*70)

    # Generate visualizations
    plot_convergence_comparison(W, x0_1, x0_2, x0_3)
    plot_phase_plane(W, x0_1, identity, "Identity")
    plot_phase_plane(W, x0_2, sigmoid, "Sigmoid")
    plot_phase_plane(W, x0_3, tanh_fn, "Tanh")
    plot_eigenvalue_stability(result_1.lambda_max, result_2.lambda_max, result_3.lambda_max)

    print("\n" + "="*70)
    print("ANÁLISIS COMPLETO")
    print("="*70 + "\n")
