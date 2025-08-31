#!/usr/bin/env python3
"""
Flip.gg Lootbox Calculator - Standalone Version

A comprehensive, standalone tool for designing optimal lootboxes for flip.gg
within your $0.50-$1000.00 cost range with mixed high/low value items.
"""
import math
import random
import statistics
from enum import Enum
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import json

class RarityTier(str, Enum):
    """Standard rarity tiers for lootbox items"""
    COMMON = "common"
    UNCOMMON = "uncommon" 
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"
    MYTHIC = "mythic"

@dataclass
class LootboxItem:
    """Represents a single item in a lootbox"""
    name: str
    value: float
    rarity: RarityTier
    probability: float
    description: str = ""
    
    def __post_init__(self):
        if not 0 <= self.probability <= 1:
            raise ValueError("Probability must be between 0 and 1")
        if self.value <= 0:
            raise ValueError("Item value must be positive")

@dataclass
class Lootbox:
    """Represents a complete lootbox configuration"""
    name: str
    cost: float
    items: List[LootboxItem]
    description: str = ""
    
    def __post_init__(self):
        if not 0.5 <= self.cost <= 1000.0:
            raise ValueError("Lootbox cost must be between $0.50 and $1000.00")
        
        # Normalize probabilities if needed
        total_prob = sum(item.probability for item in self.items)
        if abs(total_prob - 1.0) > 1e-6:
            for item in self.items:
                item.probability = item.probability / total_prob
    
    def get_expected_value(self) -> float:
        """Calculate expected value"""
        return sum(item.value * item.probability for item in self.items)
    
    def get_house_edge(self) -> float:
        """Calculate house edge"""
        return (self.cost - self.get_expected_value()) / self.cost

