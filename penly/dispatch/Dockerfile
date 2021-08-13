#  docker build -t wrask/penly:dispatch .   | 2021.7.30
FROM python:3.8-slim
RUN pip install redis numpy fire
WORKDIR /
COPY pen_stroke_dispatch.py . 
EXPOSE 80
CMD python pen_stroke_dispatch.py