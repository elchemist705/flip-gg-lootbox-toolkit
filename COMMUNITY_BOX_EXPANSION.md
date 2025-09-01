# Community Box Expansion - Enhanced Item Variety

## Overview
The lootbox toolkit has been expanded to support **8-12 items per community box** (up from the previous 4-6 item limit), providing much more variety and granular prize tiers for better player engagement.

## Changes Made

### 📈 Item Count Expansion
- **Low Variance**: 4 → 8 items (100% increase)
- **Medium Variance**: 5 → 9 items (80% increase)  
- **High Variance**: 5-6 → 11-12 items (100%+ increase)

### 🎯 Enhanced Configurations

#### Low Variance (8 items)
- More consistent prize structure with expanded tiers
- Better distribution of value around the box cost
- Reduced volatility for casual players

#### Medium Variance (9 items)
- Balanced excitement with granular prize tiers
- Smooth progression from common to mythic items
- Optimal for mainstream appeal

#### High Variance (11-12 items)
- Maximum variety with extreme distribution
- Multiple cost scaling tiers:
  - Standard ($0.50-$10.00): 11 items
  - Whale tier ($10.01-$100.00): 11 items
  - Luxury tier ($100.01-$1000.00): 12 items

### 🔧 Technical Improvements

1. **Probability Validation**: Added automatic validation to ensure probabilities sum to 1.0
2. **Auto-normalization**: Automatic correction if probability distributions are slightly off
3. **Enhanced Display**: Updated UI to show total item count prominently
4. **Template Expansion**: Added new community box templates with 10+ items

### 📊 New Templates Added

1. **Community Expanded Box** (11 items)
   - Cost: $1.50
   - Focus: Community engagement with variety
   - House Edge Target: 15%

2. **Mega Variety Community Box** (12 items)
   - Cost: $2.50
   - Focus: Maximum variety and excitement
   - House Edge Target: 18%

## Usage

### Interactive Script
```bash
python3 bin/flip_gg_interactive.py
```

The script now shows item counts in the variance selection:
- `1. Low variance - Consistent, predictable outcomes (8 items)`
- `2. Medium variance - Balanced excitement (9 items)`
- `3. High variance - Big wins, big losses (11-12 items)`

### Demo Script
```bash
python3 examples/demo_expanded_community_boxes.py
```

## Configuration Files

Updated `configs/templates.json` with:
- Increased `max_items` from 10 to 15
- Added `recommended_items` configuration
- New community box templates with expanded variety

## Validation

All configurations have been tested to ensure:
- ✅ Probabilities sum to exactly 1.0
- ✅ House edge calculations remain accurate
- ✅ Performance is optimized for larger item sets
- ✅ Display formatting handles increased item counts properly

## Benefits

1. **Player Engagement**: More granular prize tiers create better psychological rewards
2. **Community Appeal**: Expanded variety makes boxes more interesting for community events
3. **Flexible Scaling**: Configurations adapt better to different cost ranges
4. **Improved Balance**: Better distribution of risk across more prize tiers