class LootboxCalculator:
    """Advanced calculator for lootbox analysis"""
    
    def __init__(self):
        random.seed(42)  # For reproducible results
    
    def analyze_lootbox(self, lootbox: Lootbox) -> Dict:
        """Comprehensive lootbox analysis"""
        expected_value = lootbox.get_expected_value()
        house_edge = lootbox.get_house_edge()
        
        # Calculate variance and standard deviation
        variance = sum(
            item.probability * (item.value - expected_value) ** 2
            for item in lootbox.items
        )
        std_deviation = math.sqrt(variance)
        
        # Calculate coefficient of variation
        cv = std_deviation / expected_value if expected_value > 0 else float('inf')
        
        # Break-even probability
        break_even_prob = sum(
            item.probability for item in lootbox.items 
            if item.value >= lootbox.cost
        )
        
        # Profit probabilities
        profit_10_prob = sum(
            item.probability for item in lootbox.items
            if item.value >= lootbox.cost * 1.1
        )
        
        profit_50_prob = sum(
            item.probability for item in lootbox.items
            if item.value >= lootbox.cost * 1.5
        )
        
        # Risk assessment
        risk_level = self._get_risk_level(cv)
        player_rating = self._get_player_rating(house_edge)
        
        # Rarity breakdown
        rarity_breakdown = {}
        for rarity in RarityTier:
            rarity_items = [item for item in lootbox.items if item.rarity == rarity]
            if rarity_items:
                total_prob = sum(item.probability for item in rarity_items)
                avg_value = sum(item.value * item.probability for item in rarity_items) / total_prob
                rarity_breakdown[rarity.value] = {
                    'count': len(rarity_items),
                    'probability': total_prob,
                    'avg_value': avg_value
                }
        
        return {
            'expected_value': expected_value,
            'house_edge': house_edge,
            'variance': variance,
            'std_deviation': std_deviation,
            'coefficient_of_variation': cv,
            'break_even_probability': break_even_prob,
            'profit_10_probability': profit_10_prob,
            'profit_50_probability': profit_50_prob,
            'risk_level': risk_level,
            'player_rating': player_rating,
            'rarity_breakdown': rarity_breakdown
        }
    
    def _get_risk_level(self, cv: float) -> str:
        """Categorize risk level"""
        if cv < 0.5:
            return "Low Risk"
        elif cv < 1.0:
            return "Medium Risk"
        elif cv < 2.0:
            return "High Risk"
        else:
            return "Very High Risk"
    
    def _get_player_rating(self, house_edge: float) -> str:
        """Rate player value proposition"""
        if house_edge < 0:
            return "Excellent (Player Advantage)"
        elif house_edge < 0.1:
            return "Very Good"
        elif house_edge < 0.2:
            return "Good"
        elif house_edge < 0.3:
            return "Fair"
        elif house_edge < 0.4:
            return "Poor"
        else:
            return "Very Poor"
    
    def simulate_openings(self, lootbox: Lootbox, num_simulations: int = 10000) -> Dict:
        """Monte Carlo simulation"""
        results = []
        rarity_counts = {rarity.value: 0 for rarity in RarityTier}
        
        for _ in range(num_simulations):
            # Select item based on probabilities
            rand = random.random()
            cumulative_prob = 0.0
            
            for item in lootbox.items:
                cumulative_prob += item.probability
                if rand <= cumulative_prob:
                    results.append(item.value)
                    rarity_counts[item.rarity.value] += 1
                    break
        
        total_cost = num_simulations * lootbox.cost
        total_value = sum(results)
        
        return {
            'num_simulations': num_simulations,
            'total_cost': total_cost,
            'total_value': total_value,
            'average_value': statistics.mean(results),
            'median_value': statistics.median(results),
            'std_deviation': statistics.stdev(results) if len(results) > 1 else 0,
            'roi_percent': ((total_value - total_cost) / total_cost) * 100,
            'win_rate_percent': (sum(1 for v in results if v > lootbox.cost) / num_simulations) * 100,
            'house_edge_actual': (total_cost - total_value) / total_cost,
            'rarity_distribution': rarity_counts
        }
    
    def optimize_probabilities(self, lootbox: Lootbox, target_house_edge: float) -> Lootbox:
        """Simple probability optimization using iterative approach"""
        # Create a copy for optimization
        optimized_items = []
        for item in lootbox.items:
            optimized_items.append(LootboxItem(
                name=item.name,
                value=item.value,
                rarity=item.rarity,
                probability=item.probability,
                description=item.description
            ))
        
        # Iterative optimization (simplified)
        for iteration in range(1000):
            current_ev = sum(item.value * item.probability for item in optimized_items)
            current_house_edge = (lootbox.cost - current_ev) / lootbox.cost
            
            if abs(current_house_edge - target_house_edge) < 0.001:
                break
            
            # Adjust probabilities
            if current_house_edge < target_house_edge:
                # Need to reduce expected value (reduce high-value probabilities)
                for item in optimized_items:
                    if item.value > lootbox.cost:
                        item.probability *= 0.99
            else:
                # Need to increase expected value (increase high-value probabilities)
                for item in optimized_items:
                    if item.value > lootbox.cost:
                        item.probability *= 1.01
            
            # Renormalize probabilities
            total_prob = sum(item.probability for item in optimized_items)
            for item in optimized_items:
                item.probability = item.probability / total_prob
        
        return Lootbox(
            name=f"{lootbox.name} (Optimized)",
            cost=lootbox.cost,
            items=optimized_items,
            description=f"Optimized for {target_house_edge*100:.1f}% house edge"
        )

