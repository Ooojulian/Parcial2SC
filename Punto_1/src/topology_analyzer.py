"""
Topology analyzer for Internet networks.

Computes:
- Degree distribution (Ley de Potencia)
- Small world properties
- Clustering coefficient
- Percolation threshold
"""

import pickle
from pathlib import Path
from dataclasses import dataclass
from typing import Tuple, List, Dict

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


@dataclass
class TopologyMetrics:
    """Metrics describing network topology."""
    num_nodes: int
    num_edges: int
    avg_degree: float
    min_degree: int
    max_degree: int
    avg_shortest_path: float
    clustering_coefficient: float
    density: float
    gamma: float  # power law exponent (if scale-free)
    kappa: float  # kappa = <k^2>/<k> for percolation


class TopologyAnalyzer:
    """Analyze network topology properties."""

    def __init__(self, graph: nx.DiGraph):
        self.graph = graph
        self.metrics: TopologyMetrics = None

    def analyze(self) -> TopologyMetrics:
        """Compute all metrics."""
        # Convert to undirected for certain metrics
        G_undirected = self.graph.to_undirected()

        degrees = [d for n, d in self.graph.in_degree()]

        avg_deg = np.mean(degrees)
        max_deg = np.max(degrees)
        min_deg = np.min(degrees)
        deg2_avg = np.mean([d**2 for d in degrees])

        # Small world: compute average shortest path on largest component
        if len(G_undirected) > 100:
            largest_cc = max(nx.connected_components(G_undirected), key=len)
            subgraph = G_undirected.subgraph(largest_cc)
            avg_path = nx.average_shortest_path_length(subgraph)
        else:
            avg_path = nx.average_shortest_path_length(G_undirected)

        # Clustering coefficient (undirected)
        clustering = nx.average_clustering(G_undirected)

        # Density
        density = nx.density(G_undirected)

        # Power law exponent (via log-log regression on degree tail)
        gamma = self._estimate_power_law_exponent(degrees)

        # Kappa for percolation threshold
        kappa = deg2_avg / avg_deg if avg_deg > 0 else 0

        self.metrics = TopologyMetrics(
            num_nodes=self.graph.number_of_nodes(),
            num_edges=self.graph.number_of_edges(),
            avg_degree=avg_deg,
            min_degree=min_deg,
            max_degree=max_deg,
            avg_shortest_path=avg_path,
            clustering_coefficient=clustering,
            density=density,
            gamma=gamma,
            kappa=kappa
        )

        return self.metrics

    @staticmethod
    def _estimate_power_law_exponent(degrees: List[int], min_k: int = 2) -> float:
        """
        Estimate power law exponent γ from degree distribution.

        Uses log-log linear regression on the tail.
        P(k) ~ k^(-γ) => log P(k) ~ -γ log(k)
        """
        degrees = np.array(degrees)
        degrees = degrees[degrees >= min_k]

        if len(degrees) < 10:
            return np.nan

        # Count histogram
        unique_degs, counts = np.unique(degrees, return_counts=True)
        probs = counts / len(degrees)

        # Log-log fit
        log_k = np.log(unique_degs)
        log_p = np.log(probs)

        # Linear regression: log_p = a + b*log_k
        coeffs = np.polyfit(log_k, log_p, 1)
        gamma = -coeffs[0]  # slope is -gamma

        return gamma

    def plot_degree_distribution(self, filepath: str = None, figsize: Tuple = (12, 4)) -> None:
        """Plot degree distribution (linear and log-log)."""
        degrees = [d for n, d in self.graph.in_degree()]

        fig, axes = plt.subplots(1, 2, figsize=figsize)

        # Linear histogram
        ax = axes[0]
        ax.hist(degrees, bins=50, alpha=0.7, color='blue', edgecolor='black')
        ax.set_xlabel('Degree k', fontsize=12)
        ax.set_ylabel('Count', fontsize=12)
        ax.set_title('Degree Distribution (Linear)', fontsize=13, fontweight='bold')
        ax.grid(True, alpha=0.3)

        # Log-log (if scale-free)
        ax = axes[1]
        unique_degs, counts = np.unique(degrees, return_counts=True)
        probs = counts / len(degrees)

        ax.scatter(unique_degs, probs, alpha=0.6, s=50, color='darkblue')

        # Fit line
        if self.metrics:
            k_fit = np.logspace(0, np.log10(np.max(unique_degs)), 100)
            p_fit = (self.metrics.gamma ** (self.metrics.gamma)) / k_fit ** self.metrics.gamma
            p_fit = p_fit / np.sum(p_fit)  # normalize
            ax.loglog(k_fit, p_fit, 'r--', linewidth=2, label=f'P(k) ~ k^(-{self.metrics.gamma:.2f})')
            ax.legend(fontsize=11)

        ax.loglog(unique_degs, probs, 'o', markersize=6, color='darkblue', label='Empirical')
        ax.set_xlabel('Degree k', fontsize=12)
        ax.set_ylabel('P(k)', fontsize=12)
        ax.set_title('Degree Distribution (Log-Log)', fontsize=13, fontweight='bold')
        ax.grid(True, alpha=0.3, which='both')

        plt.tight_layout()

        if filepath:
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"✓ Saved: {filepath}")
        else:
            plt.show()

        plt.close()

    def plot_percolation_threshold(self, filepath: str = None, num_runs: int = 50) -> None:
        """
        Plot network robustness under random node removal.

        Simulates percolation by randomly removing nodes and measuring
        largest connected component size.
        """
        G_undirected = self.graph.to_undirected()
        largest_cc = max(nx.connected_components(G_undirected), key=len)
        G_main = G_undirected.subgraph(largest_cc).copy()

        fractions = np.linspace(0, 1, 20)
        lcc_sizes = []
        lcc_std = []

        for frac in fractions:
            sizes = []
            for _ in range(num_runs):
                G_test = G_main.copy()
                num_remove = int(frac * G_test.number_of_nodes())

                if num_remove > 0:
                    nodes_to_remove = np.random.choice(G_test.nodes(), size=num_remove, replace=False)
                    G_test.remove_nodes_from(nodes_to_remove)

                if G_test.number_of_nodes() > 0:
                    largest = max(nx.connected_components(G_test), key=len)
                    sizes.append(len(largest) / G_main.number_of_nodes())
                else:
                    sizes.append(0)

            lcc_sizes.append(np.mean(sizes))
            lcc_std.append(np.std(sizes))

        fig, ax = plt.subplots(figsize=(10, 6))

        ax.errorbar(fractions, lcc_sizes, yerr=lcc_std, marker='o', linewidth=2,
                   markersize=8, capsize=5, capthick=2, color='darkblue', label='Random removal')

        # Theoretical threshold (Molloy-Reed)
        if self.metrics:
            f_c = 1 - 1 / (self.metrics.kappa - 1) if self.metrics.kappa > 1 else 0
            ax.axvline(f_c, color='red', linestyle='--', linewidth=2, label=f'Percolation threshold f_c={f_c:.3f}')

        ax.set_xlabel('Fraction of nodes removed', fontsize=12)
        ax.set_ylabel('Relative size of largest component', fontsize=12)
        ax.set_title('Network Robustness: Percolation Analysis', fontsize=13, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=11)
        ax.set_ylim([0, 1.05])

        plt.tight_layout()

        if filepath:
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"✓ Saved: {filepath}")
        else:
            plt.show()

        plt.close()

    def print_summary(self) -> None:
        """Print metrics summary."""
        if not self.metrics:
            self.analyze()

        m = self.metrics
        print("\n" + "="*60)
        print("NETWORK TOPOLOGY METRICS")
        print("="*60)
        print(f"Nodes:                    {m.num_nodes}")
        print(f"Edges:                    {m.num_edges}")
        print(f"Average degree:           {m.avg_degree:.2f}")
        print(f"Degree range:             {m.min_degree} - {m.max_degree}")
        print(f"Network density:          {m.density:.6f}")
        print(f"\nSmall World Properties:")
        print(f"  Average shortest path:  {m.avg_shortest_path:.2f}")
        print(f"  Clustering coeff:       {m.clustering_coefficient:.4f}")
        print(f"\nScale-Free Analysis:")
        print(f"  Power law exponent γ:   {m.gamma:.2f} (P(k) ~ k^-γ)")
        print(f"  κ = <k²>/<k>:           {m.kappa:.2f}")
        if m.kappa > 1:
            f_c = 1 - 1 / (m.kappa - 1)
            print(f"  Percolation threshold:  f_c = {f_c:.3f}")
            print(f"  Robustness:             {'HIGH' if f_c > 0.5 else 'LOW'} (scale-free)")
        print("="*60 + "\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Analyze network topology")
    parser.add_argument("graph_file", help="Pickle file with NetworkX graph")
    parser.add_argument("--output-dir", default="results", help="Output directory for plots")

    args = parser.parse_args()

    with open(args.graph_file, 'rb') as f:
        G = pickle.load(f)

    analyzer = TopologyAnalyzer(G)
    analyzer.analyze()
    analyzer.print_summary()

    output_dir = args.output_dir
    analyzer.plot_degree_distribution(f"{output_dir}/degree_distribution.png")
    analyzer.plot_percolation_threshold(f"{output_dir}/percolation_threshold.png")
