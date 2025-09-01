#!/usr/bin/env python3
"""
Interactive Flip.gg Lootbox Designer

Specifically designed for your requirements:
- Cost between $0.50 and $1000.00
- Mix of high cases (high-value items) and low cases (low-value items)
- Expanded item variety: 8-12 items per lootbox (up from 4-6)
- Optimal probability distributions for profitability
- Enhanced community box support with granular prize tiers
- Advanced variance scaling for different player types
"""
from lootbox_calculator import LootboxCalculator, Lootbox, LootboxItem, RarityTier
import json

def validate_probability_distribution(items):
    """Validate that probabilities sum to 1.0 and are all positive"""
    total_prob = sum(item.probability for item in items)
    if abs(total_prob - 1.0) > 0.0001:
        raise ValueError(f"Probabilities sum to {total_prob:.6f}, not 1.0")
    
    for item in items:
        if item.probability < 0:
            raise ValueError(f"Negative probability for {item.name}: {item.probability}")
    
    return True

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
    print(f"1. Low variance - Consistent, predictable outcomes (8 items)")
    print(f"2. Medium variance - Balanced excitement (9 items)")
    print(f"3. High variance - Big wins, big losses (11-12 items)")
    
    while True:
        variance_choice = input("Choose variance (1-3): ").strip()
        if variance_choice in ["1", "2", "3"]:
            variance_level = int(variance_choice)
            break
        else:
            print("❌ Please choose 1, 2, or 3")
    
    return cost, house_edge, variance_level

