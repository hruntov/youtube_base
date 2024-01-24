#!/bin/bash

cd youtube_base && \
python manage.py migrate && \
python manage.py loaddata youtubers/fixtures/categories.json && \
python manage.py loaddata youtubers/fixtures/youtubers.json && \
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell && \
python manage.py runserver 0.0.0.0:8000