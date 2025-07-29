FROM python:3.11-slim

WORKDIR /app

COPY xml_watcher.py .
COPY xml_utils.py .
COPY xml_models.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "xml_watcher.py", "--src", "/input", "--dest", "/output"]
