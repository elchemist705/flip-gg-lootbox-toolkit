"""
Expected Value Calculator for Lootbox Analysis

Provides comprehensive mathematical analysis of lootbox configurations
including expected value, variance, and risk metrics.
"""
import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional, Union
import math
import statistics
from decimal import Decimal, ROUND_HALF_UP
import logging

from ..core.models import Lootbox, LootboxItem, RarityTier, LootboxAnalytics

logger = logging.getLogger(__name__)


class ExpectedValueCalculator:
    """
    Advanced calculator for lootbox expected value and statistical analysis
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def calculate_expected_value(self, lootbox: Lootbox) -> float:
        """
        Calculate the expected value (mathematical expectation) of a lootbox
        
        Args:
            lootbox: Lootbox configuration
            
        Returns:
            Expected value in USD
        """
        return sum(item.value * item.probability for item in lootbox.items)
    
    def calculate_variance(self, lootbox: Lootbox) -> float:
        """
        Calculate the variance of lootbox outcomes
        
        Args:
            lootbox: Lootbox configuration
            
        Returns:
            Variance value
        """
        expected_value = self.calculate_expected_value(lootbox)
        variance = sum(
            item.probability * (item.value - expected_value) ** 2
            for item in lootbox.items
        )
        return variance
    
    def calculate_standard_deviation(self, lootbox: Lootbox) -> float:
        """
        Calculate standard deviation of lootbox outcomes
        
        Args:
            lootbox: Lootbox configuration
            
        Returns:
            Standard deviation
        """
        return math.sqrt(self.calculate_variance(lootbox))
    
    def calculate_coefficient_of_variation(self, lootbox: Lootbox) -> float:
        """
        Calculate coefficient of variation (relative standard deviation)
        
        Args:
            lootbox: Lootbox configuration
            
        Returns:
            Coefficient of variation
        """
        expected_value = self.calculate_expected_value(lootbox)
        if expected_value == 0:
            return float('inf')
        
        std_dev = self.calculate_standard_deviation(lootbox)
        return std_dev / expected_value
    
    def calculate_house_edge(self, lootbox: Lootbox) -> float:
        """
        Calculate house edge (casino advantage)
        
        Args:
            lootbox: Lootbox configuration
            
        Returns:
            House edge as decimal (0.1 = 10% house edge)
        """
        expected_value = self.calculate_expected_value(lootbox)
        return (lootbox.cost - expected_value) / lootbox.cost
    
    def calculate_sharpe_ratio(self, lootbox: Lootbox, risk_free_rate: float = 0.0) -> float:
        """
        Calculate Sharpe ratio for risk-adjusted returns
        
        Args:
            lootbox: Lootbox configuration
            risk_free_rate: Risk-free return rate
            
        Returns:
            Sharpe ratio
        """
        expected_return = (self.calculate_expected_value(lootbox) - lootbox.cost) / lootbox.cost
        std_dev = self.calculate_standard_deviation(lootbox) / lootbox.cost
        
        if std_dev == 0:
            return float('inf') if expected_return > risk_free_rate else float('-inf')
        
        return (expected_return - risk_free_rate) / std_dev
    
    def calculate_value_percentiles(self, lootbox: Lootbox, percentiles: List[float] = None) -> Dict[str, float]:
        """
        Calculate value percentiles for the lootbox
        
        Args:
            lootbox: Lootbox configuration
            percentiles: List of percentiles to calculate (default: [5, 10, 25, 50, 75, 90, 95])
            
        Returns:
            Dictionary mapping percentile names to values
        """
        if percentiles is None:
            percentiles = [5, 10, 25, 50, 75, 90, 95]
        
        # Create value array weighted by probability
        values = []
        probabilities = []
        
        for item in lootbox.items:
            values.append(item.value)
            probabilities.append(item.probability)
        
        # Sort by value
        sorted_data = sorted(zip(values, probabilities))
        sorted_values, sorted_probs = zip(*sorted_data)
        
        # Calculate cumulative probabilities
        cumulative_probs = np.cumsum(sorted_probs)
        
        result = {}
        for p in percentiles:
            target_prob = p / 100.0
            
            # Find the value at this percentile
            idx = np.searchsorted(cumulative_probs, target_prob, side='right')
            if idx < len(sorted_values):
                result[f"p{p}"] = sorted_values[idx]
            else:
                result[f"p{p}"] = sorted_values[-1]
        
        return result
    
    def analyze_rarity_breakdown(self, lootbox: Lootbox) -> Dict[str, Dict[str, Union[int, float]]]:
        """
        Analyze the distribution of items by rarity tier
        
        Args:
            lootbox: Lootbox configuration
            
        Returns:
            Dictionary with rarity analysis data
        """
        breakdown = {}
        
        for rarity in RarityTier:
            items = lootbox.get_items_by_rarity(rarity)
            total_prob = sum(item.probability for item in items)
            
            if items:
                avg_value = sum(item.value * item.probability for item in items) / total_prob if total_prob > 0 else 0
                min_value = min(item.value for item in items)
                max_value = max(item.value for item in items)
                
                breakdown[rarity.value] = {
                    "item_count": len(items),
                    "total_probability": total_prob,
                    "average_value": avg_value,
                    "min_value": min_value,
                    "max_value": max_value,
                    "expected_contribution": sum(item.value * item.probability for item in items)
                }
            else:
                breakdown[rarity.value] = {
                    "item_count": 0,
                    "total_probability": 0.0,
                    "average_value": 0.0,
                    "min_value": 0.0,
                    "max_value": 0.0,
                    "expected_contribution": 0.0
                }
        
        return breakdown
    
    def calculate_break_even_probability(self, lootbox: Lootbox) -> float:
        """
        Calculate probability of getting items worth at least the lootbox cost
        
        Args:
            lootbox: Lootbox configuration
            
        Returns:
            Probability of breaking even or profiting
        """
        break_even_prob = 0.0
        
        for item in lootbox.items:
            if item.value >= lootbox.cost:
                break_even_prob += item.probability
        
        return break_even_prob
    
    def calculate_profit_probability(self, lootbox: Lootbox, min_profit_margin: float = 0.0) -> float:
        """
        Calculate probability of getting items worth more than cost + margin
        
        Args:
            lootbox: Lootbox configuration
            min_profit_margin: Minimum profit margin (0.1 = 10% profit)
            
        Returns:
            Probability of achieving target profit
        """
        target_value = lootbox.cost * (1 + min_profit_margin)
        profit_prob = 0.0
        
        for item in lootbox.items:
            if item.value >= target_value:
                profit_prob += item.probability
        
        return profit_prob
    
    def generate_full_analysis(self, lootbox: Lootbox) -> LootboxAnalytics:
        """
        Generate comprehensive analytics for a lootbox
        
        Args:
            lootbox: Lootbox configuration
            
        Returns:
            Complete analytics object
        """
        expected_value = self.calculate_expected_value(lootbox)
        variance = self.calculate_variance(lootbox)
        std_deviation = self.calculate_standard_deviation(lootbox)
        house_edge = self.calculate_house_edge(lootbox)
        
        # Calculate coefficient of variation
        cv = self.calculate_coefficient_of_variation(lootbox)
        
        # Calculate Sharpe ratio
        sharpe_ratio = self.calculate_sharpe_ratio(lootbox)
        
        # Get rarity breakdown
        rarity_breakdown = self.analyze_rarity_breakdown(lootbox)
        
        # Calculate value percentiles
        value_percentiles = self.calculate_value_percentiles(lootbox)
        
        return LootboxAnalytics(
            lootbox_name=lootbox.name,
            expected_value=expected_value,
            house_edge=house_edge,
            variance=variance,
            standard_deviation=std_deviation,
            coefficient_of_variation=cv,
            sharpe_ratio=sharpe_ratio,
            rarity_breakdown=rarity_breakdown,
            value_percentiles=value_percentiles
        )
    
    def compare_lootboxes(self, lootboxes: List[Lootbox]) -> pd.DataFrame:
        """
        Compare multiple lootbox configurations
        
        Args:
            lootboxes: List of lootbox configurations
            
        Returns:
            DataFrame with comparison metrics
        """
        comparison_data = []
        
        for lootbox in lootboxes:
            analytics = self.generate_full_analysis(lootbox)
            
            row = {
                "Name": lootbox.name,
                "Cost": f"${lootbox.cost:.2f}",
                "Expected Value": f"${analytics.expected_value:.4f}",
                "House Edge": f"{analytics.house_edge*100:.2f}%",
                "Std Deviation": f"${analytics.standard_deviation:.4f}",
                "CV": f"{analytics.coefficient_of_variation:.2f}",
                "Risk Level": analytics.get_risk_level(),
                "Player Rating": analytics.get_player_value_rating(),
                "Break Even Prob": f"{self.calculate_break_even_probability(lootbox)*100:.2f}%"
            }
            comparison_data.append(row)
        
        return pd.DataFrame(comparison_data)
    
    def optimize_for_target_house_edge(self, lootbox: Lootbox, target_house_edge: float) -> float:
        """
        Calculate optimal lootbox cost for a target house edge
        
        Args:
            lootbox: Lootbox configuration
            target_house_edge: Desired house edge (0.1 = 10%)
            
        Returns:
            Optimal cost for target house edge
        """
        expected_value = self.calculate_expected_value(lootbox)
        
        # House edge = (cost - expected_value) / cost
        # Solving for cost: cost = expected_value / (1 - target_house_edge)
        if target_house_edge >= 1.0:
            raise ValueError("Target house edge must be less than 100%")
        
        optimal_cost = expected_value / (1 - target_house_edge)
        
        # Clamp to acceptable range
        optimal_cost = max(0.5, min(4.0, optimal_cost))
        
        return optimal_cost
    
    def calculate_roi_distribution(self, lootbox: Lootbox) -> Dict[str, float]:
        """
        Calculate distribution of ROI outcomes
        
        Args:
            lootbox: Lootbox configuration
            
        Returns:
            Dictionary with ROI statistics
        """
        roi_values = []
        probabilities = []
        
        for item in lootbox.items:
            roi = (item.value - lootbox.cost) / lootbox.cost
            roi_values.append(roi)
            probabilities.append(item.probability)
        
        # Calculate weighted statistics
        expected_roi = sum(roi * prob for roi, prob in zip(roi_values, probabilities))
        
        # Calculate variance of ROI
        roi_variance = sum(
            prob * (roi - expected_roi) ** 2
            for roi, prob in zip(roi_values, probabilities)
        )
        
        roi_std = math.sqrt(roi_variance)
        
        # Calculate percentiles
        sorted_data = sorted(zip(roi_values, probabilities))
        sorted_roi, sorted_probs = zip(*sorted_data)
        cumulative_probs = np.cumsum(sorted_probs)
        
        percentiles = {}
        for p in [5, 10, 25, 50, 75, 90, 95]:
            target_prob = p / 100.0
            idx = np.searchsorted(cumulative_probs, target_prob, side='right')
            if idx < len(sorted_roi):
                percentiles[f"p{p}"] = sorted_roi[idx] * 100  # Convert to percentage
        
        return {
            "expected_roi_percent": expected_roi * 100,
            "roi_std_percent": roi_std * 100,
            "min_roi_percent": min(roi_values) * 100,
            "max_roi_percent": max(roi_values) * 100,
            **percentiles
        }
