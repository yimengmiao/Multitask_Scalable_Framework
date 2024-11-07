
from pathlib import Path
from openai import OpenAI


def analyze_text_with_llm(prompt_path, analysis_text_path, standard_path, teaching_methods_path,
                          teaching_process_path, qna_behavior_path, teaching_effect_path, api_key, base_url):
    """
    使用指定的 LLM 服务对文本进行分析。将课程标准和相关教学内容文件上传到 LLM 服务，
    然后根据 prompt 和分析文本进行对话生成。

    参数：
    - prompt_path: 提示词文件的路径
    - analysis_text_path: 待分析文本文件的路径
    - standard_path: 课程标准文件的路径
    - teaching_methods_path: 教学方法文件路径
    - teaching_process_path: 教学过程文件路径
    - qna_behavior_path: 问答行为文件路径
    - teaching_effect_path: 教学效果文件路径
    - api_key: LLM 服务的 API 密钥
    - base_url: LLM 服务的基础 URL

    返回：
    - LLM 对话生成的分析结果
    """
    # 初始化 LLM 客户端
    # todo: 配置阿里云的API密钥和基础URL。你可以改成我们自己部署好的LLM服务url，但是要注意，我们部署的LLM服务中是没有文件上传并解析的功能的，
    #  所以这个代码只能调用大厂那边LLM的服务。
    client = OpenAI(api_key=api_key, base_url=base_url)

    # 读取提示词文件
    with open(prompt_path, "r", encoding='utf-8') as f:
        prompt_content = f.read()

    # 读取待分析文本文件
    with open(analysis_text_path, "r", encoding='utf-8') as f:
        analysis_content = f.read()

    # 上传课程标准和各个教学文件到 LLM 并获取文件对象
    standard_file = client.files.create(file=Path(standard_path), purpose="file-extract")
    teaching_methods_file = client.files.create(file=Path(teaching_methods_path), purpose="file-extract")
    teaching_process_file = client.files.create(file=Path(teaching_process_path), purpose="file-extract")
    qna_behavior_file = client.files.create(file=Path(qna_behavior_path), purpose="file-extract")
    teaching_effect_file = client.files.create(file=Path(teaching_effect_path), purpose="file-extract")

    # 构造对话请求内容并调用 LLM 进行对话
    completion = client.chat.completions.create(
        model="qwen-long",
        messages=[
            {
                'role': 'system',
                'content': f'fileid://{standard_file.id},fileid://{teaching_methods_file.id},'
                           f'fileid://{teaching_process_file.id},fileid://{qna_behavior_file.id},'
                           f'fileid://{teaching_effect_file.id}'
            },
            {'role': 'user', 'content': prompt_content }  # 组合 prompt 和待分析文本
        ]
    )

    # 提取和解码返回的内容
    raw_content = completion.model_dump_json()
    result_content = raw_content.encode('latin1').decode('unicode_escape')

    # 输出和返回分析结果
    print("分析结果:", result_content)
    return result_content


if __name__ == '__main__':
# 使用示例
    analyze_text_with_llm(
        prompt_path="prompt.txt",
        analysis_text_path="地球的运动.txt",
        standard_path="【3.0】义务教育地理课程标准（2022年版）.txt",
        teaching_methods_path="教学方法.txt",
        teaching_process_path="教学过程.txt",
        qna_behavior_path="问答行为.txt",
        teaching_effect_path="教学效果.txt",

        api_key="sk-454416d3aac549cd9bf043aa9fa2f158",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )
