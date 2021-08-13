docker run -d -p 7099:7099 --name roberta_cloze --restart=always cikuu_roberta:7099 gunicorn --workers=2 --bind=0.0.0.0:7099 --timeout 120 --chdir /home/cikuu/api/roberta roberta_flask:app

#http://dev.werror.com:7099/roberta/cloze/I%20*%20you?topk=9
#[["love",0.5055],["miss",0.0825],["hate",0.0278],["need",0.0271],["know",0.0235],["loved",0.0221],["forgive",0.0214],["want",0.0205],["missed",0.0198]]
