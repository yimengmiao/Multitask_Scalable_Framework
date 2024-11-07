以下是整理后的文档，分为安装、部署和测试步骤：

---
## Swift安装
   ```bash
    git clone https://github.com/modelscope/swift.git
    cd swift
    pip install -e '.[all]'
   ```
## Swift 启动服务命令
1. Swift 启动服务命令示例：
   ```bash
   CUDA_VISIBLE_DEVICES=0,1,2,3 swift deploy --model_type qwen2_5-32b-instruct --model_id_or_path /root/autodl-fs/Qwen/Qwen2___5-32B-Instruct --infer_backend lmdeploy --tp 4 --port 6006 --max_length 512000 --dtype bf16 --rope_scaling linear
   ```

2. LMdeploy推理框架启动服务命令：
   ```bash
   lmdeploy serve api_server /root/autodl-fs/Qwen/Qwen2___5-32B-Instruct --server-port 6006 --session-len 51200 --tp 4
   ```

--- 
## vLLM 安装
1. 创建新的 conda 环境：
   ```bash
   conda create -n qwen python=3.10 -y
   conda activate qwen
   ```

2. 安装 vLLM（CUDA 12.1）：
   ```bash
   pip install vllm
   ```

## vLLM 部署服务
1. 启动 32B 模型服务，使用 `bf16` 精度，指定端口 6006：
   ```bash
   vllm serve /root/autodl-fs/Qwen/Qwen2___5-32B-Instruct --dtype auto --api-key token-abc123 --host 0.0.0.0 --port 6006 --tensor-parallel-size 4 --max-context-length 51200 --precision bf16
   ```

2. 启动 7B 模型服务，指定端口 8000：
   ```bash
   vllm serve /root/autodl-tmp/Qwen/Qwen2___5-7B-Instruct --dtype auto --api-key token-abc123 --host 0.0.0.0 --port 8000
   ```

## vLLM 性能测试命令
性能测试参数说明：
- `--input_length`：输入文本长度
- `--output_length`：输出文本长度
- `--num_threads`：并发请求数量

```bash
python vllm_inference.py --input_length 4000 --output_length 800 --num_threads 64
```

---

## TensorRT-LLM 安装
1. 配置临时目录：
   ```bash
   mkdir /root/autodl-tmp/tmp
   export TMPDIR=/root/autodl-tmp/tmp
   ```

2. 安装 CUDA 12.4.2 及工具包：
   ```bash
   wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-ubuntu2204.pin
   sudo mv cuda-ubuntu2204.pin /etc/apt/preferences.d/cuda-repository-pin-600
   wget https://developer.download.nvidia.com/compute/cuda/12.4.1/local_installers/cuda-repo-ubuntu2204-12-4-local_12.4.1-550.54.15-1_amd64.deb
   sudo dpkg -i cuda-repo-ubuntu2204-12-4-local_12.4.1-550.54.15-1_amd64.deb
   sudo cp /var/cuda-repo-ubuntu2204-12-4-local/cuda-*-keyring.gpg /usr/share/keyrings/
   sudo apt-get update
   sudo apt-get -y install cuda-toolkit-12-4
   ```

3. 安装必要的 Python 环境和包：
   ```bash
   conda create -n tensorrt python=3.10
   conda activate tensorrt
   conda install -c conda-forge ucx ucc nccl
   conda install mpi4py openmpi
   conda install cuda-cudart cuda-version=12
   apt-get update && apt-get -y install openmpi-bin libopenmpi-dev git git-lfs
   pip install tensorrt_llm==0.13.0 --extra-index-url https://pypi.nvidia.com
   pip cache purge
   ```

## TensorRT-LLM 部署服务
1. 克隆仓库并转换模型：
   ```bash
   git clone https://github.com/NVIDIA/TensorRT-LLM.git
   python convert_checkpoint.py --model_dir /root/autodl-fs/Qwen/Qwen2___5-32B-Instruct --output_dir /root/autodl-fs/tllm_checkpoint_4gpu_tp4 --dtype bfloat16 --tp_size 2
   ```

2. 构建 Qwen-14B-Chat，使用 2-way Tensor 并行：
   ```bash
   trtllm-build --checkpoint_dir /root/autodl-fs/tllm_checkpoint_4gpu_tp4 --output_dir /root/autodl-fs/qwen/32B/trt_engines/fp16/4-gpu --gpt_attention_plugin bfloat16 --gemm_plugin bfloat16 --kv_cache_type paged
   ```

3. 测试命令示例：
   ```bash
   mpirun -n 2 --allow-run-as-root python ../run.py --input_text "请对下面文章总结出50个字的摘要..." --max_output_len=200 --tokenizer_dir /root/autodl-fs/Qwen/Qwen2___5-32B-Instruct --engine_dir=/root/autodl-fs/qwen/32B/trt_engines/fp16/4-gpu
   ```

## 使用 Triton Server 搭建 TensorRT 服务
1. 克隆 `tensorrtllm_backend` 并进行配置：
   ```bash
   git clone https://github.com/triton-inference-server/tensorrtllm_backend.git
   ```

2. 配置参数和启动 Triton Server：
   ```bash
   ENGINE_DIR=/root/autodl-fs/qwen/32B/trt_engines/fp16/4-gpu
   TOKENIZER_DIR=/root/autodl-fs/Qwen/Qwen2___5-32B-Instruct
   MODEL_FOLDER=/triton_model_repo
   TRITON_MAX_BATCH_SIZE=4
   INSTANCE_COUNT=1
   MAX_QUEUE_DELAY_MS=0
   MAX_QUEUE_SIZE=0
   FILL_TEMPLATE_SCRIPT=/root/tensorrtllm_backend/tools/fill_template.py
   DECOUPLED_MODE=false

   python3 ${FILL_TEMPLATE_SCRIPT} -i ${MODEL_FOLDER}/ensemble/config.pbtxt triton_max_batch_size:${TRITON_MAX_BATCH_SIZE}
   python3 /tensorrtllm_backend/scripts/launch_triton_server.py --world_size=2 --model_repo=${MODEL_FOLDER}
   ```

---

## LLama-Factory 启动命令
1. 配置 CUDA 设备并启动训练：
   ```bash
   export CUDA_VISIBLE_DEVICES=0,1,2,3
   llamafactory-cli train --stage pt --do_train True --model_name_or_path /root/autodl-tmp/Qwen/Qwen2___5-7B-Instruct --preprocessing_num_workers 16 --finetuning_type full --template qwen --flash_attn auto --dataset_dir data --dataset class_stand --cutoff_len 1024 --learning_rate 1e-05 --num_train_epochs 200 --max_samples 10000 --per_device_train_batch_size 1 --gradient_accumulation_steps 8 --lr_scheduler_type linear --max_grad_norm 0.5 --logging_steps 5 --save_steps 50 --warmup_steps 20 --optim adamw_torch --packing True --report_to none --output_dir /root/autodl-tmp/Qwen2.5/full/train_2024-11-01-15-37-39 --bf16 True --plot_loss True --ddp_timeout 180000000 --include_num_input_tokens_seen True --val_size 0.1 --eval_strategy steps --eval_steps 50 --per_device_eval_batch_size 2 --overwrite_output_dir --save_total_limit 1 --load_best_model_at_end True --deepspeed cache/ds_z3_config.json
   ```

---



以上是按步骤和逻辑整理的完整部署与测试指南。