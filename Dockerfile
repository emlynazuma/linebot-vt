FROM python:3.8-slim as python-base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    POETRY_HOME="/opt/poetry" \
    build_dep="curl"
ENV PATH="${POETRY_HOME}/bin:${PATH}"
WORKDIR /app/src/
COPY . /app/src/
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        ${build_dep} \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - --uninstall \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get purge -y --auto-remove ${build_dep}
ENTRYPOINT [ "/app/src/run_server.sh" ]