def create_custom_lootbox(cost: float, house_edge: float, variance_level: int) -> Lootbox:
    """Create custom lootbox based on user preferences with expanded item variety"""
    
    if variance_level == 1:  # Low variance - 7-8 items for more consistent gameplay
        # More consistent values, closer to cost with expanded variety
        items = [
            LootboxItem("Tiny Prize", cost * 0.20, RarityTier.COMMON, 0.28),
            LootboxItem("Small Prize", cost * 0.35, RarityTier.COMMON, 0.25),
            LootboxItem("Medium Prize", cost * 0.60, RarityTier.UNCOMMON, 0.22),
            LootboxItem("Good Prize", cost * 0.90, RarityTier.UNCOMMON, 0.15),
            LootboxItem("Great Prize", cost * 1.40, RarityTier.RARE, 0.08),
            LootboxItem("Excellent Prize", cost * 2.20, RarityTier.RARE, 0.015),
            LootboxItem("Premium Prize", cost * 4.00, RarityTier.EPIC, 0.004),
            LootboxItem("Elite Prize", cost * 8.00, RarityTier.LEGENDARY, 0.001)
        ]
        description = "Low variance - consistent returns with expanded variety"
        
    elif variance_level == 2:  # Medium variance - 8-9 items for balanced excitement
        # Balanced distribution with more granular tiers
        items = [
            LootboxItem("Basic Item", cost * 0.12, RarityTier.COMMON, 0.32),
            LootboxItem("Common Item", cost * 0.28, RarityTier.COMMON, 0.25),
            LootboxItem("Decent Item", cost * 0.50, RarityTier.UNCOMMON, 0.20),
            LootboxItem("Good Item", cost * 0.85, RarityTier.UNCOMMON, 0.12),
            LootboxItem("Fine Item", cost * 1.30, RarityTier.RARE, 0.08),
            LootboxItem("Excellent Item", cost * 2.50, RarityTier.RARE, 0.025),
            LootboxItem("Epic Item", cost * 5.50, RarityTier.EPIC, 0.0045),
            LootboxItem("Legendary Item", cost * 12.00, RarityTier.LEGENDARY, 0.0003),
            LootboxItem("Mythic Item", cost * 25.00, RarityTier.MYTHIC, 0.0002)
        ]
        description = "Medium variance - balanced excitement with expanded tiers"
        
    else:  # High variance - 9-12 items for maximum variety
        # Extreme distribution with big jackpots - scale appropriately for cost
        if cost <= 10.0:
            # Standard scaling for low-medium cost boxes with expanded variety
            items = [
                LootboxItem("Dust", cost * 0.03, RarityTier.COMMON, 0.40),
                LootboxItem("Scraps", cost * 0.08, RarityTier.COMMON, 0.25),
                LootboxItem("Small Win", cost * 0.20, RarityTier.UNCOMMON, 0.15),
                LootboxItem("Decent Win", cost * 0.45, RarityTier.UNCOMMON, 0.10),
                LootboxItem("Good Win", cost * 0.80, RarityTier.RARE, 0.06),
                LootboxItem("Great Win", cost * 1.50, RarityTier.RARE, 0.025),
                LootboxItem("Big Win", cost * 3.50, RarityTier.EPIC, 0.012),
                LootboxItem("Major Win", cost * 8.00, RarityTier.EPIC, 0.005),
                LootboxItem("Huge Win", cost * 18.00, RarityTier.LEGENDARY, 0.002),
                LootboxItem("Mega Jackpot", cost * 40.00, RarityTier.LEGENDARY, 0.0008),
                LootboxItem("Ultra Jackpot", cost * 100.00, RarityTier.MYTHIC, 0.0002)
            ]
        elif cost <= 100.0:
            # Medium-high cost scaling (whale tier) with more granular prizes
            items = [
                LootboxItem("Token Drop", cost * 0.02, RarityTier.COMMON, 0.45),
                LootboxItem("Small Coins", cost * 0.06, RarityTier.COMMON, 0.25),
                LootboxItem("Coin Bundle", cost * 0.15, RarityTier.UNCOMMON, 0.15),
                LootboxItem("Token Pack", cost * 0.35, RarityTier.UNCOMMON, 0.08),
                LootboxItem("Good Win", cost * 0.70, RarityTier.RARE, 0.04),
                LootboxItem("Great Win", cost * 1.20, RarityTier.RARE, 0.02),
                LootboxItem("Major Win", cost * 2.80, RarityTier.EPIC, 0.008),
                LootboxItem("Big Jackpot", cost * 6.00, RarityTier.EPIC, 0.003),
                LootboxItem("Huge Jackpot", cost * 12.00, RarityTier.LEGENDARY, 0.0015),
                LootboxItem("Ultimate Prize", min(cost * 25.00, 2000.0), RarityTier.LEGENDARY, 0.0004),
                LootboxItem("Supreme Treasure", min(cost * 50.00, 5000.0), RarityTier.MYTHIC, 0.0001)
            ]
        else:
            # Ultra-high cost scaling (luxury/elite tier) with maximum variety
            items = [
                LootboxItem("Base Token", cost * 0.015, RarityTier.COMMON, 0.50),
                LootboxItem("Micro Prize", cost * 0.04, RarityTier.COMMON, 0.25),
                LootboxItem("Minor Prize", cost * 0.10, RarityTier.UNCOMMON, 0.12),
                LootboxItem("Small Prize", cost * 0.25, RarityTier.UNCOMMON, 0.08),
                LootboxItem("Decent Prize", cost * 0.50, RarityTier.RARE, 0.03),
                LootboxItem("Good Prize", cost * 0.90, RarityTier.RARE, 0.015),
                LootboxItem("Great Prize", cost * 1.80, RarityTier.EPIC, 0.006),
                LootboxItem("Major Prize", cost * 3.50, RarityTier.EPIC, 0.003),
                LootboxItem("Elite Jackpot", cost * 7.00, RarityTier.LEGENDARY, 0.0012),
                LootboxItem("Premium Jackpot", min(cost * 15.00, 5000.0), RarityTier.LEGENDARY, 0.0005),
                LootboxItem("Supreme Treasure", min(cost * 35.00, 10000.0), RarityTier.MYTHIC, 0.0002),
                LootboxItem("Ultimate Fortune", min(cost * 75.00, 25000.0), RarityTier.MYTHIC, 0.0001)
            ]
        description = "High variance - high risk, high reward with maximum variety"
    
    # Validate probability distribution
    try:
        validate_probability_distribution(items)
    except ValueError as e:
        print(f"⚠️ Warning: Probability distribution issue: {e}")
        print("Adjusting probabilities to ensure they sum to 1.0...")
        # Normalize probabilities to sum to 1.0
        total_prob = sum(item.probability for item in items)
        for item in items:
            item.probability = item.probability / total_prob
    
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
    print(f"Total Items: {len(optimized_lootbox.items)} cases/prizes")
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
