#!/bin/sh
while ! nc -z "$DB_HOSTNAME" "$DB_PORT"; do
	echo "Waiting for PostgreSQL to become available..."
	sleep 2
done


echo "migrating ..."
python manage.py makemigrations
python manage.py migrate

echo "starting django server..."
python manage.py runserver 0.0.0.0:8000

