FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p /var/log/app && chown -R 1000:1000 /var/log/app

EXPOSE 5000

CMD ["python", "app.py"]

