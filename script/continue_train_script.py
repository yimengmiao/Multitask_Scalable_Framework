import transformers
import math
from transformers.utils import send_example_telemetry
from datasets import load_dataset
from transformers import AutoTokenizer, Trainer, TrainingArguments, AutoConfig, AutoModelForCausalLM


def tokenize_function(examples):
    return tokenizer(examples["text"])


def group_texts(examples):
    # Concatenate all texts.
    concatenated_examples = {k: sum(examples[k], []) for k in examples.keys()}
    total_length = len(concatenated_examples[list(examples.keys())[0]])
    # We drop the small remainder, we could add padding if the model supported it instead of this drop, you can
    # customize this part to your needs.
    total_length = (total_length // block_size) * block_size
    # Split by chunks of max_len.
    result = {
        k: [t[i: i + block_size] for i in range(0, total_length, block_size)]
        for k, t in concatenated_examples.items()
    }
    result["labels"] = result["input_ids"].copy()
    return result


model_checkpoint = "/root/autodl-fs/Qwen/Qwen2___5-32B-Instruct"
tokenizer_checkpoint = "/root/autodl-fs/Qwen/Qwen2___5-32B-Instruct"

send_example_telemetry("language_modeling_from_scratch_notebook", framework="pytorch")

datasets = load_dataset("soikit/class_stand")

tokenizer = AutoTokenizer.from_pretrained(tokenizer_checkpoint)

tokenized_datasets = datasets.map(tokenize_function, batched=True, num_proc=4, remove_columns=["text"])

# 以这个长度来切割 文本
# block_size = tokenizer.model_max_length
block_size = 1024

lm_datasets = tokenized_datasets.map(
    group_texts,
    batched=True,
    batch_size=1000,
    num_proc=2,
)

model = AutoModelForCausalLM.from_pretrained(model_checkpoint,device_map="auto")
training_args = TrainingArguments(
    output_dir="/root/autodl-tmp",            # 保存模型的路径
    evaluation_strategy="epoch",              # 每个 epoch 后评估一次
    save_strategy="epoch",                    # 每个 epoch 后保存一次
    num_train_epochs=300,                     # 总的训练轮次
    learning_rate=2e-5,                       # 学习率
    weight_decay=0.01,                        # 权重衰减
    save_total_limit=1,                       # 最多保存一个模型
    load_best_model_at_end=True,              # 在训练结束时加载效果最好的模型
    metric_for_best_model="eval_loss",        # 用于判断最优模型的评价指标
    greater_is_better=False,                  # 若 `metric_for_best_model` 越小越好，则设为 False；否则设为 True
      # 降低显存占用的设置
    per_device_train_batch_size=1,               # 每个设备上的批次大小（越小越省显存）
    per_device_eval_batch_size=1,                # 评估时的批次大小
    gradient_accumulation_steps=8,               # 梯度累积步数（有效批次大小 = 批次大小 x 累积步数）
    fp16=True,                                  # 使用混合精度（如果支持，可以大幅降低显存）
    optim="adamw_torch",                         # 使用更省显存的优化器
    logging_steps=10,                            # 记录间隔步数
    dataloader_num_workers=4,                    # 数据加载的线程数（适当调低以节省CPU和显存）
    lr_scheduler_type="linear"
)

# 初始化 Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=lm_datasets["train"],
    eval_dataset=lm_datasets["validation"],
)
# 开始训练
trainer.train()



eval_results = trainer.evaluate()
print(f"Perplexity: {math.exp(eval_results['eval_loss']):.2f}")