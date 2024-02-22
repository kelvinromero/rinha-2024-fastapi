FROM python:3.11-slim-bookworm

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY src/ /app/src

CMD ["uvicorn", "--reload", "src.main:app", "--host", "0.0.0.0", "--port", "80"]