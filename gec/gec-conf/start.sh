
CUDA_VISIBLE_DEVICES=0,1 python Translater.py ./ --port 80 --path clean.pt --beam 5 --bpe subword_nmt --bpe-codes ./code --buffer-size 10 --batch-size 10 --source-lang er --target-lang co --remove-bpe --num-workers 20  --tokenizer space --nbest 5 
