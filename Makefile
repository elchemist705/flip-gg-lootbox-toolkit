# Lootbox Probability Toolkit - Makefile

.PHONY: help install clean test analyze demo batch quick setup

# Default target
help:
	@echo "🎲 Lootbox Probability Toolkit"
	@echo "=============================="
	@echo ""
	@echo "Available commands:"
	@echo "  make install    - Install dependencies and setup"
	@echo "  make demo       - Run comprehensive demonstration"
	@echo "  make analyze    - Run full cost range analysis"
	@echo "  make quick      - Quick comparison analysis"
	@echo "  make batch      - Batch analyze all configurations"
	@echo "  make clean      - Clean temporary files"
	@echo "  make test       - Run test suite (future)"
	@echo "  make setup      - Initial project setup"
	@echo ""
	@echo "Interactive tools:"
	@echo "  make designer   - Launch interactive designer"
	@echo "  make calculator - Launch main calculator"
	@echo ""

# Installation and setup
install:
	@echo "📦 Installing Lootbox Toolkit..."
	./install.sh

setup: install
	@echo "✅ Setup complete!"

# Main tools
calculator:
	@echo "🧮 Launching main calculator..."
	./lootbox-calc

designer:
	@echo "🎨 Launching interactive designer..."
	./flip-gg-designer

# Analysis commands
demo:
	@echo "🎬 Running comprehensive demo..."
	source venv/bin/activate && python3 examples/demo.py

analyze:
	@echo "📊 Running full analysis..."
	./lootbox-calc

quick:
	@echo "⚡ Running quick analysis..."
	./lootbox-toolkit quick

batch:
	@echo "📋 Running batch analysis..."
	./batch-analyzer --input-dir outputs --output-dir outputs

# Utilities
clean:
	@echo "🧹 Cleaning temporary files..."
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache 2>/dev/null || true
	rm -f *.log 2>/dev/null || true
	@echo "✅ Clean complete"

# Development commands
dev-install:
	@echo "🔧 Installing development dependencies..."
	source venv/bin/activate && pip install pytest black flake8 mypy

lint:
	@echo "🔍 Running code quality checks..."
	source venv/bin/activate && black --check src/ bin/
	source venv/bin/activate && flake8 src/ bin/ --max-line-length=100

format:
	@echo "✨ Formatting code..."
	source venv/bin/activate && black src/ bin/

test:
	@echo "🧪 Running tests..."
	@echo "Test suite not yet implemented"

# Documentation
docs:
	@echo "📚 Generating documentation..."
	@echo "Documentation generation not yet implemented"

# Status and info
status:
	@echo "📋 Toolkit Status:"
	@echo "=================="
	@ls -la bin/
	@echo ""
	@echo "Generated Configurations:"
	@ls -la outputs/ 2>/dev/null || echo "No configurations yet"
	@echo ""
	@echo "Virtual Environment:"
	@if [ -d "venv" ]; then echo "✅ Active"; else echo "❌ Not found"; fi

info:
	@echo "🎲 Lootbox Probability Toolkit v1.0.0"
	@echo "======================================"
	@echo "Purpose: Design and analyze optimal lootbox configurations"
	@echo "Target: Flip.gg lootboxes ($0.50-$4.00 range)"
	@echo "Features: Mathematical optimization, Monte Carlo simulation"
	@echo ""
	@echo "Main tools:"
	@echo "  ./lootbox-calc      - Comprehensive calculator"
	@echo "  ./flip-gg-designer  - Interactive designer"
	@echo "  ./batch-analyzer    - Batch processor"
	@echo ""
	@echo "For help: make help"

# Shortcuts for common workflows
flip-gg: designer

all: install demo

# Example workflows
example-budget:
	@echo "💰 Creating budget lootbox example..."
	./lootbox-toolkit create --name "Budget Example" --cost 0.75 --template balanced
	./lootbox-toolkit analyze --detailed
	./lootbox-toolkit save --file budget_example

example-premium:
	@echo "💎 Creating premium lootbox example..."  
	./lootbox-toolkit create --name "Premium Example" --cost 3.50 --template high_variance
	./lootbox-toolkit optimize --house-edge 0.18
	./lootbox-toolkit save --file premium_example
