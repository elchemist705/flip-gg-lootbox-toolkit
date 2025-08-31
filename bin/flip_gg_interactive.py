#!/usr/bin/env python3
"""
Interactive Flip.gg Lootbox Designer

Specifically designed for your requirements:
- Cost between $0.50 and $1000.00
- Mix of high cases (high-value items) and low cases (low-value items)
- Optimal probability distributions for profitability
"""
from lootbox_calculator import LootboxCalculator, Lootbox, LootboxItem, RarityTier
import json

def get_user_input():
    """Get user requirements for lootbox design"""
    print("🎲 FLIP.GG LOOTBOX DESIGNER")
    print("Let's create your optimal lootbox!")
    print("="*50)
    
    # Get cost
    while True:
        try:
            cost = float(input("\n💰 Enter lootbox cost ($0.50 - $1000.00): $"))
            if 0.5 <= cost <= 1000.0:
                break
            else:
                print("❌ Cost must be between $0.50 and $1000.00")
        except ValueError:
            print("❌ Please enter a valid number")
    
    # Get house edge preference
    print(f"\n🎯 Choose house edge strategy:")
    print(f"1. Conservative (10-15% house edge) - Better for players")
    print(f"2. Balanced (15-20% house edge) - Fair for both")
    print(f"3. Aggressive (20-30% house edge) - Higher profit")
    
    while True:
        strategy = input("Choose strategy (1-3): ").strip()
        if strategy == "1":
            house_edge = 0.12
            break
        elif strategy == "2":
            house_edge = 0.17
            break
        elif strategy == "3":
            house_edge = 0.25
            break
        else:
            print("❌ Please choose 1, 2, or 3")
    
    # Get variance preference
    print(f"\n🎢 Choose risk/variance level:")
    print(f"1. Low variance - Consistent, predictable outcomes")
    print(f"2. Medium variance - Balanced excitement")
    print(f"3. High variance - Big wins, big losses")
    
    while True:
        variance_choice = input("Choose variance (1-3): ").strip()
        if variance_choice in ["1", "2", "3"]:
            variance_level = int(variance_choice)
            break
        else:
            print("❌ Please choose 1, 2, or 3")
    
    return cost, house_edge, variance_level

def create_custom_lootbox(cost: float, house_edge: float, variance_level: int) -> Lootbox:
    """Create custom lootbox based on user preferences"""
    
    if variance_level == 1:  # Low variance
        # More consistent values, closer to cost
        items = [
            LootboxItem("Small Prize", cost * 0.30, RarityTier.COMMON, 0.40),
            LootboxItem("Medium Prize", cost * 0.70, RarityTier.UNCOMMON, 0.35),
            LootboxItem("Good Prize", cost * 1.20, RarityTier.RARE, 0.20),
            LootboxItem("Great Prize", cost * 2.50, RarityTier.EPIC, 0.05)
        ]
        description = "Low variance - consistent returns"
        
    elif variance_level == 2:  # Medium variance
        # Balanced distribution
        items = [
            LootboxItem("Basic Item", cost * 0.15, RarityTier.COMMON, 0.45),
            LootboxItem("Decent Item", cost * 0.45, RarityTier.UNCOMMON, 0.30),
            LootboxItem("Good Item", cost * 1.10, RarityTier.RARE, 0.18),
            LootboxItem("Excellent Item", cost * 4.00, RarityTier.EPIC, 0.06),
            LootboxItem("Legendary Item", cost * 12.00, RarityTier.LEGENDARY, 0.01)
        ]
        description = "Medium variance - balanced excitement"
        
    else:  # High variance
        # Extreme distribution with big jackpots - scale appropriately for cost
        if cost <= 10.0:
            # Standard scaling for low-medium cost boxes
            items = [
                LootboxItem("Almost Nothing", cost * 0.05, RarityTier.COMMON, 0.65),
                LootboxItem("Small Win", cost * 0.30, RarityTier.UNCOMMON, 0.20),
                LootboxItem("Decent Win", cost * 0.90, RarityTier.RARE, 0.10),
                LootboxItem("Big Win", cost * 5.00, RarityTier.EPIC, 0.04),
                LootboxItem("Mega Jackpot", cost * 25.00, RarityTier.LEGENDARY, 0.01)
            ]
        elif cost <= 100.0:
            # Medium-high cost scaling (whale tier)
            items = [
                LootboxItem("Token Drop", cost * 0.03, RarityTier.COMMON, 0.70),
                LootboxItem("Small Prize", cost * 0.15, RarityTier.UNCOMMON, 0.20),
                LootboxItem("Good Win", cost * 0.60, RarityTier.RARE, 0.08),
                LootboxItem("Major Win", cost * 2.50, RarityTier.EPIC, 0.015),
                LootboxItem("Huge Jackpot", cost * 10.00, RarityTier.LEGENDARY, 0.004),
                LootboxItem("Ultimate Prize", min(cost * 30.00, 1000.0), RarityTier.MYTHIC, 0.001)
            ]
        else:
            # Ultra-high cost scaling (luxury/elite tier)
            items = [
                LootboxItem("Base Token", cost * 0.02, RarityTier.COMMON, 0.80),
                LootboxItem("Minor Prize", cost * 0.08, RarityTier.UNCOMMON, 0.15),
                LootboxItem("Decent Prize", cost * 0.40, RarityTier.RARE, 0.04),
                LootboxItem("Big Prize", cost * 1.50, RarityTier.EPIC, 0.008),
                LootboxItem("Elite Jackpot", cost * 5.00, RarityTier.LEGENDARY, 0.0015),
                LootboxItem("Supreme Treasure", min(cost * 15.00, 1000.0), RarityTier.MYTHIC, 0.0005)
            ]
        description = "High variance - high risk, high reward"
    
    return Lootbox(
        name=f"Custom Flip.gg Box ${cost:.2f}",
        cost=cost,
        items=items,
        description=description
    )

