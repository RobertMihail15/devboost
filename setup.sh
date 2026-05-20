#!/bin/bash
echo "🚀 Setting up DevBoost..."

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Seed sample data
python seed.py

# Create superuser (optional)
echo ""
echo "✅ Setup complete!"
echo ""
echo "Run the server with:"
echo "  python manage.py runserver"
echo ""
echo "Then open: http://127.0.0.1:8000"
echo ""
echo "Django admin: http://127.0.0.1:8000/admin"
echo "  (Create superuser with: python manage.py createsuperuser)"
