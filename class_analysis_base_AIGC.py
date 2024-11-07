import argparse
from pathlib import Path

from openai import OpenAI


def main(prompt_file, analysis_file, standard_file, TM_file, TP_file, AA_file, TE_file):
    # todo: 配置阿里云的API密钥和基础URL。你可以改成我们自己部署好的LLM服务url，但是要注意，我们部署的LLM服务中是没有文件上传并解析的功能的，
    #  所以这个代码只能调用大厂那边LLM的服务。
    client = OpenAI(
        api_key="sk-454416d3aac549cd9bf043aa9fa2f158",  # 密钥隐藏一下
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    # 读取 prompt 文件
    with open(prompt_file, "r", encoding='utf-8') as f:
        prompt = f.read()

    # 读取待分析文本文件
    # with open(analysis_file, "r", encoding='utf-8') as f1:
    #     text = f1.read()

    # 上传课程标准文件到 dashscope 并获取 file_object
    file_object1 = client.files.create(file=Path(standard_file), purpose="file-extract")

    # 上传模型知识文件到 dashscope 并获取 file_object
    file_object2 = client.files.create(file=Path(TM_file), purpose="file-extract")

    # 上传模型知识文件到 dashscope 并获取 file_object
    file_object3 = client.files.create(file=Path(TP_file), purpose="file-extract")

    # 上传模型知识文件到 dashscope 并获取 file_object
    file_object4 = client.files.create(file=Path(AA_file), purpose="file-extract")

    # 上传模型知识文件到 dashscope 并获取 file_object
    file_object5 = client.files.create(file=Path(TE_file), purpose="file-extract")

    # 上传待分析文本文件到dashscope并获取 file_object
    file_object6 = client.files.create(file=Path(analysis_file), purpose="file-extract")
    # 进行模型对话请求
    completion = client.chat.completions.create(
        model="qwen-long",
        messages=[
            {'role': 'system',
             'content': f'fileid://{file_object1.id},fileid://{file_object2.id},fileid://{file_object3.id},'
                        f'fileid://{file_object4.id},fileid://{file_object5.id},fileid://{file_object6.id}'},


            {'role': 'user', 'content': prompt}  # 添加空格增加可读性
        ]
    )

    content = completion.model_dump_json()

    # 将 Unicode 转义字符解码为中文

    # 输出结果
    print("输出结果", content)
    return content


if __name__ == "__main__":
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description="Process some files for OpenAI analysis.")
    parser.add_argument("--prompt_file", type=str, required=True, help="Path to the prompt file (prompt.txt)")
    parser.add_argument("--analysis_file", type=str, required=True,
                        help="Path to the analysis text file (待分析文本.txt)")
    parser.add_argument("--standard_file", type=str, required=True,
                        help="Path to the standard file (【3.0】义务教育课程标准（2022年版）.txt）")
    parser.add_argument("--TM_file", type=str, required=True,
                        help="这里传入的是模型知识.txt中对应的部分内容共有四块,分别为：教学方法.txt、教学过程.txt、问答行为.txt、教学效果.txt。这个参数只传入教学方法.txt")
    parser.add_argument("--TP_file", type=str, required=True,
                        help="教学过程.txt")
    parser.add_argument("--AA_file", type=str, required=True,
                        help="问答行为.txt ")
    parser.add_argument("--TE_file", type=str, required=True,
                        help="教学效果.txt ")
    # 解析参数
    args = parser.parse_args()

    # 调用主函数
    main(args.prompt_file, args.analysis_file, args.standard_file, args.TM_file, args.TP_file, args.AA_file,
         args.TE_file)

# 使用示例：
# python class_analysis_base_AIGC.py --prompt_file prompt.txt --analysis_file data/original_data/待分析文本.txt --standard_file 【3.0】义务教育生物课程标准（2022年版）.txt --TM_file 教学方法.txt --TP_file 教学过程.txt --AA_file 问答行为.txt --TE_file 教学效果.txt
# python class_analysis_base_AIGC.py --prompt_file prompt/基于AIGC的课堂分析/prompt/教学效果.txt --analysis_file data/original_data/待分析文本.txt --standard_file prompt/基于AIGC的课堂分析/课程标准/【3.0】义务教育生物课程标准（2022年版）.txt --TM_file prompt/基于AIGC的课堂分析/模型知识/教学方法.txt  --TP_file prompt/基于AIGC的课堂分析/模型知识/教学过程.txt --AA_file prompt/基于AIGC的课堂分析/模型知识/问答行为.txt --TE_file prompt/基于AIGC的课堂分析/模型知识/教学效果.txt
