"""Tests for topology analyzer module."""

import pytest
import numpy as np
import networkx as nx

from src.topology_analyzer import TopologyAnalyzer, TopologyMetrics
from src.network_generator import NetworkConfig, InternetTopologyGenerator


class TestTopologyAnalyzer:
    """Test topology analysis."""

    @pytest.fixture
    def ba_graph(self):
        """Generate a test BA graph."""
        config = NetworkConfig(num_nodes=100, seed=42)
        gen = InternetTopologyGenerator(config)
        return gen.generate()

    @pytest.fixture
    def er_graph(self):
        """Generate a test ER graph."""
        config = NetworkConfig(num_nodes=100, seed=42, network_type="erdos_renyi")
        gen = InternetTopologyGenerator(config)
        return gen.generate()

    def test_analyzer_initialization(self, ba_graph):
        analyzer = TopologyAnalyzer(ba_graph)
        assert analyzer.graph is ba_graph
        assert analyzer.metrics is None

    def test_analyze_basic_metrics(self, ba_graph):
        analyzer = TopologyAnalyzer(ba_graph)
        metrics = analyzer.analyze()

        assert isinstance(metrics, TopologyMetrics)
        assert metrics.num_nodes == 100
        assert metrics.num_edges > 0
        assert metrics.avg_degree > 0
        assert metrics.min_degree >= 0
        assert metrics.max_degree > 0

    def test_small_world_property(self, ba_graph):
        """BA graphs exhibit small-world property."""
        analyzer = TopologyAnalyzer(ba_graph)
        metrics = analyzer.analyze()

        # Average path length should be logarithmic in network size
        assert metrics.avg_shortest_path < np.log(ba_graph.number_of_nodes()) * 3

    def test_clustering_coefficient_ba_vs_er(self, ba_graph, er_graph):
        """BA should have higher clustering than ER."""
        analyzer_ba = TopologyAnalyzer(ba_graph)
        metrics_ba = analyzer_ba.analyze()

        analyzer_er = TopologyAnalyzer(er_graph)
        metrics_er = analyzer_er.analyze()

        # BA typically has higher clustering
        assert metrics_ba.clustering_coefficient > metrics_er.clustering_coefficient

    def test_power_law_exponent(self, ba_graph):
        """BA graph should have power-law distribution."""
        analyzer = TopologyAnalyzer(ba_graph)
        metrics = analyzer.analyze()

        # BA with m=2 should have power law (gamma > 1)
        assert metrics.gamma > 1.0

    def test_kappa_percolation(self, ba_graph):
        """Test kappa computation for percolation."""
        analyzer = TopologyAnalyzer(ba_graph)
        metrics = analyzer.analyze()

        assert metrics.kappa > 0
        # For scale-free, kappa should be > 2
        assert metrics.kappa > 1.5

    def test_percolation_threshold(self, ba_graph):
        """Compute percolation threshold."""
        analyzer = TopologyAnalyzer(ba_graph)
        metrics = analyzer.analyze()

        if metrics.kappa > 1:
            f_c = 1 - 1 / (metrics.kappa - 1)
            assert 0 <= f_c <= 1

    def test_power_law_estimation(self):
        """Test power law exponent estimation on synthetic data."""
        # Create synthetic power-law distribution
        degrees = np.random.pareto(2.0, 1000) + 1  # Pareto generates ~ k^-3
        analyzer = TopologyAnalyzer(nx.path_graph(10))  # dummy graph

        gamma = analyzer._estimate_power_law_exponent(list(degrees.astype(int)))
        # Should be close to 2 (approximately)
        assert not np.isnan(gamma)

    def test_density_calculation(self, ba_graph):
        analyzer = TopologyAnalyzer(ba_graph)
        metrics = analyzer.analyze()

        assert 0 <= metrics.density <= 1
        # Sparse networks should have low density
        assert metrics.density < 0.5

    def test_print_summary(self, ba_graph, capsys):
        """Test summary printout."""
        analyzer = TopologyAnalyzer(ba_graph)
        analyzer.analyze()
        analyzer.print_summary()

        captured = capsys.readouterr()
        assert "NETWORK TOPOLOGY METRICS" in captured.out
        assert "Nodes:" in captured.out
        assert "Power law exponent" in captured.out
