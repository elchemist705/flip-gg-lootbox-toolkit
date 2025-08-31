#!/usr/bin/env python3
"""
Lootbox Probability Toolkit - Quick Start

A comprehensive toolkit for designing, analyzing, and optimizing lootbox
probability distributions with mathematical rigor.

Usage:
    python3 lootbox_toolkit.py --help
    python3 lootbox_toolkit.py create --name "My Box" --cost 2.50
    python3 lootbox_toolkit.py template --template balanced --cost 2.00
    python3 lootbox_toolkit.py analyze
    python3 lootbox_toolkit.py simulate --simulations 10000
    python3 lootbox_toolkit.py optimize --target-house-edge 0.15
"""

import os
import sys
import click
from pathlib import Path

# Add src directory to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

try:
    from cli.main import cli
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install required dependencies:")
    print("  pip install -r requirements.txt")
    sys.exit(1)


@click.command()
@click.option('--install-deps', is_flag=True, help='Install required dependencies')
def setup(install_deps):
    """Set up the lootbox toolkit environment"""
    if install_deps:
        os.system("pip install -r requirements.txt")
        print("✓ Dependencies installed")
    
    print("🎲 Lootbox Probability Toolkit Setup Complete!")
    print("\nQuick Start Commands:")
    print("  python3 lootbox_toolkit.py template --template balanced")
    print("  python3 lootbox_toolkit.py analyze")
    print("  python3 lootbox_toolkit.py simulate") 
    print("  python3 lootbox_toolkit.py optimize")


if __name__ == '__main__':
    # Check if setup command
    if len(sys.argv) > 1 and sys.argv[1] == 'setup':
        setup()
    else:
        # Run main CLI
        cli()
