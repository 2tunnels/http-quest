FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1

RUN groupadd --system app && useradd --system --shell /bin/false --gid app app

WORKDIR /app

COPY pyproject.toml .
COPY poetry.lock .

RUN pip install --upgrade --no-cache-dir pip setuptools poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

COPY docker-entrypoint.sh /usr/local/bin/

COPY . .

USER app

EXPOSE 8000

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["gunicorn"]
