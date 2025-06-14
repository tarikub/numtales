###################
# BUILD FOR LOCAL DEVELOPMENT
###################
# start by pulling the python image
FROM python:3.11.0-bullseye

# switch working directory
WORKDIR /app

# install the dependencies
RUN pip install "poetry==1.3.1"

# copy every content from the local file to the image
COPY . /app

# Install poetry dependencies
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi --no-root

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

ARG MONGODB_URI
ENV MONGODB_URI=${MONGODB_URI}

EXPOSE 5000

CMD ["search.py" ]