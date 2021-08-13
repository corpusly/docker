
https://huggingface.co/transformers/task_summary.html

python:3.8-slim 
pip install transformers 
pip install torch 


python -c 'from foo import hello; print hello()'
python -c 'from transformers import pipeline; pipeline('sentiment-analysis')'

python -c 'import pprint;pprint.pprint(1)'
'

==== hello === 

>>> from transformers import pipeline

# Allocate a pipeline for sentiment-analysis
>>> classifier = pipeline('sentiment-analysis')
>>> classifier('We are very happy to include pipeline into the transformers repository.')
[{'label': 'POSITIVE', 'score': 0.9978193640708923}]



ps@gpu24:~$ docker run -it --rm python:3.8-alpine3.10  /bin/sh
/ # apk add gcc   | apt-get install gcc -y
fetch http://dl-cdn.alpinelinux.org/alpine/v3.10/main/x86_64/APKINDEX.tar.gz
fetch http://dl-cdn.alpinelinux.org/alpine/v3.10/community/x86_64/APKINDEX.tar.gz
(1/10) Installing binutils (2.32-r0)
(2/10) Installing gmp (6.1.2-r1)
(3/10) Installing isl (0.18-r0)
(4/10) Installing libgomp (8.3.0-r0)
(5/10) Installing libatomic (8.3.0-r0)
(6/10) Installing libgcc (8.3.0-r0)
(7/10) Installing mpfr3 (3.1.5-r1)
(8/10) Installing mpc1 (1.1.0-r0)
(9/10) Installing libstdc++ (8.3.0-r0)
(10/10) Installing gcc (8.3.0-r0)
Executing busybox-1.30.1-r3.trigger
OK: 97 MiB in 44 packages
/ # apk add g++
(1/4) Upgrading musl (1.1.22-r3 -> 1.1.22-r4)
(2/4) Installing musl-dev (1.1.22-r4)
(3/4) Installing libc-dev (0.7.1-r0)
(4/4) Installing g++ (8.3.0-r0)
Executing busybox-1.30.1-r3.trigger
OK: 163 MiB in 47 packages
/ # pip install https://github.com/kpu/kenlm/archive/master.zip
Collecting https://github.com/kpu/kenlm/archive/master.zip
  Downloading https://github.com/kpu/kenlm/archive/master.zip
     / 540 kB 267 kB/s
Building wheels for collected packages: kenlm
  Building wheel for kenlm (setup.py) ... done
  Created wheel for kenlm: filename=kenlm-0.0.0-cp38-cp38-linux_x86_64.whl size=300567 sha256=d45c889f74566dc3793ac51d6e7a204d670bc7c8291334566e1bb0b95222204d
  Stored in directory: /tmp/pip-ephem-wheel-cache-vcf411y0/wheels/ff/08/4e/a3ddc0e786e0f3c1fcd2e7a82c4324c02fc3ae2638471406d2
Successfully built kenlm
Installing collected packages: kenlm
Successfully installed kenlm-0.0.0
WARNING: You are using pip version 20.1.1; however, version 21.0.1 is available.
You should consider upgrading via the '/usr/local/bin/python -m pip install --upgrade pip' command.



https://github.com/huggingface/transformers/blob/master/docker/transformers-pytorch-gpu/Dockerfile


===
fast_app = FastAPI()

register_tortoise(fast_app, config=TORTOISE_ORM, generate_schemas=True)

fast_app.mount('/admin', admin_app)

@fast_app.on_event('startup')
async def startup():
    admin_app.init(
        user_model='User',
        tortoise_app='models',
        admin_secret='test',
        permission=True,
        site=Site(...)
    )