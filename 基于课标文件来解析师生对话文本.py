import argparse
from pathlib import Path

from openai import OpenAI


def main(prompt_file, analysis_file, standard_file, model_file):
    # 配置API Key和基础URL
    client = OpenAI(
        api_key="sk-454416d3aac549cd9bf043aa9fa2f158",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    # 读取 prompt 文件
    with open(prompt_file, "r", encoding='utf-8') as f:
        prompt = f.read()

    # 读取待分析文本文件
    with open(analysis_file, "r", encoding='utf-8') as f1:
        text = f1.read()

    # 上传课程标准文件到 OpenAI 并获取 file_object
    file_object1 = client.files.create(file=Path(standard_file), purpose="file-extract")

    # 上传模型知识文件到 OpenAI 并获取 file_object
    file_object2 = client.files.create(file=Path(model_file), purpose="file-extract")
    # 进行模型对话请求
    completion = client.chat.completions.create(
        model="qwen-long",
        messages=[
            {'role': 'system', 'content': f'fileid://{file_object1.id},fileid://{file_object2.id}'},
            {'role': 'user', 'content': prompt + " " + text}
        ]
    )

    content = completion.model_dump_json()
    # 将 Unicode 转义字符解码为中文
    decoded_str = content.encode().decode('unicode_escape')

    # 输出结果
    print("输出结果", decoded_str)
    return decoded_str


if __name__ == "__main__":
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description="Process some files for OpenAI analysis.")
    parser.add_argument("--prompt_file", type=str, required=True, help="Path to the prompt file (prompt.txt)")
    parser.add_argument("--analysis_file", type=str, required=True,
                        help="Path to the analysis text file (待分析文本.txt)")
    parser.add_argument("--standard_file", type=str, required=True,
                        help="Path to the standard file (【3.0】义务教育课程标准（2022年版）.txt）")
    parser.add_argument("--model_file", type=str, required=True,
                        help="Path to the tip file (这里传入的是模型知识.txt中对应的部分内容共有四块,分别为：教学方法.txt、教学过程.txt、问答行为.txt、教学效果.txt）")

    # 解析参数
    args = parser.parse_args()

    # 调用主函数
    main(args.prompt_file, args.analysis_file, args.standard_file, args.model_file)

# 使用示例：
# python 基于课标文件来解析师生对话文本.py --prompt_file prompt.txt --analysis_file 待分析文本.txt --standard_file 【3.0】义务教育生物课程标准（2022年版）.txt --model_file 教学方法.txt
