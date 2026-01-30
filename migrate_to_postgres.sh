#!/bin/bash

echo "Setting up PostgreSQL for Spiritual Gifts Survey..."

# Install psycopg2-binary
cd backend
pip install psycopg2-binary

# Run migrations
echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

# Populate data
echo "Populating spiritual gifts and questions..."
python manage.py populate_data

echo "✅ PostgreSQL setup complete!"
echo ""
echo "Database credentials:"
echo "  Database: spiritual_gifts_survey"
echo "  User: postgres"
echo "  Password: postgres"
echo "  Host: localhost"
echo "  Port: 5432"