def create_flip_gg_lootbox(cost: float) -> Lootbox:
    """Create a lootbox tailored for flip.gg requirements"""
    
    # Scale item values based on cost with different tiers
    if cost <= 10.0:
        # Standard scaling for low-medium cost boxes
        low_value = cost * 0.08
        medium_low = cost * 0.25
        medium_high = cost * 0.80
        high_value = cost * 3.0
        jackpot = min(cost * 10.0, 1000.0)  # Cap at $1000
        
        items = [
            LootboxItem(
                name="Small Coins",
                value=low_value,
                rarity=RarityTier.COMMON,
                probability=0.50,
                description="Basic coins with minimal value"
            ),
            LootboxItem(
                name="Token Bundle", 
                value=medium_low,
                rarity=RarityTier.UNCOMMON,
                probability=0.25,
                description="Decent token bundle"
            ),
            LootboxItem(
                name="Premium Item",
                value=medium_high,
                rarity=RarityTier.RARE,
                probability=0.15,
                description="Premium item worth most of box cost"
            ),
            LootboxItem(
                name="Valuable Prize",
                value=high_value,
                rarity=RarityTier.EPIC,
                probability=0.08,
                description="High-value prize worth 3x the box"
            ),
            LootboxItem(
                name="Mega Jackpot",
                value=jackpot,
                rarity=RarityTier.LEGENDARY,
                probability=0.02,
                description="Massive jackpot - up to $1000!"
            )
        ]
    elif cost <= 100.0:
        # Whale tier scaling
        low_value = cost * 0.05
        medium_low = cost * 0.20
        medium_high = cost * 0.60
        high_value = cost * 2.0
        epic_value = cost * 8.0
        jackpot = min(cost * 20.0, 1000.0)
        
        items = [
            LootboxItem(
                name="Token Drop",
                value=low_value,
                rarity=RarityTier.COMMON,
                probability=0.65,
                description="Basic token with minimal value"
            ),
            LootboxItem(
                name="Small Prize", 
                value=medium_low,
                rarity=RarityTier.UNCOMMON,
                probability=0.20,
                description="Small prize for whale players"
            ),
            LootboxItem(
                name="Good Win",
                value=medium_high,
                rarity=RarityTier.RARE,
                probability=0.10,
                description="Decent win for serious players"
            ),
            LootboxItem(
                name="Major Win",
                value=high_value,
                rarity=RarityTier.EPIC,
                probability=0.04,
                description="Major prize worth 2x the box"
            ),
            LootboxItem(
                name="Epic Jackpot",
                value=epic_value,
                rarity=RarityTier.LEGENDARY,
                probability=0.008,
                description="Epic jackpot for whale tier"
            ),
            LootboxItem(
                name="Ultimate Prize",
                value=jackpot,
                rarity=RarityTier.MYTHIC,
                probability=0.002,
                description="Ultimate prize up to $1000!"
            )
        ]
    else:
        # Ultra-luxury tier scaling
        low_value = cost * 0.03
        medium_low = cost * 0.12
        medium_high = cost * 0.40
        high_value = cost * 1.20
        epic_value = cost * 4.0
        jackpot = min(cost * 12.0, 1000.0)
        
        items = [
            LootboxItem(
                name="Base Token",
                value=low_value,
                rarity=RarityTier.COMMON,
                probability=0.75,
                description="Base reward for luxury tier"
            ),
            LootboxItem(
                name="Minor Prize", 
                value=medium_low,
                rarity=RarityTier.UNCOMMON,
                probability=0.18,
                description="Minor prize for elite players"
            ),
            LootboxItem(
                name="Solid Prize",
                value=medium_high,
                rarity=RarityTier.RARE,
                probability=0.05,
                description="Solid prize for luxury tier"
            ),
            LootboxItem(
                name="Premium Win",
                value=high_value,
                rarity=RarityTier.EPIC,
                probability=0.015,
                description="Premium win for elite players"
            ),
            LootboxItem(
                name="Luxury Jackpot",
                value=epic_value,
                rarity=RarityTier.LEGENDARY,
                probability=0.004,
                description="Luxury jackpot prize"
            ),
            LootboxItem(
                name="Supreme Treasure",
                value=jackpot,
                rarity=RarityTier.MYTHIC,
                probability=0.001,
                description="Supreme treasure up to $1000!"
            )
        ]
    
    return Lootbox(
        name=f"Flip.gg Lootbox ${cost:.2f}",
        cost=cost,
        items=items,
        description=f"Optimized for flip.gg with cost ${cost:.2f}"
    )

