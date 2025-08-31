"""
Probability Optimizer for Lootbox Design

Uses mathematical optimization techniques to find optimal probability distributions
for lootbox items based on various constraints and objectives.
"""
import numpy as np
from scipy.optimize import minimize, LinearConstraint, Bounds
from typing import List, Dict, Tuple, Optional, Callable
import logging
from dataclasses import dataclass

from ..core.models import Lootbox, LootboxItem, RarityTier, OptimizationConstraints
from ..calculator.expected_value import ExpectedValueCalculator

logger = logging.getLogger(__name__)


@dataclass
class OptimizationResult:
    """Result of probability optimization"""
    success: bool
    optimized_lootbox: Optional[Lootbox]
    original_house_edge: float
    optimized_house_edge: float
    original_expected_value: float
    optimized_expected_value: float
    optimization_message: str
    iterations: int


class ProbabilityOptimizer:
    """
    Advanced probability optimizer for lootbox configurations
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.calculator = ExpectedValueCalculator()
    
    def optimize_for_house_edge(
        self,
        lootbox: Lootbox,
        target_house_edge: float,
        constraints: OptimizationConstraints = None
    ) -> OptimizationResult:
        """
        Optimize lootbox probabilities to achieve target house edge
        
        Args:
            lootbox: Base lootbox configuration
            target_house_edge: Target house edge (0.1 = 10%)
            constraints: Optimization constraints
            
        Returns:
            Optimization result
        """
        if constraints is None:
            constraints = OptimizationConstraints()
        
        # Calculate original metrics
        original_ev = lootbox.get_expected_value()
        original_he = lootbox.get_house_edge()
        
        # Set up optimization problem
        n_items = len(lootbox.items)
        item_values = np.array([item.value for item in lootbox.items])
        
        # Objective: minimize deviation from target house edge
        def objective(probabilities):
            expected_value = np.dot(probabilities, item_values)
            house_edge = (lootbox.cost - expected_value) / lootbox.cost
            return (house_edge - target_house_edge) ** 2
        
        # Constraints
        constraints_list = []
        
        # Probabilities must sum to 1
        constraints_list.append(LinearConstraint(
            np.ones(n_items), 1.0, 1.0
        ))
        
        # Individual probability bounds
        lower_bounds = []
        upper_bounds = []
        
        for item in lootbox.items:
            rarity_key = item.rarity.value
            min_prob = constraints.min_probability_per_tier.get(rarity_key, 0.0)
            max_prob = constraints.max_probability_per_tier.get(rarity_key, 1.0)
            
            lower_bounds.append(min_prob)
            upper_bounds.append(max_prob)
        
        bounds = Bounds(lower_bounds, upper_bounds)
        
        # Initial guess (current probabilities)
        initial_probs = np.array([item.probability for item in lootbox.items])
        
        # Optimize
        try:
            result = minimize(
                objective,
                initial_probs,
                method='SLSQP',
                bounds=bounds,
                constraints=constraints_list,
                options={'maxiter': 1000, 'ftol': 1e-9}
            )
            
            if result.success:
                # Create optimized lootbox
                optimized_items = []
                for i, item in enumerate(lootbox.items):
                    optimized_item = LootboxItem(
                        name=item.name,
                        value=item.value,
                        rarity=item.rarity,
                        probability=float(result.x[i]),
                        description=item.description
                    )
                    optimized_items.append(optimized_item)
                
                optimized_lootbox = Lootbox(
                    name=f"{lootbox.name} (Optimized)",
                    description=f"Optimized for {target_house_edge*100:.1f}% house edge",
                    cost=lootbox.cost,
                    items=optimized_items
                )
                
                optimized_ev = optimized_lootbox.get_expected_value()
                optimized_he = optimized_lootbox.get_house_edge()
                
                return OptimizationResult(
                    success=True,
                    optimized_lootbox=optimized_lootbox,
                    original_house_edge=original_he,
                    optimized_house_edge=optimized_he,
                    original_expected_value=original_ev,
                    optimized_expected_value=optimized_ev,
                    optimization_message=f"Successfully optimized to {optimized_he*100:.2f}% house edge",
                    iterations=result.nit
                )
            else:
                return OptimizationResult(
                    success=False,
                    optimized_lootbox=None,
                    original_house_edge=original_he,
                    optimized_house_edge=original_he,
                    original_expected_value=original_ev,
                    optimized_expected_value=original_ev,
                    optimization_message=f"Optimization failed: {result.message}",
                    iterations=result.nit if hasattr(result, 'nit') else 0
                )
        
        except Exception as e:
            self.logger.error(f"Optimization error: {str(e)}")
            return OptimizationResult(
                success=False,
                optimized_lootbox=None,
                original_house_edge=original_he,
                optimized_house_edge=original_he,
                original_expected_value=original_ev,
                optimized_expected_value=original_ev,
                optimization_message=f"Optimization error: {str(e)}",
                iterations=0
            )
    
    def optimize_for_cost_range(
        self,
        items: List[LootboxItem],
        min_cost: float = 0.5,
        max_cost: float = 1000.0,
        target_house_edge: float = 0.15,
        constraints: OptimizationConstraints = None
    ) -> List[OptimizationResult]:
        """
        Optimize lootbox for different cost points within a range
        
        Args:
            items: List of available items
            min_cost: Minimum cost to test
            max_cost: Maximum cost to test
            target_house_edge: Target house edge
            constraints: Optimization constraints
            
        Returns:
            List of optimization results for different cost points
        """
        if constraints is None:
            constraints = OptimizationConstraints()
        
        results = []
        cost_points = np.linspace(min_cost, max_cost, 10)
        
        for cost in cost_points:
            # Create temporary lootbox with equal probabilities
            temp_items = []
            equal_prob = 1.0 / len(items)
            
            for item in items:
                temp_items.append(LootboxItem(
                    name=item.name,
                    value=item.value,
                    rarity=item.rarity,
                    probability=equal_prob,
                    description=item.description
                ))
            
            temp_lootbox = Lootbox(
                name=f"Temp Box ${cost:.2f}",
                cost=cost,
                items=temp_items
            )
            
            # Optimize this configuration
            result = self.optimize_for_house_edge(temp_lootbox, target_house_edge, constraints)
            results.append(result)
        
        return results
    
    def genetic_algorithm_optimization(
        self,
        items: List[LootboxItem],
        cost: float,
        target_house_edge: float,
        population_size: int = 100,
        generations: int = 500,
        mutation_rate: float = 0.1,
        constraints: OptimizationConstraints = None
    ) -> OptimizationResult:
        """
        Use genetic algorithm for probability optimization
        
        Args:
            items: List of available items
            cost: Lootbox cost
            target_house_edge: Target house edge
            population_size: Size of genetic algorithm population
            generations: Number of generations to evolve
            mutation_rate: Probability of mutation
            constraints: Optimization constraints
            
        Returns:
            Optimization result
        """
        if constraints is None:
            constraints = OptimizationConstraints()
        
        n_items = len(items)
        item_values = np.array([item.value for item in items])
        
        # Initialize population
        population = []
        for _ in range(population_size):
            # Generate random probabilities that sum to 1
            probs = np.random.exponential(1.0, n_items)
            probs = probs / np.sum(probs)
            
            # Apply constraints
            for i, item in enumerate(items):
                rarity_key = item.rarity.value
                min_prob = constraints.min_probability_per_tier.get(rarity_key, 0.0)
                max_prob = constraints.max_probability_per_tier.get(rarity_key, 1.0)
                probs[i] = np.clip(probs[i], min_prob, max_prob)
            
            # Renormalize
            probs = probs / np.sum(probs)
            population.append(probs)
        
        # Fitness function
        def fitness(probabilities):
            expected_value = np.dot(probabilities, item_values)
            house_edge = (cost - expected_value) / cost
            return -abs(house_edge - target_house_edge)  # Minimize deviation
        
        best_individual = None
        best_fitness = float('-inf')
        
        for generation in range(generations):
            # Evaluate fitness
            fitness_scores = [fitness(individual) for individual in population]
            
            # Track best
            gen_best_idx = np.argmax(fitness_scores)
            if fitness_scores[gen_best_idx] > best_fitness:
                best_fitness = fitness_scores[gen_best_idx]
                best_individual = population[gen_best_idx].copy()
            
            # Selection (tournament selection)
            new_population = []
            for _ in range(population_size):
                tournament_indices = np.random.choice(population_size, 3, replace=False)
                tournament_fitness = [fitness_scores[i] for i in tournament_indices]
                winner_idx = tournament_indices[np.argmax(tournament_fitness)]
                new_population.append(population[winner_idx].copy())
            
            # Crossover and mutation
            for i in range(0, population_size - 1, 2):
                if np.random.random() < 0.8:  # Crossover probability
                    # Single-point crossover
                    crossover_point = np.random.randint(1, n_items)
                    child1 = np.concatenate([
                        new_population[i][:crossover_point],
                        new_population[i+1][crossover_point:]
                    ])
                    child2 = np.concatenate([
                        new_population[i+1][:crossover_point],
                        new_population[i][crossover_point:]
                    ])
                    
                    # Normalize
                    child1 = child1 / np.sum(child1)
                    child2 = child2 / np.sum(child2)
                    
                    new_population[i] = child1
                    new_population[i+1] = child2
                
                # Mutation
                for j in [i, i+1]:
                    if j < len(new_population) and np.random.random() < mutation_rate:
                        # Add small random noise
                        noise = np.random.normal(0, 0.01, n_items)
                        new_population[j] += noise
                        new_population[j] = np.clip(new_population[j], 0.001, 1.0)
                        new_population[j] = new_population[j] / np.sum(new_population[j])
            
            population = new_population
        
        # Create optimized lootbox from best individual
        optimized_items = []
        for i, item in enumerate(items):
            optimized_item = LootboxItem(
                name=item.name,
                value=item.value,
                rarity=item.rarity,
                probability=float(best_individual[i]),
                description=item.description
            )
            optimized_items.append(optimized_item)
        
        optimized_lootbox = Lootbox(
            name=f"GA Optimized Box ${cost:.2f}",
            description=f"Genetic algorithm optimized for {target_house_edge*100:.1f}% house edge",
            cost=cost,
            items=optimized_items
        )
        
        # Create temporary original lootbox for comparison
        original_items = []
        equal_prob = 1.0 / len(items)
        for item in items:
            original_items.append(LootboxItem(
                name=item.name,
                value=item.value,
                rarity=item.rarity,
                probability=equal_prob,
                description=item.description
            ))
        
        original_lootbox = Lootbox(
            name="Original",
            cost=cost,
            items=original_items
        )
        
        return OptimizationResult(
            success=True,
            optimized_lootbox=optimized_lootbox,
            original_house_edge=original_lootbox.get_house_edge(),
            optimized_house_edge=optimized_lootbox.get_house_edge(),
            original_expected_value=original_lootbox.get_expected_value(),
            optimized_expected_value=optimized_lootbox.get_expected_value(),
            optimization_message=f"Genetic algorithm completed after {generations} generations",
            iterations=generations
        )
    
    def find_optimal_cost(
        self,
        items: List[LootboxItem],
        probabilities: List[float],
        target_house_edge: float,
        min_cost: float = 0.5,
        max_cost: float = 4.0
    ) -> Tuple[float, bool]:
        """
        Find optimal cost for given items and probabilities to achieve target house edge
        
        Args:
            items: List of lootbox items
            probabilities: Probability for each item
            target_house_edge: Target house edge
            min_cost: Minimum allowed cost
            max_cost: Maximum allowed cost
            
        Returns:
            Tuple of (optimal_cost, is_feasible)
        """
        # Calculate expected value
        expected_value = sum(item.value * prob for item, prob in zip(items, probabilities))
        
        # Calculate optimal cost
        # house_edge = (cost - expected_value) / cost
        # target_house_edge = (cost - expected_value) / cost
        # cost * target_house_edge = cost - expected_value
        # cost * (1 - target_house_edge) = expected_value
        # cost = expected_value / (1 - target_house_edge)
        
        if target_house_edge >= 1.0:
            return max_cost, False
        
        optimal_cost = expected_value / (1 - target_house_edge)
        
        # Check if within bounds
        if min_cost <= optimal_cost <= max_cost:
            return optimal_cost, True
        else:
            # Return clamped value and indicate infeasibility
            clamped_cost = max(min_cost, min(max_cost, optimal_cost))
            return clamped_cost, False
    
    def optimize_rarity_distribution(
        self,
        items: List[LootboxItem],
        cost: float,
        target_metrics: Dict[str, float],
        constraints: OptimizationConstraints = None
    ) -> OptimizationResult:
        """
        Optimize probability distribution with focus on rarity tier balance
        
        Args:
            items: List of available items
            cost: Lootbox cost
            target_metrics: Target metrics (house_edge, variance, etc.)
            constraints: Optimization constraints
            
        Returns:
            Optimization result
        """
        if constraints is None:
            constraints = OptimizationConstraints()
        
        # Group items by rarity
        rarity_groups = {}
        for i, item in enumerate(items):
            if item.rarity not in rarity_groups:
                rarity_groups[item.rarity] = []
            rarity_groups[item.rarity].append(i)
        
        # Set up optimization
        n_items = len(items)
        item_values = np.array([item.value for item in items])
        
        # Multi-objective function
        def objective(probabilities):
            expected_value = np.dot(probabilities, item_values)
            house_edge = (cost - expected_value) / cost
            
            # Calculate variance
            variance = np.sum(probabilities * (item_values - expected_value) ** 2)
            
            # Objective components
            house_edge_error = (house_edge - target_metrics.get('house_edge', 0.15)) ** 2
            variance_error = (variance - target_metrics.get('variance', 1.0)) ** 2
            
            # Rarity distribution penalties
            rarity_penalty = 0.0
            for rarity, indices in rarity_groups.items():
                rarity_prob = sum(probabilities[i] for i in indices)
                target_prob = target_metrics.get(f'{rarity.value}_probability', 0.1)
                rarity_penalty += (rarity_prob - target_prob) ** 2
            
            return house_edge_error + 0.1 * variance_error + 0.1 * rarity_penalty
        
        # Set up constraints
        constraints_list = []
        
        # Probabilities sum to 1
        constraints_list.append(LinearConstraint(np.ones(n_items), 1.0, 1.0))
        
        # Rarity tier constraints
        for rarity, indices in rarity_groups.items():
            rarity_key = rarity.value
            min_total_prob = constraints.min_probability_per_tier.get(rarity_key, 0.0)
            max_total_prob = constraints.max_probability_per_tier.get(rarity_key, 1.0)
            
            # Create constraint matrix for this rarity
            constraint_matrix = np.zeros(n_items)
            for idx in indices:
                constraint_matrix[idx] = 1.0
            
            constraints_list.append(LinearConstraint(
                constraint_matrix, min_total_prob, max_total_prob
            ))
        
        # Individual bounds
        bounds = Bounds(
            [0.0001] * n_items,  # Minimum individual probability
            [1.0] * n_items      # Maximum individual probability
        )
        
        # Initial guess
        initial_probs = np.random.dirichlet(np.ones(n_items))
        
        # Optimize
        try:
            result = minimize(
                objective,
                initial_probs,
                method='SLSQP',
                bounds=bounds,
                constraints=constraints_list,
                options={'maxiter': 2000, 'ftol': 1e-9}
            )
            
            if result.success:
                # Create optimized lootbox
                optimized_items = []
                for i, item in enumerate(items):
                    optimized_item = LootboxItem(
                        name=item.name,
                        value=item.value,
                        rarity=item.rarity,
                        probability=float(result.x[i]),
                        description=item.description
                    )
                    optimized_items.append(optimized_item)
                
                optimized_lootbox = Lootbox(
                    name=f"Rarity Optimized ${cost:.2f}",
                    description="Optimized for balanced rarity distribution",
                    cost=cost,
                    items=optimized_items
                )
                
                return OptimizationResult(
                    success=True,
                    optimized_lootbox=optimized_lootbox,
                    original_house_edge=0.0,  # No original for comparison
                    optimized_house_edge=optimized_lootbox.get_house_edge(),
                    original_expected_value=0.0,
                    optimized_expected_value=optimized_lootbox.get_expected_value(),
                    optimization_message="Successfully optimized rarity distribution",
                    iterations=result.nit
                )
            else:
                return OptimizationResult(
                    success=False,
                    optimized_lootbox=None,
                    original_house_edge=0.0,
                    optimized_house_edge=0.0,
                    original_expected_value=0.0,
                    optimized_expected_value=0.0,
                    optimization_message=f"Rarity optimization failed: {result.message}",
                    iterations=result.nit if hasattr(result, 'nit') else 0
                )
        
        except Exception as e:
            self.logger.error(f"Rarity optimization error: {str(e)}")
            return OptimizationResult(
                success=False,
                optimized_lootbox=None,
                original_house_edge=0.0,
                optimized_house_edge=0.0,
                original_expected_value=0.0,
                optimized_expected_value=0.0,
                optimization_message=f"Rarity optimization error: {str(e)}",
                iterations=0
            )
