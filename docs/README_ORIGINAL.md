# 🎲 Lootbox Probability Toolkit

A comprehensive Python toolkit for designing, analyzing, and optimizing lootbox probability distributions with mathematical rigor. Perfect for game developers, analysts, and anyone interested in understanding the mathematics behind lootbox mechanics.

## ✨ Features

- **🎯 Expected Value Calculations**: Precise mathematical analysis of lootbox profitability
- **📊 Monte Carlo Simulations**: Statistical validation through thousands of simulated openings
- **🔧 Probability Optimization**: Mathematical optimization to achieve target house edges
- **📈 Risk Analysis**: Comprehensive variance and risk assessment tools
- **🎨 Interactive CLI**: User-friendly command-line interface with colored output
- **📋 Predefined Templates**: Industry-standard configurations (CS:GO, balanced, high/low variance)
- **💾 Configuration Management**: Save, load, and share lootbox configurations
- **📊 Detailed Analytics**: In-depth analysis of rarity distributions and player value

## 🚀 Quick Start

### Installation

```bash
# Navigate to the toolkit directory
cd lootbox_toolkit

# Install dependencies
pip install -r requirements.txt

# Run setup (optional)
python3 lootbox_toolkit.py setup --install-deps
```

### Basic Usage

```bash
# Create a lootbox from template
python3 lootbox_toolkit.py template --template balanced --cost 2.00

# Analyze the lootbox
python3 lootbox_toolkit.py analyze

# Run Monte Carlo simulation
python3 lootbox_toolkit.py simulate --simulations 10000

# Optimize probabilities for 15% house edge
python3 lootbox_toolkit.py optimize --target-house-edge 0.15

# Show current configuration
python3 lootbox_toolkit.py show

# Save configuration
python3 lootbox_toolkit.py save --file my_lootbox.json
```

## 📋 Available Commands

### Design Commands
- `create` - Create a new lootbox interactively
- `template` - Create from predefined templates (balanced, csgo, high_variance, low_variance)
- `load` - Load existing configuration from file
- `save` - Save current configuration to file
- `show` - Display current lootbox details

### Analysis Commands
- `analyze` - Comprehensive statistical analysis
- `simulate` - Monte Carlo simulation with configurable parameters
- `cost-analysis` - Analyze optimal configurations across cost ranges

### Optimization Commands
- `optimize` - Optimize probabilities for target house edge
  - Methods: `scipy` (fast, precise) or `genetic` (robust, global optimization)

## 🎯 Core Concepts

### Expected Value
The mathematical expectation of value from opening a lootbox:
```
Expected Value = Σ(Item Value × Probability)
```

### House Edge
The casino's mathematical advantage:
```
House Edge = (Cost - Expected Value) / Cost
```

### Rarity Tiers
- **Common**: High probability, low value items
- **Uncommon**: Medium probability, moderate value
- **Rare**: Lower probability, good value
- **Epic**: Low probability, high value
- **Legendary**: Very low probability, very high value  
- **Mythic**: Extremely low probability, extreme value

## 📊 Example Analysis

```bash
# Load a balanced lootbox template
$ python3 lootbox_toolkit.py template --template balanced --cost 2.00

# Analyze it
$ python3 lootbox_toolkit.py analyze

ANALYSIS: Balanced Box
Expected Value:    $1.7250
House Edge:        13.75%
Standard Deviation: $4.2441
Risk Level:        High Risk
Player Rating:     Good

Break Even Chance: 33.00%
10%+ Profit Chance: 20.00%
```

## 🔧 Advanced Features

### Cost Range Analysis
Find optimal configurations across different price points:
```bash
python3 lootbox_toolkit.py cost-analysis --min-cost 0.5 --max-cost 4.0 --house-edge 0.15
```

### Optimization Methods
1. **SciPy Optimization**: Fast, mathematically precise
2. **Genetic Algorithm**: Robust, handles complex constraints

### Monte Carlo Simulation
- Configurable number of simulations (default: 10,000)
- Reproducible results with random seeds
- Statistical validation of theoretical calculations
- Streak pattern analysis

## 📁 Project Structure

```
lootbox_toolkit/
├── src/
│   ├── core/           # Data models and base classes
│   ├── calculator/     # Expected value calculations
│   ├── simulator/      # Monte Carlo simulation engine
│   ├── optimizer/      # Probability optimization algorithms
│   ├── config/         # Configuration management
│   ├── cli/           # Command-line interface
│   └── analytics/     # Advanced analytics tools
├── examples/          # Example configurations and demos
├── tests/            # Unit tests
├── docs/             # Documentation
└── requirements.txt  # Python dependencies
```

## 🎮 Example Templates

### Balanced Template
- 15% house edge
- Fair player value proposition
- Moderate variance
- Good for general-purpose lootboxes

### CS:GO Style Template
- Mimics CS:GO weapon case odds
- High house edge (~90%)
- Extreme variance
- Industry-standard distribution

### High Variance Template
- 70% chance of minimal value
- 1% chance of extreme jackpot
- High risk, high reward
- Appeals to thrill-seekers

### Low Variance Template
- Consistent, predictable returns
- Low standard deviation
- Appeals to risk-averse players
- Suitable for loyalty programs

## 🧮 Mathematical Background

The toolkit uses rigorous statistical methods:

- **Expected Value Theory**: Mathematical expectation calculations
- **Variance Analysis**: Risk assessment through variance and standard deviation
- **Optimization Theory**: Linear programming and genetic algorithms
- **Monte Carlo Methods**: Statistical validation and simulation
- **Probability Theory**: Comprehensive probability distribution analysis

## ⚠️ Important Notes

- **Educational Purpose**: This toolkit is for educational and analytical purposes
- **Responsible Gaming**: Always consider player welfare in lootbox design
- **Legal Compliance**: Ensure compliance with local gambling regulations
- **Transparency**: Consider disclosing odds to players for ethical reasons

## 🔍 Use Cases

1. **Game Developers**: Design balanced lootbox systems
2. **Data Analysts**: Analyze existing lootbox economics
3. **Researchers**: Study probability distributions and player behavior
4. **Educators**: Teach probability and statistics concepts
5. **Compliance**: Verify fairness and regulatory compliance

## 📈 Performance

- **Fast Calculations**: Optimized algorithms for real-time analysis
- **Scalable Simulations**: Handle millions of simulations efficiently
- **Memory Efficient**: Minimal memory footprint for large datasets
- **Parallel Processing**: Multi-threaded simulations (future enhancement)

## 🤝 Contributing

This is an educational project. Contributions welcome:
- Bug reports and fixes
- Feature enhancements
- Documentation improvements
- Additional templates and examples
- Performance optimizations

## 📜 License

Educational and research use. See LICENSE file for details.

---

**Remember**: Design lootboxes responsibly and always consider player welfare!
