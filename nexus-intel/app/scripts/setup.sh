#!/bin/bash

echo "🚀 Setting up NEXUS-INTEL Project..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Download spaCy models
echo "Downloading spaCy models..."
python -m spacy download en_core_web_sm
python -m spacy download hi_core_news_sm

# Create .env file
echo "Creating .env file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️ Please update .env with your credentials"
fi

# Generate sample data
echo "Generating sample data..."
python scripts/generate_sample_data.py

# Initialize database
echo "Initializing database..."
python -c "from app.backend.database.models import init_database; init_database()"

echo "✅ Setup complete! Run 'streamlit run app/frontend/streamlit/app.py' to start the application"