docker run -d -p 7098:7098 -v /home/cikuu/model:/home/cikuu/model --name kenlm --restart=always cikuu_kenlm:7098 gunicorn --workers=2 --bind=0.0.0.0:7098 --timeout 120 --chdir /home/cikuu/api/ken_lm kenlm_flask:app

#http://dev.werror.com:7098/kenlm/flue/I%20love%20you%7CI%20live%20you%7CI%20love%20you%20so%20much
#{"I live you":0.297494,"I love you":0.384929,"I love you so much":0.450107}
