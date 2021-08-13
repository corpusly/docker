docker run -d -p 7091:7091 -v /home/cikuu/model:/home/cikuu/model --name cikuu_mapf --restart=always cikuu_mapf:7091 gunicorn --workers=2 --bind=0.0.0.0:7091 --timeout 120 --chdir /home/cikuu/api/flask mapfapp:app

#http://dev.werror.com:7091/api/nextword?snt=I%20love%20you
#