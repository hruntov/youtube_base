FROM python:3.10-slim-buster

ENV PYTHONPATH "${PYTHONPATH}:/website_wsl"
ENV DJANGO_ENV=${DJANGO_ENV} \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_VERSION=1.7.0 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry'

# System deps:
RUN apt-get update && \
  apt-get install --no-install-recommends -y \
  build-essential \
  gettext \
  libpq-dev \
  wget \
  # Cleaning cache:
  && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* \
  # Installing `poetry` package manager:
  && pip install "poetry-core==1.8.1" "poetry==$POETRY_VERSION" && poetry --version

# Copy only requirements, to cache them in docker layer
WORKDIR /website_wsl
COPY ./poetry.lock ./pyproject.toml /website_wsl/

# Project initialization:
RUN poetry install


# Creating folders, and files for a project:
COPY . /website_wsl

RUN chmod +x /website_wsl/start_web.sh
RUN poetry shell
CMD ["bash", "/website_wsl/start_web.sh"]
