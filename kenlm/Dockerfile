# 2021-2-12
FROM python:3.8

RUN pip install --no-cache-dir uvicorn gunicorn \
    && pip install fastapi \
    && pip install https://github.com/kpu/kenlm/archive/master.zip \
    && mkdir /model

WORKDIR /
COPY main.py /main.py
EXPOSE 80
CMD python /main.py