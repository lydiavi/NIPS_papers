FROM python:3.11-slim as base

# Expecting proxy to be passed as build args
ARG HTTP_PROXY
ARG HTTPS_PROXY

# Set proxy environment variables
ENV HTTP_PROXY ${HTTP_PROXY}
ENV HTTPS_PROXY ${HTTPS_PROXY}

WORKDIR /app

# Copy the poetry config files
COPY config.toml auth.toml pyproject.toml /app/

RUN pip config set global.trusted-host "pypi.org files.pythonhosted.org pypi.python.org"

RUN pip install poetry && \
    mkdir $HOME/.config/pypoetry/ && \
    cp config.toml $HOME/.config/pypoetry/config.toml && \
    cp auth.toml $HOME/.config/pypoetry/auth.toml && \
    poetry config virtualenvs.create false

RUN poetry install --only main --no-cache

CMD streamlit run app/basic_streamlit_app.py
