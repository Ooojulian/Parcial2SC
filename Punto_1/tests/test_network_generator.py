"""Tests for network generator module."""

import pytest
import tempfile
import networkx as nx
from pathlib import Path

from src.network_generator import NetworkConfig, InternetTopologyGenerator


class TestNetworkConfig:
    """Test configuration dataclass."""

    def test_default_config(self):
        cfg = NetworkConfig(num_nodes=100)
        assert cfg.num_nodes == 100
        assert cfg.seed == 42
        assert cfg.network_type == "barabasi_albert"

    def test_custom_config(self):
        cfg = NetworkConfig(num_nodes=500, seed=123, network_type="erdos_renyi")
        assert cfg.num_nodes == 500
        assert cfg.seed == 123
        assert cfg.network_type == "erdos_renyi"


class TestInternetTopologyGenerator:
    """Test topology generation."""

    def test_barabasi_albert_generation(self):
        config = NetworkConfig(num_nodes=100, seed=42)
        gen = InternetTopologyGenerator(config)
        G = gen.generate()

        assert isinstance(G, nx.DiGraph)
        assert G.number_of_nodes() == 100
        assert G.number_of_edges() > 0
        # BA with m=2 should have roughly 2*n edges (each edge is bidirectional)
        assert G.number_of_edges() > 100

    def test_erdos_renyi_generation(self):
        config = NetworkConfig(num_nodes=50, network_type="erdos_renyi", seed=42)
        gen = InternetTopologyGenerator(config)
        G = gen.generate()

        assert isinstance(G, nx.DiGraph)
        assert G.number_of_nodes() == 50

    def test_isp_hierarchy_generation(self):
        config = NetworkConfig(num_nodes=300, network_type="isp", seed=42)
        gen = InternetTopologyGenerator(config)
        G = gen.generate()

        assert isinstance(G, nx.DiGraph)
        assert G.number_of_nodes() == 300
        assert G.number_of_edges() > 0

    def test_edge_weights(self):
        """Check all edges have weights."""
        config = NetworkConfig(num_nodes=50)
        gen = InternetTopologyGenerator(config)
        G = gen.generate()

        for u, v, data in G.edges(data=True):
            assert 'weight' in data
            assert data['weight'] > 0

    def test_reproducibility(self):
        """Same seed should produce same topology."""
        config1 = NetworkConfig(num_nodes=100, seed=999)
        config2 = NetworkConfig(num_nodes=100, seed=999)

        gen1 = InternetTopologyGenerator(config1)
        gen2 = InternetTopologyGenerator(config2)

        G1 = gen1.generate()
        G2 = gen2.generate()

        # Same degree sequence
        deg1 = sorted([d for n, d in G1.in_degree()])
        deg2 = sorted([d for n, d in G2.in_degree()])

        assert deg1 == deg2

    def test_save_load(self):
        """Test persistence."""
        config = NetworkConfig(num_nodes=50)
        gen = InternetTopologyGenerator(config)
        G_original = gen.generate()

        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = f"{tmpdir}/test_graph.pkl"
            gen.save(filepath)

            # Verify file exists
            assert Path(filepath).exists()

            # Load and compare
            G_loaded = InternetTopologyGenerator.load(filepath)

            assert G_loaded.number_of_nodes() == G_original.number_of_nodes()
            assert G_loaded.number_of_edges() == G_original.number_of_edges()

    def test_invalid_network_type(self):
        """Unknown network type raises error."""
        config = NetworkConfig(num_nodes=50, network_type="unknown")
        gen = InternetTopologyGenerator(config)

        with pytest.raises(ValueError):
            gen.generate()
