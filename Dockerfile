# Pull base image
FROM python:3.10.4-slim-bullseye
# Copy project
COPY ./social_network ./social_network
COPY ./requirements.txt ./requirements.txt
COPY ./alembic.ini ./alembic.ini
COPY ./migrations ./migrations
COPY ./start.sh ./start.sh

# Install dependencies
RUN pip install -r requirements.txt