from pathlib import Path

import pandas as pd
from openai import OpenAI  # 根据您的OpenAI客户端库调整此导入


def process_files(api_key, prompt_file, analysis_file, standard_file, model_file):
    """
    处理用于OpenAI分析的文件。

    参数说明：
    - api_key (str):百炼大模型上的API密钥，用于访问百炼平台上的各个LLM模型。
    - prompt_file (str): 提示文件的路径。该文件包含将作为对话一部分提供给OpenAI模型的初始提示或指令，设置了对模型的上下文或特定请求。
    - analysis_file (str): 分析文本文件的路径。该文件包含需要由OpenAI模型分析的文本数据，例如需要根据特定标准进行分析的师生对话文本。
    - standard_file (str): 标准参考文件的路径。该文件将上传到OpenAI API，用作分析的参考或上下文，例如课程标准文档。
    - model_file (str): 模型知识文件的路径。该文件包含与模型相关的特定知识或数据，将上传到OpenAI API，例如“教学方法.txt”、“教学过程.txt”、“问答行为.txt”、“教学效果.txt”等。这为模型提供了额外的上下文或知识。

    返回值：
    - str: 经过处理后从OpenAI API获得的解码响应。
    """

    # 配置API密钥和基础URL
    client = OpenAI(
        api_key=api_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    # 读取提示文件
    with open(prompt_file, "r", encoding='utf-8') as f:
        prompt = f.read()

    # 读取待分析文本文件
    with open(analysis_file, "r", encoding='utf-8') as f1:
        text = f1.read()

    # 上传课程标准文件到OpenAI并获取文件对象
    file_object1 = client.files.create(file=Path(standard_file), purpose="file-extract")

    # 上传模型知识文件到OpenAI并获取文件对象
    file_object2 = client.files.create(file=Path(model_file), purpose="file-extract")

    # 进行模型对话请求
    completion = client.chat.completions.create(
        model="qwen-long",
        messages=[
            # 在系统消息中包含文件ID，为模型提供上下文
            {'role': 'system', 'content': f'fileid://{file_object1.id},fileid://{file_object2.id}'},
            # 在用户消息中组合提示和要分析的文本
            {'role': 'user', 'content': prompt + " " + text}
        ]
    )

    # 提取并解码响应内容
    content = completion.model_dump_json()
    decoded_str = content.encode().decode('unicode_escape')

    # 输出结果
    print("输出结果:", decoded_str)
    return decoded_str


if __name__ == '__main__':
    # 示例用法：
    df = pd.read_excel("data/original_data/test2.xlsx")

    api_key = "sk-454416d3aac549cd9bf043aa9fa2f158"
    result = process_files(
        api_key=api_key,
        prompt_file="prompt.txt",
        analysis_file="待分析文本.txt",
        standard_file="【3.0】义务教育生物课程标准（2022年版）.txt",
        model_file="教学方法.txt"
    )
    print(result)
