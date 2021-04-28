FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY . /app

# Allow installing dev dependencies to run tests
RUN bash -c "poetry install --no-root"

ENV PYTHONPATH=/app

CMD ["bash", "./start.sh"]
