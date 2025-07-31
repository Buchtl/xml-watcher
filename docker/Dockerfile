FROM python:3.11-slim

ENV LOG_DIR=/var/log/xml_watcher
RUN mkdir -p $LOG_DIR &&\
  chmod 777 $LOG_DIR &&\
  mkdir -p /app &&\
  chmod 777 /app &&\
  mkdir -p /input &&\
  chmod 777 /input &&\
  mkdir -p /output && \
  chmod 777 /output

COPY ./src/ /app/src/
COPY requirements.txt /app

WORKDIR /app

RUN pip install -r requirements.txt

# Set non-root user
USER nobody

CMD ["python", "-m", "src.xml_watcher", "--src", "/input", "--dest", "/output"]
