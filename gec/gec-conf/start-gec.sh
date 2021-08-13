#CUDA_VISIBLE_DEVICES=0 python Translater.py ./ --port 8000 --path clean.pt --beam 5 --bpe subword_nmt --bpe-codes ./code --buffer-size 10 --batch-size 10 --source-lang er --target-lang co --remove-bpe --num-workers 20  --tokenizer space --nbest 5 

docker run -d --runtime=nvidia -e NVIDIA_VISIBLE_DEVICES=all -p 7090:8000 --rm --name gec wrask/gec sh start.sh 
