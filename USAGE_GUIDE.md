# 🎲 Flip.gg Lootbox Toolkit - Complete Usage Guide

## 🚀 Quick Start (3 Commands)

```bash
# 1. Install the toolkit
./install.sh

# 2. Design a lootbox interactively
./flip-gg-designer

# 3. Analyze existing configurations
./lootbox-calc
```

## 💰 Cost Range & Value Support

- **Cost Range**: $0.50 - $1000.00
- **Item Values**: $0.02 - $1000.00 (automatically capped)
- **Smart Scaling**: Tier-based value multipliers

## 🎮 Main Tools & How to Use Them

### 1. 🎯 Interactive Designer (`./flip-gg-designer`)

**Purpose**: Create custom lootboxes with guided prompts

```bash
./flip-gg-designer
```

**What it asks:**
- Lootbox cost ($0.50 - $1000.00)
- House edge strategy (Conservative/Balanced/Aggressive)  
- Risk level (Low/Medium/High variance)

**Example Session:**
```
💰 Enter lootbox cost: $25.00
🎯 Choose strategy: 2 (Balanced 15-20% house edge)
🎢 Choose variance: 3 (High variance)
```

**Output**: Optimized lootbox + JSON config + flip.gg implementation notes

### 2. 📊 Main Calculator (`./lootbox-calc`)

**Purpose**: Comprehensive analysis with cost comparisons

```bash
./lootbox-calc
```

**What it shows:**
- Cost comparison across multiple price points
- Detailed probability breakdown
- Monte Carlo simulation (25,000 runs)
- Optimization demonstration
- Saves recommended configurations

### 3. 🔧 CLI Toolkit (`bin/lootbox_toolkit`)

**Purpose**: Advanced operations and templates

#### Create from Templates:
```bash
# Budget friendly ($0.75)
bin/lootbox_toolkit create --name "Budget Box" --cost 0.75 --template balanced

# Whale tier ($100)
bin/lootbox_toolkit create --name "Whale Box" --cost 100.00 --template whale_tier

# Elite supreme ($750)  
bin/lootbox_toolkit create --name "Elite Box" --cost 750.00 --template elite_supreme
```

#### Analyze & Optimize:
```bash
# Analyze current lootbox
bin/lootbox_toolkit analyze --detailed

# Optimize for specific house edge
bin/lootbox_toolkit optimize --house-edge 0.12

# Show current configuration
bin/lootbox_toolkit show
```

#### Save & Load:
```bash
# Save current config
bin/lootbox_toolkit save --file my_lootbox.json

# Load existing config
bin/lootbox_toolkit load --file examples/premium_box.json
```

#### Quick Analysis:
```bash
# Quick cost range overview
bin/lootbox_toolkit quick
```

### 4. 📈 Batch Analyzer (`bin/batch_analyzer.py`)

**Purpose**: Analyze multiple lootbox configurations

```bash
bin/batch_analyzer.py configs/
```

**Output**: CSV reports + summary analysis of all configs in folder

## 🎯 Available Templates

| Template | Cost Range | Description | Max Item Value |
|----------|------------|-------------|----------------|
| `balanced` | $0.50-10 | Mainstream appeal | ~6x cost |
| `high_variance` | $1-50 | High risk/reward | ~25x cost |
| `whale_tier` | $50-200 | For big spenders | Up to $1000 |
| `luxury_vault` | $200-500 | Premium experience | Up to $1000 |
| `elite_supreme` | $500-1000 | Ultimate luxury | Up to $1000 |
| `csgo_style` | $2-5 | Industry standard | ~30x cost |

## 🎨 Practical Usage Examples

### Example 1: Design a $10 Standard Box
```bash
# Method 1: Interactive
./flip-gg-designer
# Enter: 10.00, strategy 2, variance 2

# Method 2: Template
bin/lootbox_toolkit create --name "Standard Box" --cost 10.00 --template balanced
bin/lootbox_toolkit optimize --house-edge 0.15
bin/lootbox_toolkit save --file standard_10.json
```

