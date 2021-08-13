
#docker run -it -e VIRTUAL_HOST=kenlm.werror.com --rm --name kenlm1 -p 80 192.168.1.24:5000/cikuu_kenlm python -m cikuu.api.uvicorn.kenlm_api
#docker run -it -e VIRTUAL_HOST=cclm.werror.com --rm --name cclm -p 80 wrask/kenlm python /kenlm.py
docker run -it -e VIRTUAL_HOST=cclm.werror.com --rm --name cclm -p 8889:80 -v /home/cikuu/model/cclm:/model wrask/kenlm

docker run -it -e VIRTUAL_HOST=cclm.werror.com --rm --name cclm -p 8889:80 -v /home/cikuu/model/cclm:/model wrask/kenlm

