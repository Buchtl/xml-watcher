FROM python:3.11-slim

WORKDIR /app

COPY xml_watcher.py \
  xml_utils.py \
  xml_models.py \
  logging_conf.py \
  requirements.txt \
  utils.py \
  /app/

RUN pip install -r requirements.txt

ENV LOG_DIR=/var/log/xml_watcher
RUN mkdir -p $LOG_DIR && chmod 777 $LOG_DIR

# Set non-root user
USER nobody

CMD ["python", "xml_watcher.py", "--src", "/input", "--dest", "/output"]
