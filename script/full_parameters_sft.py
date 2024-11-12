import argparse
import torch
import os
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    TrainerCallback,
    TrainerState,
    TrainerControl
)
from trl import SFTTrainer

# 解析命令行参数
parser = argparse.ArgumentParser(description="Train a language model with SFTTrainer.")
parser.add_argument("--model_name", type=str, required=True, help="Path to the model.")
parser.add_argument("--output_dir", type=str, required=True, help="Directory to save the model outputs.")
args = parser.parse_args()

# 安装 flash_attention 库
os.system('pip install flash_attn')

# 配置计算数据类型为 bfloat16 和注意力实现方式为 flash_attention_2
compute_dtype = torch.bfloat16
attn_implementation = 'flash_attention_2'

# 加载分词器
tokenizer = AutoTokenizer.from_pretrained(args.model_name, add_eos_token=True, use_fast=True)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.pad_token_id = tokenizer.eos_token_id
tokenizer.padding_side = 'right'

# 加载数据集
ds = load_dataset('yimeng521/sunny_datasets')

# 加载模型，使用 bfloat16 数据类型，并配置设备和注意力实现方式
model = AutoModelForCausalLM.from_pretrained(
    args.model_name, torch_dtype=torch.bfloat16, device_map="auto", attn_implementation=attn_implementation
)
model.gradient_checkpointing_enable()
model.config.pad_token_id = tokenizer.pad_token_id
model.config.use_cache = False

# 配置训练参数
training_arguments = TrainingArguments(
    output_dir=args.output_dir,
    evaluation_strategy="epoch",
    save_strategy="epoch",  # 在每个 epoch 保存检查点
    do_eval=True,
    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,
    log_level="debug",
    optim="galore_adamw",
    optim_args="rank=1024, update_proj_gap=500, scale=1.8",
    optim_target_modules=[r".*attn.*", r".*mlp.*"],
    logging_steps=85,
    learning_rate=1e-5,
    bf16=torch.cuda.is_bf16_supported(),
    num_train_epochs=10,
    warmup_ratio=0.1,
    lr_scheduler_type="linear",
    load_best_model_at_end=False,
    metric_for_best_model="eval_loss",
    greater_is_better=False,
    save_total_limit=1
)

# 自定义回调类，用于记录最低 eval_loss 的检查点路径
class BestModelCheckpointCallback(TrainerCallback):
    def __init__(self):
        self.best_loss = float('inf')
        self.best_checkpoint = None

    def on_evaluate(self, args, state: TrainerState, control: TrainerControl, **kwargs):
        current_loss = state.log_history[-1]["eval_loss"]
        if current_loss < self.best_loss:
            self.best_loss = current_loss
            self.best_checkpoint = state.best_model_checkpoint

best_checkpoint_callback = BestModelCheckpointCallback()

# 创建训练器 SFTTrainer
trainer = SFTTrainer(
    model=model,
    train_dataset=ds['train'],
    eval_dataset=ds['test'],
    dataset_text_field="text",
    max_seq_length=512,
    tokenizer=tokenizer,
    args=training_arguments,
    callbacks=[best_checkpoint_callback]
)

# 开始训练
trainer.train()

# 在训练结束后加载并保存最佳检查点
if best_checkpoint_callback.best_checkpoint:
    best_model = AutoModelForCausalLM.from_pretrained(best_checkpoint_callback.best_checkpoint)
    best_model.save_pretrained(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)

# python train_and_save.py --model_name /root/autodl-fs/qwen/Qwen1___5-0___5B-Chat --output_dir /root/autodl-fs/qwen_0.5b_GaLore
