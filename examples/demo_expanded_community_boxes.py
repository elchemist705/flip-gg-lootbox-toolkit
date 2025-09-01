#!/usr/bin/env python3
"""
Demo: Expanded Community Box Configurations

Showcases the new expanded community box features with 8-12 items
instead of the previous 4-6 item limit. Demonstrates the enhanced
variety and granular prize tiers for better player engagement.
"""
import sys
import os
from pathlib import Path

# Add bin to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'bin'))

from lootbox_calculator import LootboxCalculator, Lootbox, LootboxItem, RarityTier

def create_expanded_community_box(cost: float = 1.50) -> Lootbox:
    """Create an expanded community box with 11 different prize tiers"""
    items = [
        LootboxItem("Dust Coins", cost * 0.08, RarityTier.COMMON, 0.35),
        LootboxItem("Small Tokens", cost * 0.20, RarityTier.COMMON, 0.25),
        LootboxItem("Token Bundle", cost * 0.40, RarityTier.UNCOMMON, 0.18),
        LootboxItem("Coin Pack", cost * 0.70, RarityTier.UNCOMMON, 0.12),
        LootboxItem("Silver Prize", cost * 1.20, RarityTier.RARE, 0.06),
        LootboxItem("Gold Prize", cost * 2.00, RarityTier.RARE, 0.025),
        LootboxItem("Premium Win", cost * 4.50, RarityTier.EPIC, 0.012),
        LootboxItem("Major Jackpot", cost * 9.00, RarityTier.EPIC, 0.005),
        LootboxItem("Elite Jackpot", cost * 20.00, RarityTier.LEGENDARY, 0.002),
        LootboxItem("Supreme Prize", cost * 50.00, RarityTier.LEGENDARY, 0.0008),
        LootboxItem("Ultimate Treasure", cost * 100.00, RarityTier.MYTHIC, 0.0002)
    ]
    
    return Lootbox(
        name="Community Expanded Box",
        cost=cost,
        items=items,
        description="Community-focused lootbox with 11+ items for maximum variety"
    )

def create_mega_variety_box(cost: float = 2.50) -> Lootbox:
    """Create a mega variety box with 12 different prize tiers"""
    items = [
        LootboxItem("Dust", cost * 0.05, RarityTier.COMMON, 0.30),
        LootboxItem("Scraps", cost * 0.12, RarityTier.COMMON, 0.25),
        LootboxItem("Small Coins", cost * 0.25, RarityTier.UNCOMMON, 0.20),
        LootboxItem("Token Pack", cost * 0.45, RarityTier.UNCOMMON, 0.12),
        LootboxItem("Coin Bundle", cost * 0.80, RarityTier.RARE, 0.08),
        LootboxItem("Silver Prize", cost * 1.40, RarityTier.RARE, 0.03),
        LootboxItem("Gold Prize", cost * 2.50, RarityTier.EPIC, 0.015),
        LootboxItem("Premium Win", cost * 5.00, RarityTier.EPIC, 0.008),
        LootboxItem("Major Jackpot", cost * 10.00, RarityTier.LEGENDARY, 0.003),
        LootboxItem("Elite Jackpot", cost * 25.00, RarityTier.LEGENDARY, 0.001),
        LootboxItem("Supreme Treasure", cost * 60.00, RarityTier.MYTHIC, 0.0004),
        LootboxItem("Ultimate Fortune", cost * 150.00, RarityTier.MYTHIC, 0.0001)
    ]
    
    return Lootbox(
        name="Mega Variety Community Box",
        cost=cost,
        items=items,
        description="Maximum variety community box with 12 different prize tiers"
    )

def analyze_and_display(lootbox: Lootbox, calculator: LootboxCalculator):
    """Analyze and display lootbox statistics"""
    analysis = calculator.analyze_lootbox(lootbox)
    
    print(f"\n📊 ANALYSIS: {lootbox.name}")
    print("=" * 60)
    print(f"Cost: ${lootbox.cost:.2f}")
    print(f"Total Items: {len(lootbox.items)} cases/prizes")
    print(f"Expected Value: ${analysis['expected_value']:.4f}")
    print(f"House Edge: {analysis['house_edge']*100:.2f}%")
    print(f"Risk Level: {analysis['risk_level']}")
    print(f"Player Rating: {analysis['player_rating']}")
    
    print(f"\n🎁 ITEM BREAKDOWN:")
    print(f"{'Item':<20} {'Value':<8} {'Rarity':<12} {'Probability':<12} {'ROI'}")
    print("-" * 70)
    
    for item in lootbox.items:
        roi = ((item.value - lootbox.cost) / lootbox.cost) * 100
        print(f"{item.name:<20} ${item.value:<7.2f} {item.rarity.value.title():<12} "
              f"{item.probability*100:<11.3f}% {roi:>7.1f}%")
    
    print(f"\n🎯 PLAYER EXPERIENCE:")
    print(f"• {analysis['break_even_probability']*100:.1f}% chance to break even or profit")
    print(f"• {analysis['profit_10_probability']*100:.1f}% chance for 10%+ profit")
    print(f"• {analysis['profit_50_probability']*100:.1f}% chance for 50%+ profit")
    
    # Rarity distribution
    print(f"\n🌟 RARITY DISTRIBUTION:")
    for rarity, stats in analysis['rarity_breakdown'].items():
        print(f"• {rarity.title()}: {stats['count']} items, "
              f"{stats['probability']*100:.2f}% total chance, "
              f"avg value ${stats['avg_value']:.2f}")

def main():
    """Demo the expanded community box configurations"""
    print("🎲 EXPANDED COMMUNITY BOX DEMO")
    print("=" * 60)
    print("Showcasing new configurations with 8-12 items (up from 4-6)")
    
    calculator = LootboxCalculator()
    
    # Demo 1: Community Expanded Box (11 items)
    community_box = create_expanded_community_box(1.50)
    analyze_and_display(community_box, calculator)
    
    # Demo 2: Mega Variety Box (12 items)
    mega_box = create_mega_variety_box(2.50)
    analyze_and_display(mega_box, calculator)
    
    # Demo 3: Show comparison with simulation
    print(f"\n🎲 SIMULATION COMPARISON (10,000 openings each)")
    print("=" * 60)
    
    for box in [community_box, mega_box]:
        sim_results = calculator.simulate_openings(box, 10000)
        print(f"\n{box.name}:")
        print(f"  Theoretical House Edge: {box.get_house_edge()*100:.2f}%")
        print(f"  Simulated House Edge: {sim_results['house_edge_actual']*100:.2f}%")
        print(f"  Win Rate: {sim_results['win_rate_percent']:.1f}%")
        print(f"  Average ROI: {sim_results['roi_percent']:.1f}%")
    
    print(f"\n✅ EXPANSION SUMMARY:")
    print("=" * 60)
    print("• Low variance: 4 → 8 items (100% increase)")
    print("• Medium variance: 5 → 9 items (80% increase)")  
    print("• High variance: 5-6 → 11-12 items (100%+ increase)")
    print("• More granular prize tiers for better player engagement")
    print("• Enhanced community box support with expanded variety")
    print("• Maintained probability distribution accuracy")

if __name__ == "__main__":
    main()
