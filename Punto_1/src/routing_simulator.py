"""
BGP-like distributed routing simulator.

Demonstrates:
- Distributed shortest path computation
- Convergence behavior under perturbations
- Sensitivity to initial conditions
"""

import pickle
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Tuple, Set

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


@dataclass
class RoutingState:
    """State of routing table at a router."""
    router_id: int
    routing_table: Dict[int, Tuple[int, float]]  # dst -> (next_hop, distance)
    timestamp: int


class DistributedRoutingSimulator:
    """Simulate distributed shortest path routing (BGP-like)."""

    def __init__(self, graph: nx.DiGraph, source_node: int = 0):
        self.graph = graph
        self.source = source_node
        self.num_nodes = graph.number_of_nodes()

        # Initialize routing tables: {node -> {dest -> (next_hop, dist)}}
        self.routing_tables: Dict[int, Dict[int, Tuple[int, float]]] = {
            n: {} for n in graph.nodes()
        }

        # Message queues: {node -> [(src, dest, distance, timestamp)]}
        self.message_queues: Dict[int, List[Tuple[int, int, float, int]]] = {
            n: [] for n in graph.nodes()
        }

        self.history: List[RoutingState] = []
        self.converged = False
        self.convergence_time = None

    def initialize(self) -> None:
        """Initialize source sends distance vector to neighbors."""
        # Source knows itself: distance 0
        self.routing_tables[self.source][self.source] = (self.source, 0)

        # Send initial updates to neighbors
        for neighbor in self.graph.successors(self.source):
            weight = self.graph[self.source][neighbor].get('weight', 1.0)
            self.message_queues[neighbor].append(
                (self.source, self.source, weight, 0)
            )

    def step(self, step_num: int) -> bool:
        """
        Execute one routing step.

        Returns True if any routing table changed.
        """
        changed = False

        # Process all incoming messages
        for node in self.graph.nodes():
            # Handle messages in queue
            while self.message_queues[node]:
                src, dest, distance, timestamp = self.message_queues[node].pop(0)

                # Update if better path found
                if dest not in self.routing_tables[node] or \
                   distance < self.routing_tables[node][dest][1]:

                    self.routing_tables[node][dest] = (src, distance)
                    changed = True

                    # Propagate to neighbors (Bellman-Ford)
                    for neighbor in self.graph.successors(node):
                        edge_weight = self.graph[node][neighbor].get('weight', 1.0)
                        new_dist = distance + edge_weight

                        self.message_queues[neighbor].append(
                            (node, dest, new_dist, step_num + 1)
                        )

        if not changed and not any(self.message_queues.values()):
            self.converged = True
            if self.convergence_time is None:
                self.convergence_time = step_num

        return changed

    def run(self, max_steps: int = 1000) -> int:
        """Run simulation until convergence or max steps."""
        self.initialize()

        for t in range(max_steps):
            if not self.step(t):
                break

        self.convergence_time = t
        return self.convergence_time

    def check_stability_under_perturbation(self, perturb_edge: Tuple[int, int],
                                          perturb_weight_change: float = 0.5,
                                          max_steps: int = 100) -> Tuple[int, float]:
        """
        Test robustness: perturb edge weight and measure re-convergence.

        Returns: (convergence_steps, table_change_ratio)
        """
        original_weight = self.graph[perturb_edge[0]][perturb_edge[1]].get('weight', 1.0)

        # Perturb weight
        self.graph[perturb_edge[0]][perturb_edge[1]]['weight'] = original_weight * perturb_weight_change

        # Reset routing tables
        self.routing_tables = {n: {} for n in self.graph.nodes()}
        self.message_queues = {n: [] for n in self.graph.nodes()}
        self.converged = False
        self.convergence_time = None

        # Re-run
        convergence_steps = self.run(max_steps)

        # Compute table change
        old_tables = {n: len(rt) for n, rt in self.routing_tables.items()}
        table_change = np.mean(list(old_tables.values()))

        # Restore
        self.graph[perturb_edge[0]][perturb_edge[1]]['weight'] = original_weight

        return convergence_steps, table_change

    def plot_convergence(self, filepath: str = None) -> None:
        """Plot convergence behavior."""
        # Simulate and track table changes
        self.initialize()
        table_sizes = [0]

        for t in range(min(500, self.num_nodes * 10)):
            changed = self.step(t)
            total_entries = sum(len(rt) for rt in self.routing_tables.values())
            table_sizes.append(total_entries)

            if self.converged:
                break

        fig, ax = plt.subplots(figsize=(10, 6))

        ax.plot(table_sizes, linewidth=2, color='darkblue', marker='o', markersize=4)
        ax.axvline(self.convergence_time, color='red', linestyle='--', linewidth=2,
                   label=f'Convergence time: {self.convergence_time} steps')

        ax.set_xlabel('Time steps', fontsize=12)
        ax.set_ylabel('Total routing table entries', fontsize=12)
        ax.set_title('BGP-like Distributed Routing: Convergence', fontsize=13, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=11)

        plt.tight_layout()

        if filepath:
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"✓ Saved: {filepath}")
        else:
            plt.show()

        plt.close()

    def plot_sensitivity_analysis(self, filepath: str = None, num_perturbations: int = 20) -> None:
        """
        Test sensitivity to perturbations.

        Perturb random edges and measure re-convergence variation.
        """
        edges = list(self.graph.edges())
        np.random.shuffle(edges)
        test_edges = edges[:min(num_perturbations, len(edges))]

        convergence_times = []
        table_changes = []

        for edge in test_edges:
            conv_t, table_ch = self.check_stability_under_perturbation(
                edge,
                perturb_weight_change=0.3,
                max_steps=200
            )
            convergence_times.append(conv_t)
            table_changes.append(table_ch)

        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        # Convergence times
        ax = axes[0]
        ax.hist(convergence_times, bins=15, alpha=0.7, color='blue', edgecolor='black')
        ax.axvline(np.mean(convergence_times), color='red', linestyle='--', linewidth=2,
                   label=f'Mean: {np.mean(convergence_times):.1f}')
        ax.set_xlabel('Re-convergence time (steps)', fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.set_title('Convergence Time After Edge Perturbation', fontsize=12, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)

        # Table changes
        ax = axes[1]
        ax.scatter(convergence_times, table_changes, alpha=0.6, s=100, color='darkgreen')
        ax.set_xlabel('Re-convergence time', fontsize=12)
        ax.set_ylabel('Avg routing table size', fontsize=12)
        ax.set_title('Sensitivity to Edge Weight Perturbations', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        if filepath:
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"✓ Saved: {filepath}")
        else:
            plt.show()

        plt.close()

    def print_summary(self) -> None:
        """Print routing statistics."""
        total_entries = sum(len(rt) for rt in self.routing_tables.values())
        avg_per_node = total_entries / self.num_nodes if self.num_nodes > 0 else 0

        print("\n" + "="*60)
        print("DISTRIBUTED ROUTING SIMULATOR RESULTS")
        print("="*60)
        print(f"Source node:              {self.source}")
        print(f"Convergence time:         {self.convergence_time} steps")
        print(f"Total routing entries:    {total_entries}")
        print(f"Avg entries per node:     {avg_per_node:.1f}")
        print(f"Network complexity:       O(n²) in worst case (BGP)")
        print("="*60 + "\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Simulate BGP routing")
    parser.add_argument("graph_file", help="Pickle file with NetworkX graph")
    parser.add_argument("--source", type=int, default=0, help="Source node")
    parser.add_argument("--steps", type=int, default=1000, help="Max steps")
    parser.add_argument("--output-dir", default="results", help="Output directory")

    args = parser.parse_args()

    with open(args.graph_file, 'rb') as f:
        G = pickle.load(f)

    sim = DistributedRoutingSimulator(G, source_node=args.source)
    sim.run(args.steps)
    sim.print_summary()

    output_dir = args.output_dir
    sim.plot_convergence(f"{output_dir}/routing_convergence.png")
    sim.plot_sensitivity_analysis(f"{output_dir}/routing_sensitivity.png")