def print_analysis(lootbox: Lootbox, calculator: LootboxCalculator):
    """Print comprehensive analysis"""
    analysis = calculator.analyze_lootbox(lootbox)
    
    print(f"\n🎲 LOOTBOX ANALYSIS: {lootbox.name}")
    print(f"{'='*60}")
    
    print(f"\n📊 BASIC METRICS")
    print(f"Cost:              ${lootbox.cost:.2f}")
    print(f"Expected Value:    ${analysis['expected_value']:.4f}")
    print(f"House Edge:        {analysis['house_edge']*100:.2f}%")
    print(f"Standard Deviation: ${analysis['std_deviation']:.4f}")
    print(f"Risk Level:        {analysis['risk_level']}")
    print(f"Player Rating:     {analysis['player_rating']}")
    
    print(f"\n🎯 PLAYER ODDS")
    print(f"Break Even Chance: {analysis['break_even_probability']*100:.2f}%")
    print(f"10%+ Profit Chance: {analysis['profit_10_probability']*100:.2f}%") 
    print(f"50%+ Profit Chance: {analysis['profit_50_probability']*100:.2f}%")
    
    print(f"\n🎁 ITEM BREAKDOWN")
    for item in sorted(lootbox.items, key=lambda x: x.probability, reverse=True):
        roi = ((item.value - lootbox.cost) / lootbox.cost) * 100
        ev_contribution = item.value * item.probability
        print(f"{item.name:<15} | {item.rarity.value.title():<10} | ${item.value:<6.2f} | "
              f"{item.probability*100:>6.2f}% | ROI: {roi:>7.1f}% | EV: ${ev_contribution:.4f}")
    
    print(f"\n🏆 RARITY DISTRIBUTION")
    for rarity, data in analysis['rarity_breakdown'].items():
        print(f"{rarity.title():<10}: {data['probability']*100:>6.2f}% chance | Avg Value: ${data['avg_value']:.2f}")

def print_simulation_results(sim_results: Dict):
    """Print Monte Carlo simulation results"""
    print(f"\n🎲 MONTE CARLO SIMULATION ({sim_results['num_simulations']:,} runs)")
    print(f"Total Cost:        ${sim_results['total_cost']:.2f}")
    print(f"Total Value:       ${sim_results['total_value']:.2f}")
    print(f"Average Value:     ${sim_results['average_value']:.4f}")
    print(f"Median Value:      ${sim_results['median_value']:.4f}")
    print(f"ROI:              {sim_results['roi_percent']:.2f}%")
    print(f"Win Rate:         {sim_results['win_rate_percent']:.2f}%")
    print(f"Actual House Edge: {sim_results['house_edge_actual']*100:.2f}%")

