#!/bin/bash

echo "🚀 Setting up Django School Website..."
echo "=================================="

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python first."
    exit 1
fi

echo "✅ Python found"

# Install requirements
echo "📦 Installing requirements..."
pip install -r requirements.txt

# Make migrations
echo "🗄️ Creating database migrations..."
python manage.py makemigrations

# Apply migrations
echo "🗄️ Applying migrations..."
python manage.py migrate

# Create superuser (optional)
echo "👤 Creating admin user..."
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@school13.uz', 'admin123') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell

# Populate sample data
echo "📊 Populating sample data..."
python manage.py populate_sample_data

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "🎉 Setup complete!"
echo "=================================="
echo "🌐 Start the server with: python manage.py runserver"
echo "🏠 Visit: http://127.0.0.1:8000/"
echo "⚙️  Admin: http://127.0.0.1:8000/admin/"
echo "👤 Admin login: admin / admin123"
