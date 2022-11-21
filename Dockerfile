#FIRST LAYER: Get all dependencies that can be copied over, while dropping compilation tools
# syntax=docker/dockerfile:experimental
FROM python:3.9.5-slim as compile-image

ENV LC_ALL "C.UTF-8"
ENV LANG "C.UTF-8"
ENV WOMBO_UTILITIES_SCHEMAS "paint_service,depth_service,mediastore,graphoperations,dream_homepage,dreambooth"

RUN apt-get update && apt-get install -y \
   libcairo2-dev gcc pkg-config libgirepository1.0-dev \
   libssl-dev libcurl4-openssl-dev build-essential git libpq-dev openssh-client\
   && rm -rf /var/lib/apt/lists/*

# Download public key for github.com
RUN mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts

#Create a virtual environment we can copy over
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt ./

RUN pip3 install --upgrade setuptools pip
RUN --mount=type=ssh pip3 install --ignore-installed --no-cache-dir -r requirements.txt

# Takes care of all packages needed for open-telemetry
RUN opentelemetry-bootstrap --action=install

#SECOND LAYER: Only get dependencies from compilation time
FROM python:3.9.5-slim as prod-image

# psycopg2 libraries are needed to run as well so let's install that
RUN apt-get update && apt-get install -y libpq-dev curl ffmpeg

WORKDIR /app/
# Actual python app
EXPOSE 8124

COPY --from=compile-image /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY . ./

# Need to do this as follows, maybe we have to migrate to use gunicorn within fastapi.py programmatically
# Uvicorn can't be used because https://github.com/open-telemetry/opentelemetry-python-contrib/issues/385#issuecomment-1199088668

CMD opentelemetry-instrument --logs_exporter otlp_proto_grpc --traces_exporter otlp_proto_grpc gunicorn wombo.fastapi:app --workers 2 --worker-class uvicorn.workers.UvicornH11Worker --bind 0.0.0.0:8124