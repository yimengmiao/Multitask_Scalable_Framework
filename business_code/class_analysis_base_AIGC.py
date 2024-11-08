import argparse
from pathlib import Path

from openai import OpenAI


def main(prompt_file, analysis_file, standard_file):
    # 配置API Key和基础URL
    client = OpenAI(
        api_key="",
        base_url="",
    )

    # 读取 prompt 文件
    with open(prompt_file, "r", encoding='utf-8') as f:
        prompt = f.read()

    # 读取待分析文本文件
    with open(analysis_file, "r", encoding='utf-8') as f1:
        text = f1.read()

    # 上传课程标准文件到 OpenAI 并获取 file_object
    file_object = client.files.create(file=Path(standard_file), purpose="file-extract")

    # 进行模型对话请求
    completion = client.chat.completions.create(
        model="qwen-long",
        messages=[
            {'role': 'system', 'content': f'fileid://{file_object.id}'},
            {'role': 'user', 'content': prompt + " " + text}
        ]
    )

    # 输出结果
    print(completion.model_dump_json())


if __name__ == "__main__":
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description="Process some files for OpenAI analysis.")
    parser.add_argument("--prompt_file", type=str, required=True, help="Path to the prompt file (prompt.txt)")
    parser.add_argument("--analysis_file", type=str, required=True,
                        help="Path to the analysis text file (待分析文本(长).txt)")
    parser.add_argument("--standard_file", type=str, required=True,
                        help="Path to the standard file (【3.0】义务教育语文课程标准（2022年版）.txt）")

    # 解析参数
    args = parser.parse_args()

    # 调用主函数
    main(args.prompt_file, args.analysis_file, args.standard_file)

# 使用示例：
# python class_analysis_base_AIGC.py --prompt_file path/to/prompt.txt --analysis_file path/to/待分析文本(长).txt --standard_file path/to/【3.0】义务教育语文课程标准（2022年版）.txt
