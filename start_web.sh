#!/bin/bash

cd youtube_base && \
python manage.py migrate && \
python manage.py loaddata youtubers/fixtures/data.json && \
python manage.py loaddata users/fixtures/users.json | python manage.py shell
python manage.py runserver 0.0.0.0:8000