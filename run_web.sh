#!/bin/sh

# wait for PSQL server to start
sleep 10

# migrate db, so we have the latest db schema
python manage.py migrate

echo "from django.contrib.auth.models import User; User.objects.create_superuser('xtomik', 'xtomik@stuba.sk', 'abc123456')" | python manage.py shell
# start development server on public ip interface, on port 8000
python manage.py runserver 0.0.0.0:8000