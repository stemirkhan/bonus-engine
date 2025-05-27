FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .

COPY . .

CMD ["uvicorn", "app:create_app", "--host", "0.0.0.0", "--port", "8000"]
