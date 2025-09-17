#!/bin/bash
# Lootbox Toolkit Installation Script
#
# Automatically sets up the complete lootbox probability toolkit
# with all dependencies and configurations.

set -e  # Exit on any error

echo "🎲 LOOTBOX PROBABILITY TOOLKIT INSTALLER"
echo "========================================"

# Check Python version
echo "🔍 Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Found Python $PYTHON_VERSION"

# Check if we're in the right directory
if [[ ! -f "requirements.txt" ]]; then
    echo "❌ Please run this script from the lootbox_toolkit directory"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [[ ! -d "venv" ]]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment and install dependencies
echo "📦 Installing dependencies..."
source venv/bin/activate

# Upgrade pip first
pip install --upgrade pip

# Install requirements
if pip install -r requirements.txt; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Create necessary directories
echo "📁 Creating directory structure..."
mkdir -p {data,logs,outputs,configs,examples,bin,docs,tests}

# Set executable permissions
echo "🔧 Setting executable permissions..."
chmod +x bin/*.py
chmod +x bin/lootbox_toolkit

# Create symlinks for easy access
echo "🔗 Creating convenience symlinks..."
ln -sf bin/lootbox_calculator.py lootbox-calc
ln -sf bin/flip_gg_interactive.py flip-gg-designer  
ln -sf bin/batch_analyzer.py batch-analyzer
ln -sf bin/lootbox_toolkit lootbox-toolkit

# Test installation
echo "🧪 Testing installation..."
if python3 bin/lootbox_calculator.py > /dev/null 2>&1; then
    echo "✅ Installation test passed"
else
    echo "❌ Installation test failed"
    exit 1
fi

# Create default configuration
echo "⚙️ Creating default configuration..."
cat > configs/default.json << EOF
{
  "default_cost": 2.00,
  "default_house_edge": 0.15,
  "default_simulations": 10000,
  "output_format": "json",
  "auto_save": true,
  "precision": 4
}
EOF

echo "✅ Default configuration created"

# Generate initial examples if they don't exist
echo "📝 Generating example configurations..."
python3 -c "
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))
from core.models import LootboxItem, Lootbox, RarityTier

# Create budget example
budget_items = [
    LootboxItem(name='Small Prize', value=0.15, rarity=RarityTier.COMMON, probability=0.50),
    LootboxItem(name='Medium Prize', value=0.45, rarity=RarityTier.UNCOMMON, probability=0.30),
    LootboxItem(name='Good Prize', value=1.20, rarity=RarityTier.RARE, probability=0.15),
    LootboxItem(name='Great Prize', value=4.00, rarity=RarityTier.EPIC, probability=0.05)
]
budget_box = Lootbox(name='Budget Box', cost=0.75, items=budget_items, description='Budget-friendly lootbox with good player value')

# Save budget example using built-in method
budget_box.save_to_file('examples/budget_example.json')

print('✅ Example configurations generated')
"

echo ""
echo "🎉 INSTALLATION COMPLETE!"
echo "========================"
echo ""
echo "📋 Available Tools:"
echo "  ./lootbox-calc                 - Comprehensive calculator" 
echo "  ./flip-gg-designer             - Interactive designer"
echo "  ./batch-analyzer               - Batch processing tool"
echo "  ./lootbox-toolkit              - Main CLI interface"
echo ""
echo "🚀 Quick Start:"
echo "  ./lootbox-calc                 # Run full analysis"
echo "  ./flip-gg-designer             # Interactive design"
echo "  ./lootbox-toolkit quick        # Quick cost analysis"
echo ""
echo "📖 Documentation:"
echo "  README.md                      # Main documentation"
echo "  docs/FLIP_GG_GUIDE.md         # Flip.gg specific guide"
echo ""
echo "💾 Output Locations:"
echo "  outputs/                       # Generated lootbox configs"
echo "  logs/                          # Application logs"
echo "  data/                          # Persistent data"
echo ""
echo "Happy lootbox designing! 🎲"
