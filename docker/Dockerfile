FROM python:3.11-slim

WORKDIR /app

COPY xml-watcher.py .

RUN pip install watchdog

CMD ["python", "xml-watcher.py", "--src", "/input", "--dest", "/output"]
