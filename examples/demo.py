#!/usr/bin/env python3
"""
Lootbox Toolkit Demo

Demonstrates the key features of the lootbox probability calculation toolkit
with practical examples for different use cases.
"""
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.models import Lootbox, LootboxItem, RarityTier
from src.calculator.expected_value import ExpectedValueCalculator
from src.simulator.monte_carlo import MonteCarloSimulator
from src.optimizer.probability_optimizer import ProbabilityOptimizer

def print_header(title: str):
    """Print formatted header"""
    print(f"\n{'='*60}")
    print(f"{title:^60}")
    print(f"{'='*60}\n")

def create_example_lootbox() -> Lootbox:
    """Create an example lootbox for demonstration"""
    items = [
        LootboxItem(name="Common Coins", value=0.25, rarity=RarityTier.COMMON, probability=0.50),
        LootboxItem(name="Silver Token", value=0.75, rarity=RarityTier.UNCOMMON, probability=0.25),
        LootboxItem(name="Gold Gem", value=2.50, rarity=RarityTier.RARE, probability=0.15),
        LootboxItem(name="Diamond Ring", value=8.00, rarity=RarityTier.EPIC, probability=0.08),
        LootboxItem(name="Legendary Sword", value=25.00, rarity=RarityTier.LEGENDARY, probability=0.02)
    ]
    
    return Lootbox(
        name="Demo Lootbox",
        description="Example lootbox for demonstration",
        cost=2.00,
        items=items
    )

def demo_basic_analysis():
    """Demonstrate basic lootbox analysis"""
    print_header("BASIC ANALYSIS DEMO")
    
    lootbox = create_example_lootbox()
    calculator = ExpectedValueCalculator()
    
    print(f"Lootbox: {lootbox.name}")
    print(f"Cost: ${lootbox.cost:.2f}")
    print(f"Items: {len(lootbox.items)}")
    
    # Basic metrics
    ev = calculator.calculate_expected_value(lootbox)
    variance = calculator.calculate_variance(lootbox)
    std_dev = calculator.calculate_standard_deviation(lootbox)
    house_edge = calculator.calculate_house_edge(lootbox)
    
    print(f"\nExpected Value: ${ev:.4f}")
    print(f"House Edge: {house_edge*100:.2f}%")
    print(f"Standard Deviation: ${std_dev:.4f}")
    print(f"Variance: ${variance:.4f}")
    
    # Probabilities
    break_even_prob = calculator.calculate_break_even_probability(lootbox)
    profit_prob = calculator.calculate_profit_probability(lootbox, 0.1)
    
    print(f"\nBreak Even Probability: {break_even_prob*100:.2f}%")
    print(f"10%+ Profit Probability: {profit_prob*100:.2f}%")
    
    # Full analysis
    analytics = calculator.generate_full_analysis(lootbox)
    print(f"\nRisk Level: {analytics.get_risk_level()}")
    print(f"Player Value Rating: {analytics.get_player_value_rating()}")

def demo_monte_carlo_simulation():
    """Demonstrate Monte Carlo simulation"""
    print_header("MONTE CARLO SIMULATION DEMO")
    
    lootbox = create_example_lootbox()
    simulator = MonteCarloSimulator(seed=42)  # Reproducible results
    
    print(f"Running 50,000 simulations of '{lootbox.name}'...")
    result = simulator.simulate_multiple_openings(lootbox, 50000, show_progress=True)
    
    print(f"\nSimulation Results:")
    print(f"Total Simulations: {result.num_simulations:,}")
    print(f"Total Cost: ${result.total_cost:.2f}")
    print(f"Total Value Received: ${result.total_value_received:.2f}")
    print(f"Average Value per Box: ${result.average_value_per_box:.4f}")
    print(f"Median Value per Box: ${result.median_value_per_box:.4f}")
    print(f"Standard Deviation: ${result.std_deviation:.4f}")
    print(f"ROI: {result.get_roi():.2f}%")
    print(f"Actual House Edge: {result.house_edge_actual*100:.2f}%")
    print(f"Theoretical House Edge: {result.house_edge_theoretical*100:.2f}%")
    
    print(f"\nRarity Distribution:")
    for rarity, count in result.rarity_distribution.items():
        percentage = (count / result.num_simulations) * 100
        print(f"  {rarity.title()}: {count:,} ({percentage:.2f}%)")