### Example 2: Create a $100 Whale Box
```bash
bin/lootbox_toolkit create --name "Whale Special" --cost 100.00 --template whale_tier
bin/lootbox_toolkit analyze --detailed
bin/lootbox_toolkit simulate --simulations 50000
bin/lootbox_toolkit save --file whale_100.json
```

### Example 3: Design Ultra-Premium $500 Box
```bash
./flip-gg-designer
# Enter: 500.00, strategy 1 (conservative), variance 3 (high)
# Results in optimized luxury lootbox
```

## 📊 Understanding the Output

### Analysis Metrics:
- **Expected Value**: Average value player receives
- **House Edge**: Your profit margin (10-20% recommended)
- **Break-even Chance**: % of players who profit
- **Player Rating**: Value assessment (Excellent → Very Poor)
- **Risk Level**: Volatility assessment

### Item Configuration:
- **ROI**: Return on investment for each item
- **Probability**: Chance of getting each item
- **Rarity**: Common → Mythic distribution
- **EV Contribution**: How much each item contributes to expected value

## 🔄 Typical Workflow

### For New Lootbox Design:
1. **Design**: Use `./flip-gg-designer` for interactive creation
2. **Analyze**: Check metrics and player experience
3. **Optimize**: Adjust house edge if needed
4. **Simulate**: Validate with Monte Carlo
5. **Save**: Export JSON for implementation
6. **Implement**: Use provided flip.gg configuration notes

### For Existing Configurations:
1. **Load**: Import existing JSON config
2. **Analyze**: Review current metrics
3. **Optimize**: Adjust for better performance
4. **Compare**: Run batch analysis vs other configs
5. **Update**: Save improved version

## 💡 Pro Tips

### Optimal Settings by Use Case:

#### **High Volume (Budget Players)**
- Cost: $0.50 - $2.00
- House Edge: 15-20%
- Variance: Medium
- Template: `balanced`

#### **Standard Players**  
- Cost: $2.00 - $10.00
- House Edge: 15-18%
- Variance: Medium-High
- Template: `balanced` or `high_variance`

#### **Premium Players**
- Cost: $10.00 - $50.00  
- House Edge: 12-15%
- Variance: High
- Template: `high_variance`

#### **Whale Players**
- Cost: $50.00 - $200.00
- House Edge: 10-15%
- Variance: Extreme
- Template: `whale_tier`

#### **Elite Players**
- Cost: $200.00 - $1000.00
- House Edge: 8-12%
- Variance: Extreme  
- Template: `luxury_vault` or `elite_supreme`

## 🎯 Key Features

### ✅ Mathematical Rigor
- Linear programming optimization
- Monte Carlo validation (up to 50,000 simulations)
- Statistical analysis and risk assessment

### ✅ Business Intelligence
- House edge optimization
- Player satisfaction metrics
- Profitability analysis

### ✅ Implementation Ready
- JSON configuration export
- Direct flip.gg probability settings
- Validation and accuracy checking

## 🚨 Important Notes

### Value Capping
- All item values automatically capped at $1000.00
- Prevents extreme jackpots that could break the system
- Maintains mathematical stability

### House Edge Guidelines
- **10-15%**: Player-friendly, high retention
- **15-20%**: Balanced, sustainable
- **20%+**: Aggressive, higher churn risk

### Simulation Accuracy
- ±2% house edge accuracy is considered excellent
- Large sample sizes (10,000+ simulations) recommended
- Results validated against theoretical calculations

## 📁 File Outputs

All tools generate JSON configurations like:
```json
{
  "name": "Custom Flip.gg Box $50.00",
  "cost": 50.0,
  "items": [
    {
      "name": "Token Drop",
      "value": 1.5,
      "rarity": "common", 
      "probability": 0.6051,
      "description": ""
    }
  ]
}
```

These files contain everything needed for flip.gg implementation!
