#!/usr/bin/env python3
"""
Main execution script for Punto 1: Internet Complexity Analysis.

Genera topologías de red y realiza análisis completo de complejidad.
"""

import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.network_generator import NetworkConfig, InternetTopologyGenerator
from src.topology_analyzer import TopologyAnalyzer
from src.routing_simulator import DistributedRoutingSimulator


def main():
    parser = argparse.ArgumentParser(
        description="Punto 1: Internet Complexity Analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --nodes 500 --type ba
  python main.py --nodes 1000 --type isp --output custom_results/
        """
    )

    parser.add_argument("--nodes", type=int, default=500,
                       help="Number of nodes (default: 500)")
    parser.add_argument("--type", choices=["ba", "er", "isp"], default="ba",
                       help="Network type (default: ba)")
    parser.add_argument("--seed", type=int, default=42,
                       help="Random seed (default: 42)")
    parser.add_argument("--output", default="results",
                       help="Output directory (default: results)")
    parser.add_argument("--skip-plots", action="store_true",
                       help="Skip generating plots")

    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("\n" + "="*70)
    print("PUNTO 1: INTERNET COMPLEXITY - MATHEMATICAL MODEL")
    print("="*70)

    # Step 1: Generate topology
    print("\n[1/4] Generating network topology...")
    config = NetworkConfig(
        num_nodes=args.nodes,
        seed=args.seed,
        network_type={"ba": "barabasi_albert", "er": "erdos_renyi", "isp": "isp"}[args.type]
    )

    gen = InternetTopologyGenerator(config)
    graph = gen.generate()
    graph_file = output_dir / f"topology_{args.type}_{args.nodes}.pkl"
    gen.save(str(graph_file))
    print(f"   ✓ Network: {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges")
    print(f"   ✓ Saved to: {graph_file}")

    # Step 2: Topology analysis
    print("\n[2/4] Analyzing topology properties...")
    analyzer = TopologyAnalyzer(graph)
    metrics = analyzer.analyze()
    analyzer.print_summary()

    if not args.skip_plots:
        print("\n[3/4] Generating visualizations...")

        degree_plot = output_dir / "degree_distribution.png"
        analyzer.plot_degree_distribution(str(degree_plot))

        percolation_plot = output_dir / "percolation_threshold.png"
        analyzer.plot_percolation_threshold(str(percolation_plot), num_runs=30)

        print(f"   ✓ Plots saved to {output_dir}/")

    # Step 3: Routing simulation
    print("\n[4/4] Simulating distributed routing (BGP-like)...")
    sim = DistributedRoutingSimulator(graph, source_node=0)
    convergence_time = sim.run(max_steps=1000)
    sim.print_summary()

    if not args.skip_plots:
        routing_convergence = output_dir / "routing_convergence.png"
        sim.plot_convergence(str(routing_convergence))

        routing_sensitivity = output_dir / "routing_sensitivity.png"
        sim.plot_sensitivity_analysis(str(routing_sensitivity), num_perturbations=15)

        print(f"   ✓ Routing plots saved to {output_dir}/")

    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)
    print(f"\nOutput directory: {output_dir.absolute()}")
    print("\nGenerated files:")
    for file in sorted(output_dir.glob("*")):
        print(f"  - {file.name}")

    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
