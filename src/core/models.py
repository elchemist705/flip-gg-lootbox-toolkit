"""
Core data models for lootbox probability calculations
"""
from enum import Enum
from typing import List, Dict, Optional, Union
from pydantic import BaseModel, Field, validator
from decimal import Decimal, ROUND_HALF_UP
import json
import logging

logger = logging.getLogger(__name__)


class RarityTier(str, Enum):
    """Standard rarity tiers for lootbox items"""
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"
    MYTHIC = "mythic"


class LootboxItem(BaseModel):
    """
    Represents a single item that can be obtained from a lootbox
    """
    name: str = Field(..., description="Item name")
    value: float = Field(..., gt=0, description="Item value in USD")
    rarity: RarityTier = Field(..., description="Item rarity tier")
    probability: float = Field(..., ge=0, le=1, description="Probability of obtaining this item")
    description: Optional[str] = Field(None, description="Item description")
    
    @validator('probability')
    def validate_probability(cls, v):
        """Ensure probability is valid"""
        if not 0 <= v <= 1:
            raise ValueError('Probability must be between 0 and 1')
        return v
    
    @validator('value')
    def validate_value(cls, v):
        """Ensure value is positive"""
        if v <= 0:
            raise ValueError('Item value must be positive')
        return v
    
    def __str__(self):
        return f"{self.name} ({self.rarity.value}) - ${self.value:.2f} ({self.probability*100:.2f}%)"


class Lootbox(BaseModel):
    """
    Represents a complete lootbox configuration
    """
    name: str = Field(..., description="Lootbox name")
    description: Optional[str] = Field(None, description="Lootbox description")
    cost: float = Field(..., ge=0.5, le=1000.0, description="Lootbox cost in USD")
    items: List[LootboxItem] = Field(..., min_items=1, description="Items in the lootbox")
    
    @validator('items')
    def validate_items(cls, v):
        """Validate items list and probabilities"""
        if not v:
            raise ValueError('Lootbox must contain at least one item')
        
        # Check total probability
        total_prob = sum(item.probability for item in v)
        if abs(total_prob - 1.0) > 1e-6:
            raise ValueError(f'Total probability must equal 1.0, got {total_prob:.6f}')
        
        # Check for duplicate names
        names = [item.name for item in v]
        if len(names) != len(set(names)):
            raise ValueError('Item names must be unique')
        
        return v
    
    @validator('cost')
    def validate_cost(cls, v):
        """Ensure cost is within acceptable range"""
        if not 0.5 <= v <= 1000.0:
            raise ValueError('Lootbox cost must be between $0.50 and $1000.00')
        return v
    
    def get_expected_value(self) -> float:
        """Calculate the expected value of the lootbox"""
        return sum(item.value * item.probability for item in self.items)
    
    def get_house_edge(self) -> float:
        """Calculate the house edge (negative value indicates player advantage)"""
        return (self.cost - self.get_expected_value()) / self.cost
    
    def get_items_by_rarity(self, rarity: RarityTier) -> List[LootboxItem]:
        """Get all items of a specific rarity"""
        return [item for item in self.items if item.rarity == rarity]
    
    def get_probability_by_rarity(self, rarity: RarityTier) -> float:
        """Get total probability for a specific rarity tier"""
        return sum(item.probability for item in self.get_items_by_rarity(rarity))
    
    def get_avg_value_by_rarity(self, rarity: RarityTier) -> float:
        """Get average value for a specific rarity tier"""
        items = self.get_items_by_rarity(rarity)
        if not items:
            return 0.0
        total_prob = sum(item.probability for item in items)
        if total_prob == 0:
            return 0.0
        return sum(item.value * item.probability for item in items) / total_prob
    
    def normalize_probabilities(self):
        """Normalize all item probabilities to sum to 1.0"""
        total_prob = sum(item.probability for item in self.items)
        if total_prob > 0:
            for item in self.items:
                item.probability = item.probability / total_prob
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "name": self.name,
            "description": self.description,
            "cost": self.cost,
            "items": [item.dict() for item in self.items]
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Lootbox':
        """Create Lootbox from dictionary"""
        items = [LootboxItem(**item_data) for item_data in data.get('items', [])]
        return cls(
            name=data['name'],
            description=data.get('description'),
            cost=data['cost'],
            items=items
        )
    
    def save_to_file(self, filepath: str):
        """Save lootbox configuration to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
        logger.info(f"Lootbox saved to {filepath}")
    
    @classmethod
    def load_from_file(cls, filepath: str) -> 'Lootbox':
        """Load lootbox configuration from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)


