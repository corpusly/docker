#2021-2-11 | docker build -t wrask/trs_fillmask:4.3.2 . 
FROM python:3.8-slim

LABEL maintainer="zy <zy@cikuu.com>"

RUN pip install --no-cache-dir uvicorn gunicorn \
    && pip install fastapi \
    && pip install transformers \
    && pip install torch \
    && python -c "from transformers import pipeline;pipeline('fill-mask')"

WORKDIR /
COPY main.py /main.py
EXPOSE 80
CMD python /main.py