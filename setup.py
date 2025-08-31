"""
Setup script for Lootbox Probability Toolkit
"""
from setuptools import setup, find_packages
import os

# Read version from VERSION file
def get_version():
    with open(os.path.join(os.path.dirname(__file__), 'VERSION'), 'r') as f:
        return f.read().strip()

# Read long description from README
def get_long_description():
    with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r') as f:
        return f.read()

setup(
    name="lootbox-toolkit",
    version=get_version(),
    description="Comprehensive probability calculation toolkit for lootbox design and analysis",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Lootbox Toolkit Team",
    author_email="contact@lootbox-toolkit.dev",
    url="https://github.com/yourusername/lootbox-toolkit",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.24.0",
        "scipy>=1.10.0", 
        "matplotlib>=3.6.0",
        "pandas>=1.5.0",
        "click>=8.0.0",
        "colorama>=0.4.0",
        "tabulate>=0.9.0",
        "pydantic>=2.0.0",
        "jsonschema>=4.0.0",
        "tqdm>=4.64.0"
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0"
        ]
    },
    entry_points={
        "console_scripts": [
            "lootbox-toolkit=cli.main:cli",
            "lootbox-calc=bin.lootbox_calculator:main",
            "flip-gg-designer=bin.flip_gg_interactive:main"
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Games/Entertainment",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="lootbox probability statistics gaming analysis optimization",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/lootbox-toolkit/issues",
        "Source": "https://github.com/yourusername/lootbox-toolkit",
        "Documentation": "https://lootbox-toolkit.readthedocs.io/",
    },
)