class SimulationResult(BaseModel):
    """
    Results from a Monte Carlo simulation
    """
    lootbox_name: str
    num_simulations: int
    total_cost: float
    total_value_received: float
    average_value_per_box: float
    median_value_per_box: float
    std_deviation: float
    profit_probability: float
    break_even_probability: float
    house_edge_actual: float
    house_edge_theoretical: float
    value_distribution: Dict[str, int]
    rarity_distribution: Dict[str, int]
    
    def get_roi(self) -> float:
        """Calculate return on investment"""
        if self.total_cost == 0:
            return 0.0
        return ((self.total_value_received - self.total_cost) / self.total_cost) * 100
    
    def get_win_rate(self) -> float:
        """Calculate percentage of profitable outcomes"""
        return self.profit_probability * 100


class OptimizationConstraints(BaseModel):
    """
    Constraints for lootbox probability optimization
    """
    min_cost: float = Field(0.5, description="Minimum lootbox cost")
    max_cost: float = Field(1000.0, description="Maximum lootbox cost")
    target_house_edge: Optional[float] = Field(None, ge=0, le=1, description="Target house edge (0-1)")
    min_house_edge: float = Field(0.05, ge=0, le=1, description="Minimum house edge")
    max_house_edge: float = Field(0.50, ge=0, le=1, description="Maximum house edge")
    min_probability_per_tier: Dict[str, float] = Field(
        default_factory=lambda: {
            RarityTier.COMMON.value: 0.3,
            RarityTier.UNCOMMON.value: 0.1,
            RarityTier.RARE.value: 0.01,
            RarityTier.EPIC.value: 0.001,
            RarityTier.LEGENDARY.value: 0.0001,
            RarityTier.MYTHIC.value: 0.00001
        },
        description="Minimum probability for each rarity tier"
    )
    max_probability_per_tier: Dict[str, float] = Field(
        default_factory=lambda: {
            RarityTier.COMMON.value: 0.8,
            RarityTier.UNCOMMON.value: 0.4,
            RarityTier.RARE.value: 0.1,
            RarityTier.EPIC.value: 0.05,
            RarityTier.LEGENDARY.value: 0.01,
            RarityTier.MYTHIC.value: 0.001
        },
        description="Maximum probability for each rarity tier"
    )
    
    @validator('min_probability_per_tier', 'max_probability_per_tier')
    def validate_tier_probabilities(cls, v):
        """Validate rarity tier probabilities"""
        for tier, prob in v.items():
            if not 0 <= prob <= 1:
                raise ValueError(f'Probability for {tier} must be between 0 and 1')
        return v


class LootboxAnalytics(BaseModel):
    """
    Analytics data for a lootbox configuration
    """
    lootbox_name: str
    expected_value: float
    house_edge: float
    variance: float
    standard_deviation: float
    coefficient_of_variation: float
    sharpe_ratio: Optional[float]
    rarity_breakdown: Dict[str, Dict[str, Union[int, float]]]
    value_percentiles: Dict[str, float]
    
    def get_risk_level(self) -> str:
        """Categorize risk level based on variance"""
        cv = self.coefficient_of_variation
        if cv < 0.5:
            return "Low Risk"
        elif cv < 1.0:
            return "Medium Risk" 
        elif cv < 2.0:
            return "High Risk"
        else:
            return "Very High Risk"
    
    def get_player_value_rating(self) -> str:
        """Rate the value proposition for players"""
        house_edge = self.house_edge
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
