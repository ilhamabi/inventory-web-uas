FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
ENV LOG_DIR=/var/log/app


EXPOSE 5000

CMD ["python", "app.py"]

