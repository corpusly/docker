# 2021.7.30
FROM wrask/uvicorn:3.8-slim
WORKDIR /
COPY print_channel.py . 
COPY websocketd . 
EXPOSE 7089
CMD /websocketd --port 7089 --address=127.0.0.1 /usr/local/bin/python print_channel.py pen_strokes