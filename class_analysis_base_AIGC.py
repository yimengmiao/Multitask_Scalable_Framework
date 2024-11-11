import argparse
import json
from pathlib import Path
from openai import OpenAI


def main(prompt_file, analysis_file=None, standard_file=None, TM_file=None, TP_file=None, AA_file=None, TE_file=None):
    client = OpenAI(
        api_key="sk-454416d3aac549cd9bf043aa9fa2f158",  # 隐藏密钥
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    # 读取 prompt 文件
    with open(prompt_file, "r", encoding='utf-8') as f:
        prompt = f.read()

    # 定义一个列表用于存储上传的文件ID
    file_ids = []

    # 判断并上传每个文件（只有在路径存在时才上传）
    if standard_file and Path(standard_file).exists():
        standard_file_object = client.files.create(file=Path(standard_file), purpose="file-extract")
        file_ids.append(f'fileid://{standard_file_object.id}')

    if TM_file and Path(TM_file).exists():
        TM_file_object = client.files.create(file=Path(TM_file), purpose="file-extract")
        file_ids.append(f'fileid://{TM_file_object.id}')

    if TP_file and Path(TP_file).exists():
        TP_file_object = client.files.create(file=Path(TP_file), purpose="file-extract")
        file_ids.append(f'fileid://{TP_file_object.id}')

    if AA_file and Path(AA_file).exists():
        AA_file_object = client.files.create(file=Path(AA_file), purpose="file-extract")
        file_ids.append(f'fileid://{AA_file_object.id}')

    if TE_file and Path(TE_file).exists():
        TE_file_object = client.files.create(file=Path(TE_file), purpose="file-extract")
        file_ids.append(f'fileid://{TE_file_object.id}')

    if analysis_file and Path(analysis_file).exists():
        analysis_file_object = client.files.create(file=Path(analysis_file), purpose="file-extract")
        file_ids.append(f'fileid://{analysis_file_object.id}')

    # 创建模型对话请求
    completion = client.chat.completions.create(
        model="qwen-long",
        messages=[
            {'role': 'system', 'content': ','.join(file_ids)},
            {'role': 'user', 'content': prompt}
        ]
    )

    # 提取并解码 JSON 中的 content 部分
    content = json.loads(completion.model_dump_json())
    content_text = content['choices'][0]['message']['content']  # 提取 content 内容

    print("输出结果", content_text)  # 打印提取的内容

    # 将提取的内容保存到文件
    with open("输出结果.txt", "w", encoding='utf-8') as f:
        f.write(content_text)  # 将 content 内容写入文件

    return content_text  # 返回 content 内容



if __name__ == "__main__":
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description="Process some files for OpenAI analysis.")
    parser.add_argument("--prompt_file", type=str, required=True, help="Path to the prompt file (prompt.txt)")
    parser.add_argument("--analysis_file", type=str, help="Path to the analysis text file (待分析文本(长).txt)")
    parser.add_argument("--standard_file", type=str, help="Path to the standard file")
    parser.add_argument("--TM_file", type=str, help="Path to the 教学方法.txt")
    parser.add_argument("--TP_file", type=str, help="Path to the 课堂活动.txt")
    parser.add_argument("--AA_file", type=str, help="Path to the 问答行为.txt")
    parser.add_argument("--TE_file", type=str, help="Path to the 教学效果.txt")
    args = parser.parse_args()

    # 调用主函数
    main(
        args.prompt_file,
        analysis_file=args.analysis_file,
        standard_file=args.standard_file,
        TM_file=args.TM_file,
        TP_file=args.TP_file,
        AA_file=args.AA_file,
        TE_file=args.TE_file
    )

# 使用示例：
# python class_analysis_base_AIGC.py --prompt_file prompt.txt --analysis_file data/original_data/待分析文本(长).txt --standard_file 【3.0】义务教育生物课程标准（2022年版）.txt --TM_file 教学方法.txt --TP_file 课堂活动.txt --AA_file 问答行为.txt --TE_file 教学效果.txt
# python class_analysis_base_AIGC.py --prompt_file prompt/基于AIGC的课堂分析（zonkey版本）/prompt/教学效果.txt --analysis_file data/original_data/待分析文本.txt --standard_file prompt/基于AIGC的课堂分析（zonkey版本）/课程标准/【3.0】义务教育生物课程标准（2022年版）.txt --TM_file prompt/基于AIGC的课堂分析（zonkey版本）/模型知识/教学方法.txt  --TP_file prompt/基于AIGC的课堂分析（zonkey版本）/模型知识/课堂活动.txt --AA_file prompt/基于AIGC的课堂分析（zonkey版本）/模型知识/问答行为.txt --TE_file prompt/基于AIGC的课堂分析（zonkey版本）/模型知识/教学效果.txt
