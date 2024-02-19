FROM python:3.11-slim-bookworm

WORKDIR /src

COPY .setup/requirements.txt /src/requirements.txt

RUN pip install --no-cache-dir -r /src/requirements.txt

COPY src/ .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]