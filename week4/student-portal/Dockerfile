FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8000

ENV FLASK_APP=app.py
ENV FLASK_RUN_PORT=8000

CMD ["python", "run.py"]