def demo_optimization():
    """Demonstrate probability optimization"""
    print_header("OPTIMIZATION DEMO")
    
    lootbox = create_example_lootbox()
    optimizer = ProbabilityOptimizer()
    
    print(f"Original Lootbox: {lootbox.name}")
    print(f"Original House Edge: {lootbox.get_house_edge()*100:.2f}%")
    print(f"Original Expected Value: ${lootbox.get_expected_value():.4f}")
    
    # Optimize for 10% house edge
    target_house_edge = 0.10
    print(f"\nOptimizing for {target_house_edge*100:.1f}% house edge...")
    
    result = optimizer.optimize_for_house_edge(lootbox, target_house_edge)
    
    if result.success:
        print(f"\nOptimization successful!")
        print(f"Optimized House Edge: {result.optimized_house_edge*100:.2f}%")
        print(f"Optimized Expected Value: ${result.optimized_expected_value:.4f}")
        print(f"Iterations: {result.iterations}")
        
        # Show probability changes
        print(f"\nProbability Changes:")
        for orig, opt in zip(lootbox.items, result.optimized_lootbox.items):
            change = opt.probability - orig.probability
            sign = "+" if change >= 0 else ""
            print(f"  {orig.name}: {orig.probability*100:.4f}% → {opt.probability*100:.4f}% ({sign}{change*100:.4f}%)")
    else:
        print(f"Optimization failed: {result.optimization_message}")

def demo_cost_range_analysis():
    """Demonstrate cost range analysis"""
    print_header("COST RANGE ANALYSIS DEMO")
    
    # Create item set for analysis
    items = [
        LootboxItem(name="Basic Item", value=0.20, rarity=RarityTier.COMMON, probability=0.6),
        LootboxItem(name="Good Item", value=1.00, rarity=RarityTier.UNCOMMON, probability=0.25),
        LootboxItem(name="Great Item", value=4.00, rarity=RarityTier.RARE, probability=0.10),
        LootboxItem(name="Amazing Item", value=15.00, rarity=RarityTier.EPIC, probability=0.04),
        LootboxItem(name="Legendary Item", value=50.00, rarity=RarityTier.LEGENDARY, probability=0.01)
    ]
    
    optimizer = ProbabilityOptimizer()
    
    print("Analyzing optimal configurations across $0.50-$4.00 cost range...")
    print("Target house edge: 15%")
    
    results = optimizer.optimize_for_cost_range(
        items, 
        min_cost=0.5, 
        max_cost=4.0, 
        target_house_edge=0.15
    )
    
    print(f"\nCost Range Analysis Results:")
    print(f"{'Cost':<8} {'Expected Value':<15} {'House Edge':<12} {'Feasible':<10}")
    print("-" * 50)
    
    for result in results:
        if result.success and result.optimized_lootbox:
            lootbox = result.optimized_lootbox
            feasible = "Yes" if abs(result.optimized_house_edge - 0.15) < 0.02 else "No"
            print(f"${lootbox.cost:<7.2f} ${lootbox.get_expected_value():<14.4f} {lootbox.get_house_edge()*100:<11.2f}% {feasible:<10}")

def demo_templates():
    """Demonstrate predefined templates"""
    print_header("TEMPLATE DEMO")
    
    calculator = ExpectedValueCalculator()
    
    # CS:GO style template
    csgo_items = [
        LootboxItem(name="Consumer Grade", value=0.05, rarity=RarityTier.COMMON, probability=0.7992),
        LootboxItem(name="Industrial Grade", value=0.15, rarity=RarityTier.UNCOMMON, probability=0.1598),
        LootboxItem(name="Mil-Spec", value=0.75, rarity=RarityTier.RARE, probability=0.032),
        LootboxItem(name="Restricted", value=3.50, rarity=RarityTier.EPIC, probability=0.0064),
        LootboxItem(name="Classified", value=15.00, rarity=RarityTier.LEGENDARY, probability=0.0013),
        LootboxItem(name="Covert", value=75.00, rarity=RarityTier.MYTHIC, probability=0.0013)
    ]
    
    csgo_box = Lootbox(
        name="CS:GO Style Case",
        description="Inspired by CS:GO weapon case odds",
        cost=2.50,
        items=csgo_items
    )
    
    analytics = calculator.generate_full_analysis(csgo_box)
    
    print(f"Template: {csgo_box.name}")
    print(f"Cost: ${csgo_box.cost:.2f}")
    print(f"Expected Value: ${analytics.expected_value:.4f}")
    print(f"House Edge: {analytics.house_edge*100:.2f}%")
    print(f"Risk Level: {analytics.get_risk_level()}")
    print(f"Player Rating: {analytics.get_player_value_rating()}")

def main():
    """Run all demonstrations"""
    print("🎲 Lootbox Probability Toolkit Demo")
    print("=" * 60)
    
    try:
        demo_basic_analysis()
        demo_monte_carlo_simulation()
        demo_optimization()
        demo_cost_range_analysis()
        demo_templates()
        
        print_header("DEMO COMPLETE")
        print("✓ All demonstrations completed successfully!")
        print("\nTo use the toolkit interactively, run:")
        print("  python3 src/cli/main.py --help")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
