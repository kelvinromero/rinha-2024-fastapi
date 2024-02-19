FROM python:3.11-slim-bookworm

WORKDIR /src

COPY ./requirements.txt /src/requirements.txt

RUN pip install --no-cache-dir -r /src/requirements.txt

COPY src/ .

# Guni
#CMD ["gunicorn", "src.main:app", "--workers", "2", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:80"]

CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]