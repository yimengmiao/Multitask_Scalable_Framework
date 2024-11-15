import os
import time

from model_api import ModelAPI


def construct_prompt(prompt_file_path, analysis_data_file_path, class_stand_text_file_path, bc_knowledge_file_paths):
    # 读取 prompt 文件内容（无需前缀）
    with open(prompt_file_path, "r", encoding='utf-8') as f:
        prompt_content = f.read()

    # 读取待分析文本，并添加前缀
    analysis_filename = os.path.basename(analysis_data_file_path)
    analysis_data_prefix = f"{{{analysis_filename}}}的内容如下："
    with open(analysis_data_file_path, "r", encoding='utf-8') as f:
        analysis_data_content = analysis_data_prefix + f.read()

    # 读取课程标准文本，并添加前缀
    class_stand_prefix = "{新课标内容如下}："
    with open(class_stand_text_file_path, "r", encoding='utf-8') as f:
        class_stand_content = class_stand_prefix + f.read()

    # 读取背景知识文件，并添加前缀
    bc_knowledge_contents = ''
    for bc_file_path in bc_knowledge_file_paths:
        bc_filename = os.path.basename(bc_file_path)
        bc_prefix = f"{{{bc_filename}}}内容如下："
        with open(bc_file_path, "r", encoding='utf-8') as f:
            bc_content = bc_prefix + f.read()
        bc_knowledge_contents += bc_content

    # 按指定顺序组合所有内容
    full_prompt = prompt_content + analysis_data_content + class_stand_content + bc_knowledge_contents

    return full_prompt


# todo:未来做成一个接口，然后传参就看business_code/业务代码文档/基于AIGC的课堂分析（zonekey）/class_analysis_base_AIGC(params)的代码使用方法.md
def get_result(params):
    # 使用 construct_prompt 函数生成 prompt 文本
    text = construct_prompt(
        prompt_file_path=params["prompt_file_path"],
        analysis_data_file_path=params["analysis_data_file_path"],
        class_stand_text_file_path=params["class_stand_text_file_path"],
        bc_knowledge_file_paths=params["bc_knowledge_file_paths"]
    )

    # 将生成的 prompt 文本添加到 params 中
    params["prompt"] = text

    # 创建 ModelAPI 实例并进行分析
    model_api = ModelAPI(params)
    result = model_api.analyze()
    return result


if __name__ == '__main__':
    # 　用ｑｗｅｎ－ｌｏｎｇ接口调用。
    # with open("prompt/基于AIGC的课堂分析（zonkey版本）/prompt/教学效果.txt", "r", encoding="utf-8") as f:
    #     text = f.read()
    #
    # params = {
    #     "model_family": "qwen",
    #     "api_key": "sk-454416d3aac549cd9bf043aa9fa2f158",
    #     "prompt": text,
    #     "model_name": "qwen-long",  # Example model, can be changed
    #     "max_tokens": 1000,
    #     "n": 1,
    #     "temperature": 0.7,
    #     "use_files": True,
    #     "files": ["data/original_data/待分析文本.txt", "prompt/基于AICG的课堂分析/模型知识/教学效果.txt",
    #               "prompt/基于AIGC的课堂分析（zonkey版本）/课程标准/【3.0】义务教育生物课程标准（2022年版）.txt"]
    # }
    #
    # # 创建 ModelAPI 实例并调用方法
    # model_api = ModelAPI(params)
    # result = model_api.analyze()
    # print("Result:", result)

    # 定义参数，不使用文件，只进行文本分析
    # 调用模型出结果
    # 设置文件路径参数
    start_time = time.time()
    params = {
        "model_family": "local",
        "api_key": "token123",  # 请替换为您的实际 API 密钥
        "prompt_file_path": "prompt/基于AIGC的课分析（杨州大学版本）/prompt/教学效果.txt",
        "analysis_data_file_path": "data/original_data/待分析文本.txt",
        "class_stand_text_file_path": "prompt/基于AIGC的课分析（杨州大学版本）/课程标准/【3.0】义务教育生物课程标准（2022年版）.txt",
        "bc_knowledge_file_paths": [
            "prompt/基于AIGC的课分析（杨州大学版本）/模型知识/教学效果.txt",

        ],
        "model_name": "qwen2_5-32b-instruct",
        "max_tokens": 2000,
        "n": 1,
        "temperature": 0.7,
        "use_files": False,
    }

    # 调用 get_result 函数获取最终结果
    result = get_result(params)
    end_time = time.time()
    print("耗时", end_time - start_time)
    print("结果", result)
