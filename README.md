# For the run docker with the project
docker run -it -d -e "API_KEY=" -v D:\projects\website_wsl:/website_wsl -p 8000:8000 --name my-django-container my-django-app
docker exec -it my-django-container bash