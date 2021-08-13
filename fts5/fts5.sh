
docker run -it -e VIRTUAL_HOST=kenlm.werror.com --rm --name kenlm1 -p 80 192.168.1.24:5000/cikuu_kenlm python -m cikuu.api.uvicorn.kenlm_api
