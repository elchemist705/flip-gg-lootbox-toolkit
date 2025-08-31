#!/usr/bin/env python3
"""
Batch Lootbox Analyzer

Processes multiple lootbox configurations and generates comparative reports.
"""
import sys
import os
import json
import argparse
from pathlib import Path
from typing import List, Dict
import pandas as pd
from datetime import datetime

# Add to path
toolkit_dir = Path(__file__).parent.parent
sys.path.insert(0, str(toolkit_dir))

from lootbox_calculator import LootboxCalculator, Lootbox, LootboxItem, RarityTier

class BatchAnalyzer:
    """Batch processor for lootbox analysis"""
    
    def __init__(self):
        self.calculator = LootboxCalculator()
        self.results = []
    
    def load_lootboxes_from_directory(self, directory: Path) -> List[Lootbox]:
        """Load all lootbox configurations from a directory"""
        lootboxes = []
        
        for file_path in directory.glob("*.json"):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                # Convert to lootbox
                items = []
                for item_data in data['items']:
                    items.append(LootboxItem(
                        name=item_data['name'],
                        value=item_data['value'],
                        rarity=RarityTier(item_data['rarity']),
                        probability=item_data['probability'],
                        description=item_data.get('description', '')
                    ))
                
                lootbox = Lootbox(
                    name=data['name'],
                    cost=data['cost'],
                    items=items,
                    description=data.get('description', '')
                )
                
                lootboxes.append(lootbox)
                print(f"✅ Loaded: {lootbox.name}")
                
            except Exception as e:
                print(f"❌ Failed to load {file_path}: {str(e)}")
        
        return lootboxes
    
    def analyze_batch(self, lootboxes: List[Lootbox], num_simulations: int = 10000) -> pd.DataFrame:
        """Analyze a batch of lootboxes"""
        results = []
        
        print(f"\n🔍 Analyzing {len(lootboxes)} lootboxes...")
        
        for lootbox in lootboxes:
            print(f"  Analyzing: {lootbox.name}")
            
            # Basic analysis
            analysis = self.calculator.analyze_lootbox(lootbox)
            
            # Simulation
            sim_results = self.calculator.simulate_openings(lootbox, num_simulations)
            
            result = {
                'Name': lootbox.name,
                'Cost': lootbox.cost,
                'Expected_Value': analysis['expected_value'],
                'House_Edge_Pct': analysis['house_edge'] * 100,
                'Player_Rating': analysis['player_rating'],
                'Risk_Level': analysis['risk_level'],
                'Break_Even_Pct': analysis['break_even_probability'] * 100,
                'Profit_10_Pct': analysis['profit_10_probability'] * 100,
                'Simulated_House_Edge_Pct': sim_results['house_edge_actual'] * 100,
                'Simulated_ROI_Pct': sim_results['roi_percent'],
                'Simulated_Win_Rate_Pct': sim_results['win_rate_percent'],
                'Variance': analysis['variance'],
                'Std_Deviation': analysis['std_deviation'],
                'CV': analysis['coefficient_of_variation']
            }
            
            results.append(result)
        
        return pd.DataFrame(results)
    
    def generate_report(self, df: pd.DataFrame, output_path: Path):
        """Generate comprehensive analysis report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # CSV report
        csv_path = output_path / f"lootbox_analysis_{timestamp}.csv"
        df.to_csv(csv_path, index=False)
        print(f"✅ CSV report saved: {csv_path}")
        
        # Summary report
        summary_path = output_path / f"lootbox_summary_{timestamp}.txt"
        
        with open(summary_path, 'w') as f:
            f.write("🎲 LOOTBOX BATCH ANALYSIS REPORT\\n")
            f.write("=" * 50 + "\\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n")
            f.write(f"Total Lootboxes: {len(df)}\\n\\n")
            
            # Summary statistics
            f.write("📊 SUMMARY STATISTICS\\n")
            f.write("-" * 30 + "\\n")
            f.write(f"Average Cost: ${df['Cost'].mean():.2f}\\n")
            f.write(f"Average House Edge: {df['House_Edge_Pct'].mean():.2f}%\\n")
            f.write(f"Average Expected Value: ${df['Expected_Value'].mean():.4f}\\n")
            f.write(f"Average Break-Even Rate: {df['Break_Even_Pct'].mean():.2f}%\\n")
            
            # Best performers
            f.write("\\n🏆 TOP PERFORMERS\\n")
            f.write("-" * 20 + "\\n")
            
            # Best player value
            best_player_value = df.loc[df['House_Edge_Pct'].idxmin()]
            f.write(f"Best Player Value: {best_player_value['Name']} ({best_player_value['House_Edge_Pct']:.2f}% house edge)\\n")
            
            # Most profitable
            most_profitable = df.loc[df['House_Edge_Pct'].idxmax()]
            f.write(f"Most Profitable: {most_profitable['Name']} ({most_profitable['House_Edge_Pct']:.2f}% house edge)\\n")
            
            # Most balanced
            target_house_edge = 15.0
            df['House_Edge_Distance'] = abs(df['House_Edge_Pct'] - target_house_edge)
            most_balanced = df.loc[df['House_Edge_Distance'].idxmin()]
            f.write(f"Most Balanced: {most_balanced['Name']} ({most_balanced['House_Edge_Pct']:.2f}% house edge)\\n")
            
            # Detailed breakdown
            f.write("\\n📋 DETAILED BREAKDOWN\\n")
            f.write("-" * 25 + "\\n")
            
            for _, row in df.iterrows():
                f.write(f"\\n{row['Name']}:\\n")
                f.write(f"  Cost: ${row['Cost']:.2f}\\n")
                f.write(f"  House Edge: {row['House_Edge_Pct']:.2f}%\\n")
                f.write(f"  Expected Value: ${row['Expected_Value']:.4f}\\n")
                f.write(f"  Player Rating: {row['Player_Rating']}\\n")
                f.write(f"  Break-Even Rate: {row['Break_Even_Pct']:.2f}%\\n")
        
        print(f"✅ Summary report saved: {summary_path}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Batch Lootbox Analyzer")
    parser.add_argument('--input-dir', type=Path, default=Path('outputs'),
                       help='Directory containing lootbox JSON files')
    parser.add_argument('--output-dir', type=Path, default=Path('outputs'),
                       help='Directory for analysis reports')
    parser.add_argument('--simulations', type=int, default=10000,
                       help='Number of Monte Carlo simulations per lootbox')
    
    args = parser.parse_args()
    
    # Ensure directories exist
    if not args.input_dir.exists():
        print(f"❌ Input directory not found: {args.input_dir}")
        return
    
    args.output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize analyzer
    analyzer = BatchAnalyzer()
    
    # Load lootboxes
    print(f"🔍 Loading lootboxes from: {args.input_dir}")
    lootboxes = analyzer.load_lootboxes_from_directory(args.input_dir)
    
    if not lootboxes:
        print("❌ No valid lootbox configurations found")
        return
    
    # Analyze batch
    df = analyzer.analyze_batch(lootboxes, args.simulations)
    
    # Generate report
    analyzer.generate_report(df, args.output_dir)
    
    # Print summary to console
    print(f"\\n📊 BATCH ANALYSIS SUMMARY")
    print("="*40)
    print(f"Analyzed: {len(lootboxes)} lootboxes")
    print(f"Average House Edge: {df['House_Edge_Pct'].mean():.2f}%")
    print(f"Cost Range: ${df['Cost'].min():.2f} - ${df['Cost'].max():.2f}")
    
    # Show top 3 by different metrics
    print(f"\\n🏆 TOP PERFORMERS:")
    
    # Best player value (lowest house edge)
    best_player = df.loc[df['House_Edge_Pct'].idxmin()]
    print(f"Best Player Value: {best_player['Name']} ({best_player['House_Edge_Pct']:.1f}% house edge)")
    
    # Most profitable (highest house edge)
    most_profitable = df.loc[df['House_Edge_Pct'].idxmax()]
    print(f"Most Profitable: {most_profitable['Name']} ({most_profitable['House_Edge_Pct']:.1f}% house edge)")
    
    # Most balanced (closest to 15% house edge)
    df['Distance_from_15'] = abs(df['House_Edge_Pct'] - 15.0)
    most_balanced = df.loc[df['Distance_from_15'].idxmin()]
    print(f"Most Balanced: {most_balanced['Name']} ({most_balanced['House_Edge_Pct']:.1f}% house edge)")

if __name__ == "__main__":
    main()
