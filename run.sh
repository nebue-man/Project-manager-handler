#!/bin/bash

# Project Manager Startup Script
# This script sets up the environment and runs the application

echo "🚀 Starting Project Manager..."

# Check if virtual environment exists
if [ ! -d "project_manager_env" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv project_manager_env
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source project_manager_env/bin/activate

# Check if dependencies are installed
if ! python -c "import customtkinter" 2>/dev/null; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
fi

# Run the application
echo "🎯 Starting application..."
python main.py

# Keep terminal open after app closes
read -p "Press Enter to exit..."