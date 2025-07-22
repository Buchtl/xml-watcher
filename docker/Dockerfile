FROM python:3.11-slim

WORKDIR /app

COPY xml-watcher.py .

RUN pip install watchdog

# Print logs without delay
ENV PYTHONUNBUFFERED=1
CMD ["python", "xml-watcher.py", "--src", "/input", "--dest", "/output"]
