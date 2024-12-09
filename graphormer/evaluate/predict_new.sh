python Graphormer-IR/graphormer/evaluate/predict_new.py \
    --user-dir Graphormer-IR/graphormer \
    --num-workers 6 \
    --ddp-backend=legacy_ddp \
	--user-data-dir Graphormer-IR/graphormer/evaluate/testing_dataset \
	--dataset-name IR_test \
    --task graph_prediction \
	--criterion sid \
	--arch graphormer_base \
    --encoder-layers 4 \
    --encoder-embed-dim  2100 \
    --encoder-ffn-embed-dim 2100 \
    --encoder-attention-heads 210 \
    --mlp-layers 3 \
    --batch-size 32 \
    --num-classes 1801 \
    --save-dir $1 \
    --split train \
    --dataset-source $2\

