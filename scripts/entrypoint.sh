#!/bin/bash

# exit immediately if any command fails
set -e

# Wait for database (optional, but recommended if MySQL container starts slow)
# python manage.py check --database default

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Compiling translations..."
python manage.py compilemessages || true

echo "Starting Gunicorn server..."
# Using gunicorn for production
exec gunicorn pcc.wsgi:application \
    --bind 0.0.0.0:8013 \
    --workers 3 \
    --access-logfile - \
    --error-logfile -
