#!/usr/bin/env python3
"""
Flip.gg Lootbox Toolkit - Expanded Range Demonstration

This demo showcases the updated toolkit supporting:
- Cost range: $0.50 - $1000.00
- Item values: Up to $1000.00
- Optimized probability distributions across all tiers
"""
import sys
sys.path.append('bin')
from lootbox_calculator import LootboxCalculator, Lootbox, LootboxItem, RarityTier
import json

def main():
    print("🎲 FLIP.GG LOOTBOX TOOLKIT - EXPANDED RANGE DEMO")
    print("Cost Range: $0.50 - $1000.00 | Item Values: Up to $1000.00")
    print("=" * 80)
    
    calculator = LootboxCalculator()
    
    # Test various cost points across the full range
    test_scenarios = [
        {"cost": 0.75, "tier": "Budget", "description": "Entry-level lootbox"},
        {"cost": 5.00, "tier": "Standard", "description": "Regular player lootbox"},
        {"cost": 25.00, "tier": "Premium", "description": "Premium player lootbox"},
        {"cost": 100.00, "tier": "Whale", "description": "High-roller lootbox"},
        {"cost": 500.00, "tier": "Elite", "description": "Elite player lootbox"},
        {"cost": 1000.00, "tier": "Supreme", "description": "Ultimate luxury lootbox"}
    ]
    
    print("\n🚀 COMPREHENSIVE COST RANGE ANALYSIS")
    print("=" * 80)
    print(f"{'Tier':<10} {'Cost':<8} {'Expected Value':<15} {'House Edge':<12} {'Max Item':<12} {'Rating'}")
    print("-" * 80)
    
    all_lootboxes = []
    
    for scenario in test_scenarios:
        cost = scenario["cost"]
        
        # Create optimized lootbox for this cost
        lootbox = create_advanced_lootbox(cost, scenario["tier"])
        
        # Optimize for reasonable house edge
        target_house_edge = 0.15 if cost >= 10 else 0.20  # Better rates for high-value boxes
        optimized_lootbox = calculator.optimize_probabilities(lootbox, target_house_edge)
        
        # Analyze
        analysis = calculator.analyze_lootbox(optimized_lootbox)
        
        # Find max item value
        max_item_value = max(item.value for item in optimized_lootbox.items)
        
        print(f"{scenario['tier']:<10} ${cost:<7.2f} "
              f"${analysis['expected_value']:<14.2f} "
              f"{analysis['house_edge']*100:<11.1f}% "
              f"${max_item_value:<11.2f} "
              f"{analysis['player_rating']}")
        
        all_lootboxes.append((scenario, optimized_lootbox, analysis))
    
    # Detailed analysis for a few key examples
    key_examples = [all_lootboxes[0], all_lootboxes[3], all_lootboxes[5]]  # Budget, Whale, Supreme
    
    for scenario_data, lootbox, analysis in key_examples:
        print(f"\n🎯 DETAILED ANALYSIS: {scenario_data['tier']} Tier (${lootbox.cost:.2f})")
        print("=" * 70)
        
        print(f"📊 METRICS:")
        print(f"  • Expected Value: ${analysis['expected_value']:.2f}")
        print(f"  • House Edge: {analysis['house_edge']*100:.1f}%")
        print(f"  • Player Rating: {analysis['player_rating']}")
        print(f"  • Risk Level: {analysis['risk_level']}")
        print(f"  • Break-even Chance: {analysis['break_even_probability']*100:.1f}%")
        
        print(f"\n🎁 TOP 3 VALUABLE ITEMS:")
        sorted_items = sorted(lootbox.items, key=lambda x: x.value, reverse=True)[:3]
        for i, item in enumerate(sorted_items, 1):
            roi = ((item.value - lootbox.cost) / lootbox.cost) * 100
            print(f"  {i}. {item.name}: ${item.value:.2f} ({item.probability*100:.3f}% chance, {roi:+.0f}% ROI)")
        
        # Quick simulation
        sim_results = calculator.simulate_openings(lootbox, 5000)
        print(f"\n🎲 SIMULATION (5,000 runs): {sim_results['win_rate_percent']:.1f}% win rate, "
              f"{sim_results['house_edge_actual']*100:.1f}% actual house edge")
        
        # Save configuration
        filename = f"demo_{scenario_data['tier'].lower()}_{lootbox.cost:.0f}.json"
        config_dict = {
            "name": lootbox.name,
            "description": lootbox.description,
            "cost": lootbox.cost,
            "items": [
                {
                    "name": item.name,
                    "value": item.value,
                    "rarity": item.rarity.value,
                    "probability": item.probability,
                    "description": item.description
                }
                for item in lootbox.items
            ]
        }
        
        with open(filename, "w") as f:
            json.dump(config_dict, f, indent=2)
        print(f"  💾 Saved to: {filename}")
    
    print(f"\n🎯 SUMMARY OF CAPABILITIES")
    print("=" * 50)
    print(f"✅ Cost Range: $0.50 to $1000.00 (2000x span)")
    print(f"✅ Item Values: $0.02 to $1000.00 (50,000x span)")
    print(f"✅ Smart scaling for different cost tiers")
    print(f"✅ Mathematical optimization across all ranges")
    print(f"✅ Validation through Monte Carlo simulation")
    print(f"✅ Professional probability distributions")
    
    print(f"\n🚀 READY FOR FLIP.GG IMPLEMENTATION!")
    print(f"Your toolkit now supports everything from micro-transactions")
    print(f"to ultra-premium luxury lootboxes with mathematically")
    print(f"optimized probability distributions!")

