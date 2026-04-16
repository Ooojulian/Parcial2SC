"""Tests for distributed routing simulator."""

import pytest
import networkx as nx

from src.routing_simulator import DistributedRoutingSimulator
from src.network_generator import NetworkConfig, InternetTopologyGenerator


class TestDistributedRoutingSimulator:
    """Test routing simulation."""

    @pytest.fixture
    def simple_graph(self):
        """Create simple test graph for routing."""
        G = nx.DiGraph()
        G.add_weighted_edges_from([
            (0, 1, 1.0),
            (1, 0, 1.0),
            (1, 2, 1.0),
            (2, 1, 1.0),
            (0, 2, 3.0),
            (2, 0, 3.0),
        ])
        return G

    @pytest.fixture
    def ba_graph(self):
        """Generate BA topology for testing."""
        config = NetworkConfig(num_nodes=50, seed=42)
        gen = InternetTopologyGenerator(config)
        return gen.generate()

    def test_simulator_initialization(self, simple_graph):
        sim = DistributedRoutingSimulator(simple_graph, source_node=0)

        assert sim.graph is simple_graph
        assert sim.source == 0
        assert sim.converged is False
        assert sim.convergence_time is None

    def test_routing_table_initialization(self, simple_graph):
        sim = DistributedRoutingSimulator(simple_graph, source_node=0)
        sim.initialize()

        # Source should know itself
        assert 0 in sim.routing_tables[0]
        assert sim.routing_tables[0][0][1] == 0  # distance to self is 0

        # Messages should be queued for neighbors
        total_messages = sum(len(q) for q in sim.message_queues.values())
        assert total_messages > 0

    def test_single_step(self, simple_graph):
        sim = DistributedRoutingSimulator(simple_graph, source_node=0)
        sim.initialize()

        # First step
        changed = sim.step(0)
        assert isinstance(changed, bool)

    def test_convergence(self, simple_graph):
        sim = DistributedRoutingSimulator(simple_graph, source_node=0)
        convergence_time = sim.run(max_steps=100)

        assert sim.converged
        assert convergence_time > 0
        assert convergence_time < 100

    def test_convergence_on_ba_graph(self, ba_graph):
        """Test convergence on larger graph."""
        sim = DistributedRoutingSimulator(ba_graph, source_node=0)
        convergence_time = sim.run(max_steps=500)

        assert sim.converged
        # Convergence should be O(n) in worst case but much faster in practice
        assert convergence_time < ba_graph.number_of_nodes() * 2

    def test_routing_correctness(self, simple_graph):
        """Verify computed routes are valid."""
        sim = DistributedRoutingSimulator(simple_graph, source_node=0)
        sim.run()

        # Check that all reachable nodes have valid routes
        for node, routing_table in sim.routing_tables.items():
            for dest, (next_hop, dist) in routing_table.items():
                # Next hop must be a successor of current node
                if node != dest:
                    assert next_hop in list(simple_graph.successors(node)) or next_hop == node

    def test_perturbation_sensitivity(self, ba_graph):
        """Test sensitivity to edge perturbations."""
        sim = DistributedRoutingSimulator(ba_graph, source_node=0)

        # Get an edge to perturb
        edges = list(ba_graph.edges())
        if len(edges) > 0:
            test_edge = edges[0]

            # Measure re-convergence
            conv_time, table_size = sim.check_stability_under_perturbation(
                test_edge,
                perturb_weight_change=0.5,
                max_steps=200
            )

            assert conv_time > 0
            assert table_size >= 0

    def test_multiple_sources(self, simple_graph):
        """Test that different sources converge."""
        for source in simple_graph.nodes():
            sim = DistributedRoutingSimulator(simple_graph, source_node=source)
            convergence_time = sim.run(max_steps=100)

            assert sim.converged
            assert convergence_time > 0

    def test_print_summary(self, simple_graph, capsys):
        """Test summary output."""
        sim = DistributedRoutingSimulator(simple_graph, source_node=0)
        sim.run()
        sim.print_summary()

        captured = capsys.readouterr()
        assert "DISTRIBUTED ROUTING SIMULATOR" in captured.out
        assert "Convergence time:" in captured.out
