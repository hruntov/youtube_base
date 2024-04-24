#!/bin/bash

cd youtube_base && \
python manage.py migrate && \
python manage.py loaddata youtubers/fixtures/categories.json && \
python manage.py loaddata youtubers/fixtures/youtubers.json && \
python manage.py loaddata youtubers/fixtures/tags.json && \
python manage.py loaddata users/fixtures/users.json && \
python manage.py clearcache | python manage.py shell
python manage.py runserver 0.0.0.0:8000