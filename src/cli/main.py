"""
Command Line Interface for Lootbox Probability Toolkit

Provides an intuitive terminal interface for designing, analyzing,
and optimizing lootbox configurations.
"""
import click
import json
import sys
import os
from pathlib import Path
from typing import List, Optional
import logging
from tabulate import tabulate
from colorama import init, Fore, Back, Style
import pandas as pd

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.core.models import Lootbox, LootboxItem, RarityTier, OptimizationConstraints
from src.calculator.expected_value import ExpectedValueCalculator
from src.simulator.monte_carlo import MonteCarloSimulator
from src.optimizer.probability_optimizer import ProbabilityOptimizer

# Initialize colorama
init()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class LootboxCLI:
    """Main CLI application for lootbox toolkit"""
    
    def __init__(self):
        self.calculator = ExpectedValueCalculator()
        self.simulator = MonteCarloSimulator()
        self.optimizer = ProbabilityOptimizer()
        self.current_lootbox: Optional[Lootbox] = None
        
    def print_header(self, title: str):
        """Print a formatted header"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{title:^60}")
        print(f"{'='*60}{Style.RESET_ALL}\n")
    
    def print_success(self, message: str):
        """Print success message"""
        print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")
    
    def print_error(self, message: str):
        """Print error message"""
        print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")
    
    def print_warning(self, message: str):
        """Print warning message"""
        print(f"{Fore.YELLOW}⚠ {message}{Style.RESET_ALL}")


@click.group()
@click.pass_context
def cli(ctx):
    """🎲 Lootbox Probability Calculation Toolkit"""
    ctx.ensure_object(dict)
    ctx.obj['app'] = LootboxCLI()


@cli.command()
@click.option('--name', prompt='Lootbox name', help='Name for the lootbox')
@click.option('--cost', prompt='Lootbox cost ($0.50-$4.00)', type=float, help='Cost of the lootbox')
@click.option('--description', help='Optional description')
@click.pass_context
def create(ctx, name: str, cost: float, description: str):
    """Create a new lootbox configuration"""
    app = ctx.obj['app']
    app.print_header("CREATE NEW LOOTBOX")
    
    if not 0.5 <= cost <= 4.0:
        app.print_error("Cost must be between $0.50 and $4.00")
        return
    
    # Interactive item creation
    items = []
    print("Add items to your lootbox. Press Enter without a name to finish.")
    
    while True:
        print(f"\n{Fore.YELLOW}Item #{len(items) + 1}{Style.RESET_ALL}")
        item_name = click.prompt("Item name (or press Enter to finish)", default="", show_default=False)
        
        if not item_name.strip():
            break
        
        item_value = click.prompt("Item value ($)", type=float)
        
        print("Available rarities:")
        for i, rarity in enumerate(RarityTier, 1):
            print(f"  {i}. {rarity.value.title()}")
        
        rarity_choice = click.prompt("Choose rarity (1-6)", type=int)
        if not 1 <= rarity_choice <= 6:
            app.print_error("Invalid rarity choice")
            continue
        
        rarity = list(RarityTier)[rarity_choice - 1]
        probability = click.prompt("Probability (0.0-1.0)", type=float)
        
        if not 0 <= probability <= 1:
            app.print_error("Probability must be between 0 and 1")
            continue
        
        item_desc = click.prompt("Item description (optional)", default="", show_default=False)
        
        item = LootboxItem(
            name=item_name,
            value=item_value,
            rarity=rarity,
            probability=probability,
            description=item_desc if item_desc else None
        )
        
        items.append(item)
        app.print_success(f"Added: {item}")
    
    if not items:
        app.print_error("Must add at least one item")
        return
    
    try:
        # Normalize probabilities
        total_prob = sum(item.probability for item in items)
        if abs(total_prob - 1.0) > 1e-6:
            app.print_warning(f"Probabilities sum to {total_prob:.4f}, normalizing to 1.0")
            for item in items:
                item.probability = item.probability / total_prob
        
        lootbox = Lootbox(
            name=name,
            cost=cost,
            description=description,
            items=items
        )
        
        ctx.obj['app'].current_lootbox = lootbox
        app.print_success(f"Created lootbox '{name}' with {len(items)} items")
        
        # Show quick analysis
        ev = lootbox.get_expected_value()
        he = lootbox.get_house_edge()
        
        print(f"\n{Fore.CYAN}Quick Analysis:{Style.RESET_ALL}")
        print(f"Expected Value: ${ev:.4f}")
        print(f"House Edge: {he*100:.2f}%")
        print(f"Player Rating: {app.calculator.generate_full_analysis(lootbox).get_player_value_rating()}")
        
    except Exception as e:
        app.print_error(f"Failed to create lootbox: {str(e)}")


@cli.command()
@click.option('--file', 'filepath', help='File path to load from')
@click.pass_context
def load(ctx, filepath: str):
    """Load a lootbox configuration from file"""
    app = ctx.obj['app']
    
    if not filepath:
        filepath = click.prompt("Enter file path")
    
    try:
        lootbox = Lootbox.load_from_file(filepath)
        ctx.obj['app'].current_lootbox = lootbox
        app.print_success(f"Loaded lootbox '{lootbox.name}' from {filepath}")
        
        # Show summary
        print(f"\nItems: {len(lootbox.items)}")
        print(f"Cost: ${lootbox.cost:.2f}")
        print(f"Expected Value: ${lootbox.get_expected_value():.4f}")
        print(f"House Edge: {lootbox.get_house_edge()*100:.2f}%")
        
    except Exception as e:
        app.print_error(f"Failed to load lootbox: {str(e)}")


@cli.command()
@click.option('--file', 'filepath', help='File path to save to')
@click.pass_context
def save(ctx, filepath: str):
    """Save current lootbox configuration to file"""
    app = ctx.obj['app']
    
    if not app.current_lootbox:
        app.print_error("No lootbox loaded. Create or load a lootbox first.")
        return
    
    if not filepath:
        default_name = f"{app.current_lootbox.name.lower().replace(' ', '_')}.json"
        filepath = click.prompt("Enter file path", default=default_name)
    
    try:
        app.current_lootbox.save_to_file(filepath)
        app.print_success(f"Saved lootbox to {filepath}")
    except Exception as e:
        app.print_error(f"Failed to save lootbox: {str(e)}")


@cli.command()
@click.pass_context
def analyze(ctx):
    """Analyze current lootbox configuration"""
    app = ctx.obj['app']
    
    if not app.current_lootbox:
        app.print_error("No lootbox loaded. Create or load a lootbox first.")
        return
    
    app.print_header(f"ANALYSIS: {app.current_lootbox.name}")
    
    # Generate full analysis
    analytics = app.calculator.generate_full_analysis(app.current_lootbox)
    
    # Basic metrics
    print(f"{Fore.CYAN}Basic Metrics:{Style.RESET_ALL}")
    print(f"Cost:              ${app.current_lootbox.cost:.2f}")
    print(f"Expected Value:    ${analytics.expected_value:.4f}")
    print(f"House Edge:        {analytics.house_edge*100:.2f}%")
    print(f"Standard Deviation: ${analytics.standard_deviation:.4f}")
    print(f"Variance:          ${analytics.variance:.4f}")
    print(f"Risk Level:        {analytics.get_risk_level()}")
    print(f"Player Rating:     {analytics.get_player_value_rating()}")
    
    # Break-even analysis
    break_even_prob = app.calculator.calculate_break_even_probability(app.current_lootbox)
    profit_prob = app.calculator.calculate_profit_probability(app.current_lootbox, 0.1)
    
    print(f"\n{Fore.CYAN}Player Odds:{Style.RESET_ALL}")
    print(f"Break Even Chance: {break_even_prob*100:.2f}%")
    print(f"10%+ Profit Chance: {profit_prob*100:.2f}%")
    
    # Rarity breakdown
    print(f"\n{Fore.CYAN}Rarity Analysis:{Style.RESET_ALL}")
    rarity_data = []
    for rarity in RarityTier:
        breakdown = analytics.rarity_breakdown[rarity.value]
        if breakdown['item_count'] > 0:
            rarity_data.append([
                rarity.value.title(),
                breakdown['item_count'],
                f"{breakdown['total_probability']*100:.2f}%",
                f"${breakdown['average_value']:.2f}",
                f"${breakdown['expected_contribution']:.4f}"
            ])
    
    if rarity_data:
        print(tabulate(
            rarity_data,
            headers=['Rarity', 'Items', 'Probability', 'Avg Value', 'EV Contribution'],
            tablefmt='grid'
        ))
    
    # Value percentiles
    print(f"\n{Fore.CYAN}Value Distribution:{Style.RESET_ALL}")
    percentile_data = []
    for p_name, value in analytics.value_percentiles.items():
        percentile_data.append([p_name.upper(), f"${value:.2f}"])
    
    print(tabulate(
        percentile_data,
        headers=['Percentile', 'Value'],
        tablefmt='grid'
    ))


@cli.command()
@click.option('--simulations', default=10000, help='Number of simulations to run')
@click.option('--seed', type=int, help='Random seed for reproducible results')
@click.pass_context
def simulate(ctx, simulations: int, seed: Optional[int]):
    """Run Monte Carlo simulation on current lootbox"""
    app = ctx.obj['app']
    
    if not app.current_lootbox:
        app.print_error("No lootbox loaded. Create or load a lootbox first.")
        return
    
    app.print_header(f"MONTE CARLO SIMULATION: {app.current_lootbox.name}")
    
    if seed:
        app.simulator = MonteCarloSimulator(seed=seed)
        print(f"Using random seed: {seed}")
    
    # Run simulation
    result = app.simulator.simulate_multiple_openings(
        app.current_lootbox,
        simulations,
        show_progress=True
    )
    
    # Display results
    print(f"\n{Fore.CYAN}Simulation Results ({simulations:,} openings):{Style.RESET_ALL}")
    print(f"Total Cost:        ${result.total_cost:.2f}")
    print(f"Total Value:       ${result.total_value_received:.2f}")
    print(f"Average Value:     ${result.average_value_per_box:.4f}")
    print(f"Median Value:      ${result.median_value_per_box:.4f}")
    print(f"Standard Deviation: ${result.std_deviation:.4f}")
    print(f"ROI:              {result.get_roi():.2f}%")
    print(f"Win Rate:         {result.get_win_rate():.2f}%")
    print(f"Actual House Edge: {result.house_edge_actual*100:.2f}%")
    print(f"Theoretical H.E.:  {result.house_edge_theoretical*100:.2f}%")
    
    # Rarity distribution
    print(f"\n{Fore.CYAN}Rarity Distribution:{Style.RESET_ALL}")
    rarity_data = []
    for rarity, count in result.rarity_distribution.items():
        percentage = (count / simulations) * 100
        rarity_data.append([rarity.title(), count, f"{percentage:.2f}%"])
    
    print(tabulate(
        rarity_data,
        headers=['Rarity', 'Count', 'Percentage'],
        tablefmt='grid'
    ))


@cli.command()
@click.option('--target-house-edge', default=0.15, help='Target house edge (0.15 = 15%)')
@click.option('--method', type=click.Choice(['scipy', 'genetic']), default='scipy', help='Optimization method')
@click.pass_context
def optimize(ctx, target_house_edge: float, method: str):
    """Optimize current lootbox probabilities"""
    app = ctx.obj['app']
    
    if not app.current_lootbox:
        app.print_error("No lootbox loaded. Create or load a lootbox first.")
        return
    
    app.print_header(f"OPTIMIZATION: {app.current_lootbox.name}")
    
    print(f"Target House Edge: {target_house_edge*100:.1f}%")
    print(f"Method: {method.title()}")
    
    # Run optimization
    if method == 'scipy':
        result = app.optimizer.optimize_for_house_edge(
            app.current_lootbox,
            target_house_edge
        )
    else:  # genetic
        result = app.optimizer.genetic_algorithm_optimization(
            app.current_lootbox.items,
            app.current_lootbox.cost,
            target_house_edge
        )
    
    if result.success:
        app.print_success(result.optimization_message)
        
        print(f"\n{Fore.CYAN}Optimization Results:{Style.RESET_ALL}")
        print(f"Original House Edge: {result.original_house_edge*100:.2f}%")
        print(f"Optimized House Edge: {result.optimized_house_edge*100:.2f}%")
        print(f"Original Expected Value: ${result.original_expected_value:.4f}")
        print(f"Optimized Expected Value: ${result.optimized_expected_value:.4f}")
        print(f"Iterations: {result.iterations}")
        
        # Ask if user wants to use optimized version
        if click.confirm("Use optimized configuration?"):
            ctx.obj['app'].current_lootbox = result.optimized_lootbox
            app.print_success("Switched to optimized configuration")
    else:
        app.print_error(result.optimization_message)


@cli.command()
@click.pass_context
def show(ctx):
    """Show current lootbox configuration"""
    app = ctx.obj['app']
    
    if not app.current_lootbox:
        app.print_error("No lootbox loaded. Create or load a lootbox first.")
        return
    
    lootbox = app.current_lootbox
    app.print_header(f"LOOTBOX: {lootbox.name}")
    
    if lootbox.description:
        print(f"Description: {lootbox.description}")
    
    print(f"Cost: ${lootbox.cost:.2f}")
    print(f"Items: {len(lootbox.items)}")
    
    # Items table
    print(f"\n{Fore.CYAN}Items:{Style.RESET_ALL}")
    items_data = []
    for item in lootbox.items:
        items_data.append([
            item.name,
            item.rarity.value.title(),
            f"${item.value:.2f}",
            f"{item.probability*100:.4f}%",
            item.description or ""
        ])
    
    print(tabulate(
        items_data,
        headers=['Name', 'Rarity', 'Value', 'Probability', 'Description'],
        tablefmt='grid'
    ))


@cli.command()
@click.option('--template', type=click.Choice(['csgo', 'balanced', 'high_variance', 'low_variance']), 
              default='balanced', help='Template type')
@click.option('--cost', default=2.0, help='Lootbox cost')
@click.pass_context
def template(ctx, template: str, cost: float):
    """Create lootbox from predefined template"""
    app = ctx.obj['app']
    
    if not 0.5 <= cost <= 4.0:
        app.print_error("Cost must be between $0.50 and $4.00")
        return
    
    templates = {
        'balanced': {
            'name': 'Balanced Box',
            'description': 'A well-balanced lootbox with fair odds',
            'items': [
                {'name': 'Common Coin', 'value': 0.10, 'rarity': RarityTier.COMMON, 'probability': 0.50},
                {'name': 'Uncommon Token', 'value': 0.50, 'rarity': RarityTier.UNCOMMON, 'probability': 0.25},
                {'name': 'Rare Gem', 'value': 1.50, 'rarity': RarityTier.RARE, 'probability': 0.15},
                {'name': 'Epic Crystal', 'value': 4.00, 'rarity': RarityTier.EPIC, 'probability': 0.08},
                {'name': 'Legendary Artifact', 'value': 12.00, 'rarity': RarityTier.LEGENDARY, 'probability': 0.02}
            ]
        },
        'csgo': {
            'name': 'CS:GO Style Case',
            'description': 'CS:GO-inspired rarity distribution',
            'items': [
                {'name': 'Consumer Grade', 'value': 0.05, 'rarity': RarityTier.COMMON, 'probability': 0.7992},
                {'name': 'Industrial Grade', 'value': 0.15, 'rarity': RarityTier.UNCOMMON, 'probability': 0.1598},
                {'name': 'Mil-Spec', 'value': 0.75, 'rarity': RarityTier.RARE, 'probability': 0.032},
                {'name': 'Restricted', 'value': 3.50, 'rarity': RarityTier.EPIC, 'probability': 0.0064},
                {'name': 'Classified', 'value': 15.00, 'rarity': RarityTier.LEGENDARY, 'probability': 0.0013},
                {'name': 'Covert', 'value': 75.00, 'rarity': RarityTier.MYTHIC, 'probability': 0.0013}
            ]
        },
        'high_variance': {
            'name': 'High Variance Box',
            'description': 'High risk, high reward lootbox',
            'items': [
                {'name': 'Nothing', 'value': 0.01, 'rarity': RarityTier.COMMON, 'probability': 0.85},
                {'name': 'Small Prize', 'value': 0.25, 'rarity': RarityTier.UNCOMMON, 'probability': 0.10},
                {'name': 'Medium Prize', 'value': 2.00, 'rarity': RarityTier.RARE, 'probability': 0.04},
                {'name': 'Jackpot', 'value': 50.00, 'rarity': RarityTier.LEGENDARY, 'probability': 0.01}
            ]
        },
        'low_variance': {
            'name': 'Low Variance Box',
            'description': 'Consistent, predictable returns',
            'items': [
                {'name': 'Small Win', 'value': 0.80, 'rarity': RarityTier.COMMON, 'probability': 0.40},
                {'name': 'Medium Win', 'value': 1.20, 'rarity': RarityTier.UNCOMMON, 'probability': 0.35},
                {'name': 'Good Win', 'value': 1.80, 'rarity': RarityTier.RARE, 'probability': 0.20},
                {'name': 'Great Win', 'value': 3.00, 'rarity': RarityTier.EPIC, 'probability': 0.05}
            ]
        }
    }
    
    template_config = templates[template]
    
    # Create items
    items = []
    for item_config in template_config['items']:
        item = LootboxItem(
            name=item_config['name'],
            value=item_config['value'],
            rarity=item_config['rarity'],
            probability=item_config['probability']
        )
        items.append(item)
    
    # Create lootbox
    lootbox = Lootbox(
        name=template_config['name'],
        description=template_config['description'],
        cost=cost,
        items=items
    )
    
    ctx.obj['app'].current_lootbox = lootbox
    app.print_success(f"Created '{template}' template lootbox")
    
    # Show quick stats
    ev = lootbox.get_expected_value()
    he = lootbox.get_house_edge()
    print(f"Expected Value: ${ev:.4f}")
    print(f"House Edge: {he*100:.2f}%")


@cli.command()
@click.option('--min-cost', default=0.5, help='Minimum cost to analyze')
@click.option('--max-cost', default=4.0, help='Maximum cost to analyze')
@click.option('--house-edge', default=0.15, help='Target house edge')
@click.pass_context
def cost_analysis(ctx, min_cost: float, max_cost: float, house_edge: float):
    """Analyze optimal configurations across cost range"""
    app = ctx.obj['app']
    
    if not app.current_lootbox:
        app.print_error("No lootbox loaded. Create or load a lootbox first.")
        return
    
    app.print_header("COST RANGE ANALYSIS")
    
    # Run optimization across cost range
    results = app.optimizer.optimize_for_cost_range(
        app.current_lootbox.items,
        min_cost,
        max_cost,
        house_edge
    )
    
    # Display results table
    analysis_data = []
    for result in results:
        if result.success and result.optimized_lootbox:
            lootbox = result.optimized_lootbox
            analysis_data.append([
                f"${lootbox.cost:.2f}",
                f"${lootbox.get_expected_value():.4f}",
                f"{lootbox.get_house_edge()*100:.2f}%",
                app.calculator.generate_full_analysis(lootbox).get_risk_level(),
                app.calculator.generate_full_analysis(lootbox).get_player_value_rating()
            ])
    
    if analysis_data:
        print(tabulate(
            analysis_data,
            headers=['Cost', 'Expected Value', 'House Edge', 'Risk Level', 'Player Rating'],
            tablefmt='grid'
        ))
    else:
        app.print_error("No successful optimizations found")


if __name__ == '__main__':
    cli()
