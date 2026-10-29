FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY aggregate.py consume.py ./
ENV PYTHONUNBUFFERED=1
CMD ["python", "consume.py"]
