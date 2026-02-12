#!/bin/bash

# E-Commerce Recommendation System - Quick Start Script
# This script automates the setup and launch process

set -e  # Exit on error

echo "=========================================="
echo "E-Commerce Recommendation System"
echo "Quick Start Script"
echo "=========================================="
echo ""

# Check Python version
echo "[1/6] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✓ Python $PYTHON_VERSION found"
echo ""

# Create virtual environment
echo "[2/6] Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "[3/6] Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "[4/6] Installing dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Run setup
echo "[5/6] Setting up the system..."
if [ ! -f "models/recommender_model.pkl" ]; then
    python setup.py
else
    echo "✓ System already set up (models exist)"
    read -p "Do you want to retrain the model? (y/N): " retrain
    if [ "$retrain" = "y" ] || [ "$retrain" = "Y" ]; then
        rm -rf data/*.csv models/*.pkl 2>/dev/null || true
        python setup.py
    fi
fi
echo ""

# Launch application
echo "[6/6] Launching application..."
echo ""
echo "=========================================="
echo "Application is starting..."
echo "=========================================="
echo ""
echo "The app will open in your browser at:"
echo "  http://localhost:8501"
echo ""
echo "Create an account or login to get started!"
echo ""
echo "Press Ctrl+C to stop the application"
echo "=========================================="
echo ""

streamlit run app.py

# Deactivate virtual environment on exit
deactivate