def create_advanced_lootbox(cost: float, tier: str) -> Lootbox:
    """Create sophisticated lootbox configurations based on cost tier"""
    
    if cost <= 2.0:  # Budget tier
        items = [
            LootboxItem("Coins", cost * 0.20, RarityTier.COMMON, 0.60),
            LootboxItem("Tokens", cost * 0.50, RarityTier.UNCOMMON, 0.25),
            LootboxItem("Small Prize", cost * 1.20, RarityTier.RARE, 0.12),
            LootboxItem("Good Win", cost * 4.00, RarityTier.EPIC, 0.025),
            LootboxItem("Jackpot", min(cost * 15.00, 50.0), RarityTier.LEGENDARY, 0.005)
        ]
    elif cost <= 10.0:  # Standard tier
        items = [
            LootboxItem("Basic Reward", cost * 0.15, RarityTier.COMMON, 0.55),
            LootboxItem("Decent Prize", cost * 0.40, RarityTier.UNCOMMON, 0.25),
            LootboxItem("Good Prize", cost * 0.90, RarityTier.RARE, 0.15),
            LootboxItem("Great Prize", cost * 3.50, RarityTier.EPIC, 0.04),
            LootboxItem("Amazing Prize", min(cost * 12.00, 200.0), RarityTier.LEGENDARY, 0.01)
        ]
    elif cost <= 50.0:  # Premium tier
        items = [
            LootboxItem("Token Drop", cost * 0.10, RarityTier.COMMON, 0.50),
            LootboxItem("Small Win", cost * 0.35, RarityTier.UNCOMMON, 0.28),
            LootboxItem("Medium Win", cost * 0.85, RarityTier.RARE, 0.15),
            LootboxItem("Big Win", cost * 2.50, RarityTier.EPIC, 0.06),
            LootboxItem("Huge Win", min(cost * 8.00, 500.0), RarityTier.LEGENDARY, 0.01)
        ]
    elif cost <= 200.0:  # Whale tier
        items = [
            LootboxItem("Base Token", cost * 0.08, RarityTier.COMMON, 0.65),
            LootboxItem("Small Prize", cost * 0.25, RarityTier.UNCOMMON, 0.20),
            LootboxItem("Good Win", cost * 0.70, RarityTier.RARE, 0.10),
            LootboxItem("Major Win", cost * 2.00, RarityTier.EPIC, 0.04),
            LootboxItem("Epic Win", cost * 6.00, RarityTier.LEGENDARY, 0.008),
            LootboxItem("Ultimate Prize", min(cost * 20.00, 1000.0), RarityTier.MYTHIC, 0.002)
        ]
    else:  # Elite/Supreme tier
        items = [
            LootboxItem("Participation", cost * 0.05, RarityTier.COMMON, 0.75),
            LootboxItem("Minor Prize", cost * 0.20, RarityTier.UNCOMMON, 0.18),
            LootboxItem("Decent Prize", cost * 0.50, RarityTier.RARE, 0.05),
            LootboxItem("Premium Prize", cost * 1.50, RarityTier.EPIC, 0.015),
            LootboxItem("Elite Prize", cost * 4.00, RarityTier.LEGENDARY, 0.004),
            LootboxItem("Supreme Treasure", min(cost * 12.00, 1000.0), RarityTier.MYTHIC, 0.001)
        ]
    
    return Lootbox(
        name=f"{tier} Flip.gg Box ${cost:.2f}",
        cost=cost,
        items=items,
        description=f"{tier} tier lootbox optimized for flip.gg"
    )

if __name__ == "__main__":
    main()
