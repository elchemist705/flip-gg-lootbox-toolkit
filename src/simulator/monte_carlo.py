"""
Monte Carlo Simulation Engine for Lootbox Testing

Performs statistical simulations to validate theoretical calculations
and analyze lootbox performance over many trials.
"""
import random
import numpy as np
from typing import List, Dict, Tuple, Optional
from collections import defaultdict, Counter
import statistics
import logging
from tqdm import tqdm

from ..core.models import Lootbox, LootboxItem, RarityTier, SimulationResult

logger = logging.getLogger(__name__)


class MonteCarloSimulator:
    """
    Monte Carlo simulation engine for lootbox analysis
    """
    
    def __init__(self, seed: Optional[int] = None):
        """
        Initialize simulator
        
        Args:
            seed: Random seed for reproducible results
        """
        self.logger = logging.getLogger(__name__)
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
    
    def simulate_single_opening(self, lootbox: Lootbox) -> LootboxItem:
        """
        Simulate opening a single lootbox
        
        Args:
            lootbox: Lootbox configuration
            
        Returns:
            The item obtained from the lootbox
        """
        # Generate random number
        rand = random.random()
        
        # Find which item was selected based on cumulative probabilities
        cumulative_prob = 0.0
        for item in lootbox.items:
            cumulative_prob += item.probability
            if rand <= cumulative_prob:
                return item
        
        # Fallback to last item (should not happen with properly normalized probabilities)
        return lootbox.items[-1]
    
    def simulate_multiple_openings(
        self,
        lootbox: Lootbox,
        num_simulations: int = 10000,
        show_progress: bool = True
    ) -> SimulationResult:
        """
        Simulate opening multiple lootboxes
        
        Args:
            lootbox: Lootbox configuration
            num_simulations: Number of simulations to run
            show_progress: Whether to show progress bar
            
        Returns:
            Simulation results
        """
        self.logger.info(f"Running {num_simulations:,} simulations for '{lootbox.name}'")
        
        # Track results
        obtained_items = []
        obtained_values = []
        rarity_counts = defaultdict(int)
        value_counts = defaultdict(int)
        
        # Run simulations
        iterator = tqdm(range(num_simulations), desc="Simulating") if show_progress else range(num_simulations)
        
        for _ in iterator:
            item = self.simulate_single_opening(lootbox)
            obtained_items.append(item)
            obtained_values.append(item.value)
            rarity_counts[item.rarity.value] += 1
            
            # Bin values for distribution analysis
            value_bin = self._get_value_bin(item.value)
            value_counts[value_bin] += 1
        
        # Calculate statistics
        total_cost = num_simulations * lootbox.cost
        total_value = sum(obtained_values)
        average_value = statistics.mean(obtained_values)
        median_value = statistics.median(obtained_values)
        std_deviation = statistics.stdev(obtained_values) if len(obtained_values) > 1 else 0.0
        
        # Calculate probabilities
        profitable_outcomes = sum(1 for value in obtained_values if value > lootbox.cost)
        break_even_outcomes = sum(1 for value in obtained_values if value >= lootbox.cost)
        
        profit_probability = profitable_outcomes / num_simulations
        break_even_probability = break_even_outcomes / num_simulations
        
        # Calculate house edges
        house_edge_actual = (total_cost - total_value) / total_cost
        house_edge_theoretical = lootbox.get_house_edge()
        
        return SimulationResult(
            lootbox_name=lootbox.name,
            num_simulations=num_simulations,
            total_cost=total_cost,
            total_value_received=total_value,
            average_value_per_box=average_value,
            median_value_per_box=median_value,
            std_deviation=std_deviation,
            profit_probability=profit_probability,
            break_even_probability=break_even_probability,
            house_edge_actual=house_edge_actual,
            house_edge_theoretical=house_edge_theoretical,
            value_distribution=dict(value_counts),
            rarity_distribution=dict(rarity_counts)
        )
    
    def _get_value_bin(self, value: float) -> str:
        """
        Categorize value into bins for distribution analysis
        
        Args:
            value: Item value
            
        Returns:
            Value bin string
        """
        if value < 0.25:
            return "$0.00-$0.25"
        elif value < 0.50:
            return "$0.25-$0.50"
        elif value < 1.00:
            return "$0.50-$1.00"
        elif value < 2.00:
            return "$1.00-$2.00"
        elif value < 5.00:
            return "$2.00-$5.00"
        elif value < 10.00:
            return "$5.00-$10.00"
        elif value < 25.00:
            return "$10.00-$25.00"
        elif value < 50.00:
            return "$25.00-$50.00"
        elif value < 100.00:
            return "$50.00-$100.00"
        else:
            return "$100.00+"
    
    def analyze_streak_patterns(
        self,
        lootbox: Lootbox,
        num_simulations: int = 10000,
        min_value_threshold: float = None
    ) -> Dict[str, any]:
        """
        Analyze winning and losing streaks
        
        Args:
            lootbox: Lootbox configuration
            num_simulations: Number of simulations
            min_value_threshold: Minimum value to consider a "win" (default: lootbox cost)
            
        Returns:
            Streak analysis data
        """
        if min_value_threshold is None:
            min_value_threshold = lootbox.cost
        
        # Simulate outcomes
        outcomes = []
        for _ in range(num_simulations):
            item = self.simulate_single_opening(lootbox)
            outcomes.append(item.value >= min_value_threshold)
        
        # Analyze streaks
        win_streaks = []
        loss_streaks = []
        current_streak = 0
        current_is_win = None
        
        for outcome in outcomes:
            if current_is_win is None:
                current_is_win = outcome
                current_streak = 1
            elif outcome == current_is_win:
                current_streak += 1
            else:
                # Streak ended
                if current_is_win:
                    win_streaks.append(current_streak)
                else:
                    loss_streaks.append(current_streak)
                
                current_is_win = outcome
                current_streak = 1
        
        # Add final streak
        if current_is_win is not None:
            if current_is_win:
                win_streaks.append(current_streak)
            else:
                loss_streaks.append(current_streak)
        
        return {
            "total_wins": sum(outcomes),
            "total_losses": len(outcomes) - sum(outcomes),
            "win_rate": sum(outcomes) / len(outcomes),
            "max_win_streak": max(win_streaks) if win_streaks else 0,
            "max_loss_streak": max(loss_streaks) if loss_streaks else 0,
            "avg_win_streak": statistics.mean(win_streaks) if win_streaks else 0,
            "avg_loss_streak": statistics.mean(loss_streaks) if loss_streaks else 0,
            "num_win_streaks": len(win_streaks),
            "num_loss_streaks": len(loss_streaks)
        }
    
    def calculate_confidence_intervals(
        self,
        lootbox: Lootbox,
        num_simulations: int = 10000,
        confidence_level: float = 0.95
    ) -> Dict[str, Tuple[float, float]]:
        """
        Calculate confidence intervals for key metrics
        
        Args:
            lootbox: Lootbox configuration
            num_simulations: Number of simulations
            confidence_level: Confidence level (0.95 = 95%)
            
        Returns:
            Dictionary with confidence intervals
        """
        # Run multiple simulation batches
        batch_size = 1000
        num_batches = num_simulations // batch_size
        
        batch_results = {
            'expected_values': [],
            'house_edges': [],
            'std_deviations': [],
            'profit_probabilities': []
        }
        
        for _ in range(num_batches):
            result = self.simulate_multiple_openings(lootbox, batch_size, show_progress=False)
            batch_results['expected_values'].append(result.average_value_per_box)
            batch_results['house_edges'].append(result.house_edge_actual)
            batch_results['std_deviations'].append(result.std_deviation)
            batch_results['profit_probabilities'].append(result.profit_probability)
        
        # Calculate confidence intervals
        alpha = 1 - confidence_level
        intervals = {}
        
        for metric, values in batch_results.items():
            lower_percentile = (alpha / 2) * 100
            upper_percentile = (1 - alpha / 2) * 100
            
            lower_bound = np.percentile(values, lower_percentile)
            upper_bound = np.percentile(values, upper_percentile)
            
            intervals[metric] = (lower_bound, upper_bound)
        
        return intervals
    
    def validate_theoretical_probabilities(
        self,
        lootbox: Lootbox,
        num_simulations: int = 100000,
        tolerance: float = 0.01
    ) -> Dict[str, bool]:
        """
        Validate that simulation results match theoretical probabilities
        
        Args:
            lootbox: Lootbox configuration
            num_simulations: Number of simulations
            tolerance: Acceptable deviation from theoretical values
            
        Returns:
            Dictionary indicating which metrics passed validation
        """
        result = self.simulate_multiple_openings(lootbox, num_simulations, show_progress=True)
        
        # Check expected value
        theoretical_ev = lootbox.get_expected_value()
        actual_ev = result.average_value_per_box
        ev_valid = abs(theoretical_ev - actual_ev) / theoretical_ev < tolerance
        
        # Check house edge
        theoretical_he = lootbox.get_house_edge()
        actual_he = result.house_edge_actual
        he_valid = abs(theoretical_he - actual_he) < tolerance
        
        # Check rarity distributions
        rarity_valid = {}
        for rarity in RarityTier:
            theoretical_prob = lootbox.get_probability_by_rarity(rarity)
            actual_count = result.rarity_distribution.get(rarity.value, 0)
            actual_prob = actual_count / num_simulations
            
            if theoretical_prob > 0:
                deviation = abs(theoretical_prob - actual_prob) / theoretical_prob
                rarity_valid[rarity.value] = deviation < tolerance
            else:
                rarity_valid[rarity.value] = actual_count == 0
        
        return {
            "expected_value_valid": ev_valid,
            "house_edge_valid": he_valid,
            "theoretical_ev": theoretical_ev,
            "actual_ev": actual_ev,
            "theoretical_he": theoretical_he,
            "actual_he": actual_he,
            "rarity_validations": rarity_valid,
            "overall_valid": ev_valid and he_valid and all(rarity_valid.values())
        }
