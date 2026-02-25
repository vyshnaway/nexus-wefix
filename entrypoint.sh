#!/bin/sh

echo "Waiting for PostgreSQL..."
until pg_isready -h db -U nexus -d nexus > /dev/null 2>&1; do
    echo "PostgreSQL not ready – retrying in 2s..."
    sleep 2
done
echo "PostgreSQL is ready."

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Django development server..."
exec python manage.py runserver 0.0.0.0:8000
