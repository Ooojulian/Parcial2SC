"""
Network generator for Internet topology modeling.

Implements:
- Barabási-Albert (scale-free)
- Erdős-Rényi (random)
- ISP-like hierarchical topologies
"""

import pickle
from pathlib import Path
from dataclasses import dataclass
from typing import Tuple, List, Dict

import networkx as nx
import numpy as np


@dataclass
class NetworkConfig:
    """Configuration for network generation."""
    num_nodes: int
    seed: int = 42
    network_type: str = "barabasi_albert"  # or "erdos_renyi", "isp"


class InternetTopologyGenerator:
    """Generate realistic Internet topologies."""

    def __init__(self, config: NetworkConfig):
        self.config = config
        self.rng = np.random.RandomState(config.seed)
        np.random.seed(config.seed)
        self.graph: nx.DiGraph = None

    def generate(self) -> nx.DiGraph:
        """Generate network based on config."""
        if self.config.network_type == "barabasi_albert":
            return self._generate_barabasi_albert()
        elif self.config.network_type == "erdos_renyi":
            return self._generate_erdos_renyi()
        elif self.config.network_type == "isp":
            return self._generate_isp_hierarchy()
        else:
            raise ValueError(f"Unknown network type: {self.config.network_type}")

    def _generate_barabasi_albert(self) -> nx.DiGraph:
        """
        Barabási-Albert (preferential attachment) model.

        Generates scale-free networks with P(k) ~ k^-3.
        Realistic for Internet AS-level topology.
        """
        # Undirected BA then convert to directed
        ba_graph = nx.barabasi_albert_graph(
            self.config.num_nodes,
            m=2,  # each new node connects to m existing nodes
            seed=self.config.seed
        )

        # Convert to directed: each edge becomes bidirectional
        G = nx.DiGraph()
        G.add_nodes_from(ba_graph.nodes())

        for u, v in ba_graph.edges():
            weight = self.rng.uniform(0.5, 10.0)  # random latency/bandwidth
            G.add_edge(u, v, weight=weight)
            G.add_edge(v, u, weight=weight)

        self.graph = G
        return G

    def _generate_erdos_renyi(self) -> nx.DiGraph:
        """
        Erdős-Rényi random graph model.

        Generates random networks with Poisson degree distribution.
        Used as baseline comparison.
        """
        p = 2 * np.log(self.config.num_nodes) / self.config.num_nodes

        er_graph = nx.erdos_renyi_graph(
            self.config.num_nodes,
            p,
            seed=self.config.seed
        )

        G = nx.DiGraph()
        G.add_nodes_from(er_graph.nodes())

        for u, v in er_graph.edges():
            weight = self.rng.uniform(0.5, 10.0)
            G.add_edge(u, v, weight=weight)
            G.add_edge(v, u, weight=weight)

        self.graph = G
        return G

    def _generate_isp_hierarchy(self) -> nx.DiGraph:
        """
        ISP-like hierarchical topology.

        Creates tier structure:
        - Tier 1: Backbone (few high-degree nodes)
        - Tier 2: Regional (moderate degree)
        - Tier 3: Local (low degree)
        """
        G = nx.DiGraph()

        # Tier 1: Backbone routers (5-10 nodes)
        tier1_count = max(5, self.config.num_nodes // 200)
        tier1_nodes = list(range(tier1_count))

        # Tier 2: Regional routers
        tier2_count = max(20, self.config.num_nodes // 50)
        tier2_nodes = list(range(tier1_count, tier1_count + tier2_count))

        # Tier 3: Local/edge
        tier3_nodes = list(range(tier1_count + tier2_count, self.config.num_nodes))

        # Add all nodes
        G.add_nodes_from(tier1_nodes + tier2_nodes + tier3_nodes)

        # Tier 1: Full mesh (all connected to all)
        for i in tier1_nodes:
            for j in tier1_nodes:
                if i != j:
                    w = self.rng.uniform(0.1, 1.0)  # low latency backbone
                    G.add_edge(i, j, weight=w)

        # Tier 2: Connect to multiple Tier 1 (2-3 connections)
        for node in tier2_nodes:
            tier1_neighbors = self.rng.choice(tier1_nodes, size=min(3, len(tier1_nodes)), replace=False)
            for t1 in tier1_neighbors:
                w = self.rng.uniform(1.0, 5.0)
                G.add_edge(node, t1, weight=w)
                G.add_edge(t1, node, weight=w)

        # Tier 3: Connect to 1-2 Tier 2
        for node in tier3_nodes:
            tier2_neighbors = self.rng.choice(tier2_nodes, size=min(2, len(tier2_nodes)), replace=False)
            for t2 in tier2_neighbors:
                w = self.rng.uniform(5.0, 20.0)
                G.add_edge(node, t2, weight=w)
                G.add_edge(t2, node, weight=w)

        self.graph = G
        return G

    def save(self, filepath: str) -> None:
        """Save graph to pickle file."""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump(self.graph, f)

    @staticmethod
    def load(filepath: str) -> nx.DiGraph:
        """Load graph from pickle file."""
        with open(filepath, 'rb') as f:
            return pickle.load(f)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate Internet topology")
    parser.add_argument("--nodes", type=int, default=1000, help="Number of nodes")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--type", choices=["ba", "er", "isp"], default="ba", help="Network type")
    parser.add_argument("--output", default="results/topology.pkl", help="Output file")

    args = parser.parse_args()

    config = NetworkConfig(
        num_nodes=args.nodes,
        seed=args.seed,
        network_type={"ba": "barabasi_albert", "er": "erdos_renyi", "isp": "isp"}[args.type]
    )

    gen = InternetTopologyGenerator(config)
    graph = gen.generate()
    gen.save(args.output)

    print(f"✓ Generated {config.network_type} network with {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges")
    print(f"✓ Saved to {args.output}")