def main():
    """Interactive main function"""
    calculator = LootboxCalculator()
    
    # Get user preferences
    cost, target_house_edge, variance_level = get_user_input()
    
    # Create custom lootbox
    print(f"\n🔧 Creating your custom lootbox...")
    lootbox = create_custom_lootbox(cost, target_house_edge, variance_level)
    
    # Optimize for target house edge
    print(f"🎯 Optimizing for {target_house_edge*100:.0f}% house edge...")
    optimized_lootbox = calculator.optimize_probabilities(lootbox, target_house_edge)
    
    # Analyze the optimized lootbox
    analysis = calculator.analyze_lootbox(optimized_lootbox)
    
    # Print results
    print(f"\n✅ YOUR OPTIMIZED LOOTBOX")
    print(f"="*60)
    print(f"Name: {optimized_lootbox.name}")
    print(f"Cost: ${optimized_lootbox.cost:.2f}")
    print(f"Expected Value: ${analysis['expected_value']:.4f}")
    print(f"House Edge: {analysis['house_edge']*100:.2f}%")
    print(f"Player Rating: {analysis['player_rating']}")
    print(f"Risk Level: {analysis['risk_level']}")
    
    print(f"\n🎁 ITEM CONFIGURATION:")
    print(f"{'Item':<18} {'Value':<8} {'Rarity':<10} {'Probability':<12} {'ROI'}")
    print("-" * 65)
    
    for item in optimized_lootbox.items:
        roi = ((item.value - optimized_lootbox.cost) / optimized_lootbox.cost) * 100
        print(f"{item.name:<18} ${item.value:<7.2f} {item.rarity.value.title():<10} "
              f"{item.probability*100:<11.2f}% {roi:>7.1f}%")
    
    print(f"\n🎯 PLAYER EXPERIENCE:")
    print(f"• {analysis['break_even_probability']*100:.1f}% chance to break even or profit")
    print(f"• {analysis['profit_10_probability']*100:.1f}% chance for 10%+ profit")
    print(f"• {analysis['profit_50_probability']*100:.1f}% chance for 50%+ profit")
    
    # Run quick simulation
    print(f"\n🎲 VALIDATION (10,000 simulations)...")
    sim_results = calculator.simulate_openings(optimized_lootbox, 10000)
    
    print(f"Simulated House Edge: {sim_results['house_edge_actual']*100:.2f}%")
    print(f"Simulated Win Rate: {sim_results['win_rate_percent']:.1f}%")
    print(f"Average ROI: {sim_results['roi_percent']:.1f}%")
    
    # Accuracy check
    house_edge_diff = abs(analysis['house_edge'] - sim_results['house_edge_actual'])
    accuracy = "✅ ACCURATE" if house_edge_diff < 0.02 else "⚠️ REVIEW NEEDED"
    print(f"Accuracy: {accuracy} (±{house_edge_diff*100:.2f}%)")
    
    # Save configuration
    filename = f"flip_gg_custom_{cost:.2f}_{target_house_edge*100:.0f}pct.json"
    
    config_dict = {
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
    
    with open(filename, "w") as f:
        json.dump(config_dict, f, indent=2)
    
    print(f"\n💾 SAVED TO: {filename}")
    
    # Implementation notes
    print(f"\n📋 IMPLEMENTATION NOTES FOR FLIP.GG:")
    print(f"="*50)
    print(f"1. Set lootbox cost to ${optimized_lootbox.cost:.2f}")
    print(f"2. Configure the following item probabilities:")
    
    for i, item in enumerate(optimized_lootbox.items, 1):
        percentage = item.probability * 100
        print(f"   {i}. {item.name}: {percentage:.3f}% (${item.value:.2f} value)")
    
    print(f"\n3. Expected metrics:")
    print(f"   • House Edge: {analysis['house_edge']*100:.2f}%")
    print(f"   • Player satisfaction: {analysis['player_rating']}")
    print(f"   • Break-even rate: {analysis['break_even_probability']*100:.1f}%")
    
    print(f"\n🎉 Your lootbox is ready for flip.gg!")
    
    # Ask if user wants to try different parameters
    another = input(f"\nWould you like to try different parameters? (y/n): ").lower()
    if another == 'y':
        main()

if __name__ == "__main__":
    main()
