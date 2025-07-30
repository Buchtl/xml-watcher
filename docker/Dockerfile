FROM python:3.11-slim

WORKDIR /app

COPY xml_watcher.py \
  xml_utils.py \
  xml_models.py \
  requirements.txt \
  utils.py \
  /app/

RUN pip install -r requirements.txt

CMD ["python", "xml_watcher.py", "--src", "/input", "--dest", "/output"]
