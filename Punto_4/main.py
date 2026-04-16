#!/usr/bin/env python3
"""Main execution for Punto 4: Feigenbaum δ and Bifurcation Analysis."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import numpy as np
import matplotlib.pyplot as plt
from src.feigenbaum import (
    compute_feigenbaum_delta,
    lyapunov_exponent,
    bifurcation_diagram,
    control_unstable_orbit,
    FEIGENBAUM_DELTA
)

def plot_bifurcation_diagram(r_arr, x_arr):
    """Plot bifurcation diagram with annotations."""
    fig, ax = plt.subplots(figsize=(14, 8))

    ax.plot(r_arr, x_arr, ',k', markersize=0.5, alpha=0.5)

    # Mark bifurcation points
    bifurcations = [3.0, 3.449, 3.544, 3.569]
    for i, bf in enumerate(bifurcations):
        if bf <= r_arr.max():
            ax.axvline(x=bf, color='red', linestyle='--', alpha=0.4, linewidth=1)
            ax.text(bf, 0.95, f'B{i+1}\nr≈{bf:.3f}', fontsize=9, ha='center',
                   bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))

    ax.set_xlabel('Parámetro r', fontsize=12, fontweight='bold')
    ax.set_ylabel('Variable de estado x', fontsize=12, fontweight='bold')
    ax.set_title('Diagrama de Bifurcación: Ruta Período-Doble hacia Caos',
                fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_xlim(r_arr.min(), r_arr.max())

    plt.tight_layout()
    plt.savefig('results/bifurcation_diagram.png', dpi=150, bbox_inches='tight')
    print("   ✓ Saved: results/bifurcation_diagram.png")
    plt.close()


def plot_lyapunov_spectrum(r_values, lyapunovs):
    """Plot Lyapunov exponent spectrum."""
    fig, ax = plt.subplots(figsize=(12, 6))

    colors = ['green' if l < 0 else 'red' for l in lyapunovs]
    ax.scatter(r_values, lyapunovs, c=colors, s=100, alpha=0.7, edgecolors='black', linewidth=1.5)

    # Connect points with line
    ax.plot(r_values, lyapunovs, 'k-', alpha=0.3, linewidth=1)

    # Add critical line at λ=0
    ax.axhline(y=0, color='black', linestyle='--', linewidth=2, label='λ = 0 (Transición)')
    ax.axhline(y=np.log(2), color='blue', linestyle=':', linewidth=2, label='λ = ln(2) (Caos máx.)')

    # Shade regions
    ax.axhspan(-1, 0, alpha=0.1, color='green', label='Estable (λ<0)')
    ax.axhspan(0, 1, alpha=0.1, color='red', label='Caótico (λ>0)')

    ax.set_xlabel('Parámetro r', fontsize=12, fontweight='bold')
    ax.set_ylabel('Exponente de Lyapunov (λ)', fontsize=12, fontweight='bold')
    ax.set_title('Espectro de Lyapunov: Transición Orden → Caos', fontsize=13, fontweight='bold')
    ax.legend(fontsize=10, loc='upper left')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('results/lyapunov_spectrum.png', dpi=150, bbox_inches='tight')
    print("   ✓ Saved: results/lyapunov_spectrum.png")
    plt.close()


def plot_feigenbaum_scaling(delta_seq):
    """Plot Feigenbaum delta convergence."""
    fig, ax = plt.subplots(figsize=(10, 6))

    iterations = np.arange(len(delta_seq))
    # Filter out invalid values (δ should be around 4.67)
    valid_deltas = [d for d in delta_seq if 0 < d < 10]
    valid_iters = np.arange(len(valid_deltas))

    if len(valid_deltas) > 0:
        ax.plot(valid_iters, valid_deltas, 'bo-', linewidth=2, markersize=8, label='Estimated δ')
        ax.axhline(y=FEIGENBAUM_DELTA, color='red', linestyle='--', linewidth=2,
                  label=f'Theoretical δ = {FEIGENBAUM_DELTA:.6f}')

        ax.fill_between(valid_iters, FEIGENBAUM_DELTA - 0.1, FEIGENBAUM_DELTA + 0.1,
                       alpha=0.2, color='red', label='±5% margin')

    ax.set_xlabel('Bifurcation Number', fontsize=12, fontweight='bold')
    ax.set_ylabel('Feigenbaum δ', fontsize=12, fontweight='bold')
    ax.set_title('Convergencia de la Constante de Feigenbaum δ', fontsize=13, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(3.5, 5.5)

    plt.tight_layout()
    plt.savefig('results/feigenbaum_convergence.png', dpi=150, bbox_inches='tight')
    print("   ✓ Saved: results/feigenbaum_convergence.png")
    plt.close()


if __name__ == "__main__":
    # Create results directory
    Path("results").mkdir(exist_ok=True)

    print("\n" + "="*70)
    print("PUNTO 4: CONSTANTE DE FEIGENBAUM δ")
    print("Bifurcaciones Período-Doble y Universalidad")
    print("="*70 + "\n")

    # Compute Feigenbaum delta
    print("[1] CONSTANTE DE FEIGENBAUM δ")
    print("-"*70)
    print("Calculando bifurcaciones de período-doble...")
    delta_seq, avg_delta = compute_feigenbaum_delta(
        r_min=2.8, r_max=3.5698, num_bifurcations=15
    )

    print(f"\nSecuencia de δ (primeras 5): {delta_seq[:5]}")
    print(f"Delta promedio:  {avg_delta:.6f}")
    print(f"Delta teórico:   {FEIGENBAUM_DELTA:.6f}")
    error = abs(avg_delta - FEIGENBAUM_DELTA)
    print(f"Error absoluto:  {error:.6f}")
    if avg_delta > 0:
        percent_error = (error / FEIGENBAUM_DELTA) * 100
        print(f"Error relativo:  {percent_error:.2f}%")

    # Lyapunov exponents
    print("\n[2] EXPONENTES DE LYAPUNOV")
    print("-"*70)
    print("λ > 0: comportamiento caótico")
    print("λ < 0: comportamiento estable\n")

    test_r_values = [2.8, 3.0, 3.3, 3.5, 3.57, 3.8, 3.95, 4.0]
    for r in test_r_values:
        lya = lyapunov_exponent(r, steps=2000)
        regime = "CAÓTICO" if lya > 0.01 else "ESTABLE"
        print(f"  r = {r:.2f}: λ = {lya:8.4f}  ({regime})")

    # Bifurcation diagram computation info
    print("\n[3] DIAGRAMA DE BIFURCACIÓN")
    print("-"*70)
    print("Computando diagrama (2000 valores de r, 100 iteraciones cada uno)...")
    r_arr, x_arr = bifurcation_diagram(
        r_min=2.8, r_max=4.0, num_r=2000, num_iterations=100
    )
    print(f"✓ Calculados {len(r_arr)} puntos")
    print(f"  Rango r: [{r_arr.min():.3f}, {r_arr.max():.3f}]")
    print(f"  Rango x: [{x_arr.min():.3f}, {x_arr.max():.3f}]")

    # Control of chaotic orbits
    print("\n[4] CONTROL DE ÓRBITAS CAÓTICAS")
    print("-"*70)
    print("Intento de estabilizar órbita periódica inestable (r=3.95, T=2)\n")

    gains = [0.05, 0.1, 0.15, 0.2]
    for gain in gains:
        traj, stabilized = control_unstable_orbit(
            r=3.95, x0=0.5, target_period=2, control_gain=gain, steps=200
        )
        status = "✓ ESTABILIZADO" if stabilized else "✗ no estabilizado"
        final_variance = np.var(traj[-2:])
        print(f"  Ganancia K={gain:.2f}: {status} (varianza final ≈ {final_variance:.2e})")

    # Generate visualizations
    print("\n[5] GENERANDO VISUALIZACIONES")
    print("-"*70)
    plot_bifurcation_diagram(r_arr, x_arr)

    # Generate Lyapunov spectrum for visualization
    r_for_lyap = np.linspace(2.8, 4.0, 50)
    lyap_values = [lyapunov_exponent(r, steps=2000) for r in r_for_lyap]
    plot_lyapunov_spectrum(r_for_lyap, lyap_values)

    # Plot Feigenbaum delta convergence
    plot_feigenbaum_scaling(delta_seq)

    print("\n" + "="*70 + "\n")