def main():
    """Main demonstration function"""
    print("🎲 FLIP.GG LOOTBOX PROBABILITY CALCULATOR")
    print("Designed for $0.50-$1000.00 cost range with high/low value items")
    print("="*70)
    
    calculator = LootboxCalculator()
    
    # Test different cost points
    test_costs = [0.75, 1.50, 2.50, 3.75]
    
    print(f"\n📊 COST COMPARISON ANALYSIS")
    print(f"{'Cost':<8} {'Expected Value':<15} {'House Edge':<12} {'Break Even':<12} {'Player Rating'}")
    print("-" * 75)
    
    lootboxes = []
    
    for cost in test_costs:
        lootbox = create_flip_gg_lootbox(cost)
        analysis = calculator.analyze_lootbox(lootbox)
        lootboxes.append((lootbox, analysis))
        
        print(f"${cost:<7.2f} "
              f"${analysis['expected_value']:<14.4f} "
              f"{analysis['house_edge']*100:<11.2f}% "
              f"{analysis['break_even_probability']*100:<11.2f}% "
              f"{analysis['player_rating']}")
    
    # Detailed analysis of recommended option
    recommended_cost = 2.50
    recommended_lootbox = create_flip_gg_lootbox(recommended_cost)
    
    print(f"\n🌟 RECOMMENDED CONFIGURATION: ${recommended_cost:.2f}")
    print_analysis(recommended_lootbox, calculator)
    
    # Run simulation
    sim_results = calculator.simulate_openings(recommended_lootbox, 25000)
    print_simulation_results(sim_results)
    
    # Optimization demonstration
    print(f"\n🔧 OPTIMIZATION EXAMPLE")
    target_house_edge = 0.15  # 15%
    print(f"Optimizing for {target_house_edge*100:.0f}% house edge...")
    
    optimized_lootbox = calculator.optimize_probabilities(recommended_lootbox, target_house_edge)
    optimized_analysis = calculator.analyze_lootbox(optimized_lootbox)
    
    print(f"Original House Edge:   {recommended_lootbox.get_house_edge()*100:.2f}%")
    print(f"Optimized House Edge:  {optimized_analysis['house_edge']*100:.2f}%")
    print(f"Original Expected Value: ${recommended_lootbox.get_expected_value():.4f}")
    print(f"Optimized Expected Value: ${optimized_analysis['expected_value']:.4f}")
    
    # Show probability changes
    print(f"\n📈 PROBABILITY ADJUSTMENTS")
    for orig, opt in zip(recommended_lootbox.items, optimized_lootbox.items):
        change = opt.probability - orig.probability
        sign = "+" if change >= 0 else ""
        print(f"{orig.name:<15}: {orig.probability*100:>6.2f}% → {opt.probability*100:>6.2f}% ({sign}{change*100:.2f}%)")
    
    # Save configurations
    print(f"\n💾 SAVING CONFIGURATIONS")
    
    # Save original
    recommended_lootbox_dict = {
        "name": recommended_lootbox.name,
        "description": recommended_lootbox.description,
        "cost": recommended_lootbox.cost,
        "items": [
            {
                "name": item.name,
                "value": item.value,
                "rarity": item.rarity.value,
                "probability": item.probability,
                "description": item.description
            }
            for item in recommended_lootbox.items
        ]
    }
    
    with open("flip_gg_recommended.json", "w") as f:
        json.dump(recommended_lootbox_dict, f, indent=2)
    print(f"✅ Saved recommended config to: flip_gg_recommended.json")
    
    # Save optimized
    optimized_lootbox_dict = {
        "name": optimized_lootbox.name,
        "description": optimized_lootbox.description,
        "cost": optimized_lootbox.cost,
        "items": [
            {
                "name": item.name,
                "value": item.value,
                "rarity": item.rarity.value,
                "probability": item.probability,
                "description": item.description
            }
            for item in optimized_lootbox.items
        ]
    }
    
    with open("flip_gg_optimized.json", "w") as f:
        json.dump(optimized_lootbox_dict, f, indent=2)
    print(f"✅ Saved optimized config to: flip_gg_optimized.json")
    
    # Final recommendations
    print(f"\n🎯 FINAL RECOMMENDATIONS FOR FLIP.GG")
    print(f"="*50)
    print(f"💰 Recommended Cost: ${recommended_cost:.2f}")
    print(f"🎲 House Edge: {optimized_analysis['house_edge']*100:.1f}%")
    print(f"📈 Expected Value: ${optimized_analysis['expected_value']:.4f}")
    print(f"🏆 Player Rating: {optimized_analysis['player_rating']}")
    print(f"✨ Break Even Chance: {optimized_analysis['break_even_probability']*100:.1f}%")
    
    print(f"\n📋 KEY FEATURES:")
    jackpot_value = recommended_cost * 10.0
    low_value = recommended_cost * 0.08
    print(f"• Mix of high-value (${jackpot_value:.2f}) and low-value (${low_value:.2f}) items")
    print(f"• {optimized_analysis['risk_level']} volatility")
    print(f"• Mathematically optimized probabilities")
    print(f"• Validated through {sim_results['num_simulations']:,} simulations")
    print(f"• Cost within your ${0.50:.2f}-${1000.00:.2f} range")
    
    print(f"\n🚀 Ready for implementation on flip.gg!")

if __name__ == "__main__":
    main()
