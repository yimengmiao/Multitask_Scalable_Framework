# 使用指南

本指南将帮助您了解如何使用提供的代码来生成完整的 `prompt` 并调用模型进行分析。我们将详细介绍各个参数的用途、数据类型、可能的取值范围，以及如何配置它们。

## 代码概述

该代码的主要功能是：

1. **构建完整的 `prompt`**：通过读取指定的文件，按照特定的顺序和格式组合成模型需要的输入文本。
2. **调用模型进行分析**：使用 `ModelAPI` 类，将生成的 `prompt` 传递给模型，并获取分析结果。

## 快速开始

您只需提供一个包含必要参数的 `params` 字典，然后调用 `get_result(params)` 函数，即可获取模型的分析结果。

## 参数详解

以下是 `params` 字典中各个参数的详细说明：

| 参数名称                     | 数据类型     | 可选值 / 格式                      | 说明                                         |
|------------------------------|--------------|-------------------------------|--------------------------------------------|
| `model_family`               | 字符串       | `"qwen"` ,"local"             | 模型家族名称，指定使用的模型系列。 详细请看model_api/模型层使用说明.md |
| `api_key`                    | 字符串       | 您的 API 密钥                     | 用于身份验证的 API 密钥，请替换为您的实际密钥。                 |
| `prompt_file_path`           | 字符串       | 文件路径，如 `"prompt/教学效果.txt"`    | 指定 `prompt` 文件的路径，包含模型指令或问题。               |
| `analysis_data_file_path`    | 字符串       | 文件路径，如 `"待分析文本.txt"`          | 待分析文本的文件路径，包含需要模型分析的内容。                    |
| `class_stand_text_file_path` | 字符串       | 文件路径，如 `"初中课程标准/初中生物课程标准.txt"` | 课程标准文本的文件路径，提供背景信息。                        |
| `bc_knowledge_file_paths`    | 列表（字符串）| 文件路径列表，如 `["背景知识/教学效果.txt"]`  | 背景知识文件的路径列表，可以包含一个或多个文件。                   |
| `model_name`                 | 字符串       | `"qwen-long"`                 | 模型名称，指定具体使用的模型。                            |
| `max_tokens`                 | 整数         | 正整数，如 `1000`                  | 模型生成的最大 token 数量。                          |
| `n`                          | 整数         | 正整数，通常为 `1`                   | 生成结果的数量。                                   |
| `temperature`                | 浮点数       | `0.0` 到 `1.0`，如 `0.7`         | 控制生成的随机性，值越高结果越随机。                         |
| `use_files`                  | 布尔值       | `True` 或 `False`              | 是否使用文件上传的方式，将文件内容直接传递给模型。                  |

### 参数详细说明

- **`model_family`**：
  - **数据类型**：字符串
  - **说明**：指定使用的模型家族，例如 `"qwen"` 表示使用 Qwen 模型系列。
  - **可选值**：根据您所使用的模型服务商提供的模型系列名称。

- **`api_key`**：
  - **数据类型**：字符串
  - **说明**：用于身份验证的 API 密钥。**请务必替换为您的实际 API 密钥，不要公开分享。**

- **`prompt_file_path`**：
  - **数据类型**：字符串
  - **说明**：指向包含 `prompt` 内容的文件路径。`prompt` 通常包含对模型的指令、问题或上下文。
  - **示例**：`"prompt/教学效果.txt"`

- **`analysis_data_file_path`**：
  - **数据类型**：字符串
  - **说明**：待分析文本的文件路径，模型将对该文本进行分析。
  - **示例**：`"待分析文本.txt"`

- **`class_stand_text_file_path`**：
  - **数据类型**：字符串
  - **说明**：课程标准文本的文件路径，提供分析所需的背景信息。
  - **示例**：`"初中课程标准/初中生物课程标准.txt"`

- **`bc_knowledge_file_paths`**：
  - **数据类型**：列表（字符串）
  - **说明**：背景知识文件路径的列表，可以包含一个或多个文件，提供额外的背景信息。
  - **示例**：`["背景知识/教学效果.txt", "背景知识/教学方法.txt"]`

- **`model_name`**：
  - **数据类型**：字符串
  - **说明**：指定具体使用的模型名称。
  - **可选值**：根据模型服务商提供的模型名称，例如 `"qwen-long"`。

- **`max_tokens`**：
  - **数据类型**：整数
  - **说明**：限制模型生成的最大 token 数量，防止生成过长的文本。
  - **示例**：`1000`

- **`n`**：
  - **数据类型**：整数
  - **说明**：指定生成结果的数量，通常为 `1`。
  - **示例**：`1`

- **`temperature`**：
  - **数据类型**：浮点数
  - **说明**：控制生成文本的随机性。值越高，生成的文本越随机；值越低，生成的文本越有确定性。
  - **取值范围**：`0.0` 到 `1.0`
  - **示例**：`0.7`

- **`use_files`**：
  - **数据类型**：布尔值
  - **说明**：是否采用文件上传的方式，将文件内容直接传递给模型。设置为 `False` 时，文件内容会读取后作为字符串传递。
  - **可选值**：`True` 或 `False`

## 使用步骤

1. **准备文件**：确保所有在 `params` 中指定的文件路径都存在，并且文件内容符合要求。

2. **配置参数**：根据您的需求修改 `params` 字典中的参数值。

3. **调用 `get_result` 函数**：将 `params` 作为参数传入 `get_result` 函数。

4. **获取结果**：`get_result` 函数将返回模型的分析结果，您可以对结果进行进一步处理或输出。

## 示例代码

```python
import os
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
    params = {
        "model_family": "qwen",
        "api_key": "your_api_key_here",  # 请替换为您的实际 API 密钥
        "prompt_file_path": "prompt/教学效果.txt",
        "analysis_data_file_path": "待分析文本.txt",
        "class_stand_text_file_path": "初中课程标准/初中生物课程标准.txt",
        "bc_knowledge_file_paths": [
            "背景知识/教学效果.txt",
            "背景知识/教学方法.txt",
            "背景知识/课堂活动.txt",
            "背景知识/问答行为.txt"
        ],
        "model_name": "qwen-long",
        "max_tokens": 1000,
        "n": 1,
        "temperature": 0.7,
        "use_files": False,
    }

    # 调用 get_result 函数获取最终结果
    result = get_result(params)
    print(result)
```

## 注意事项

- **API 密钥安全**：请务必保护好您的 `api_key`，不要将其公开发布或提交到公共仓库。

- **文件路径有效性**：确保 `params` 中指定的所有文件路径都是有效的，文件存在并且内容正确。

- **编码格式**：本代码默认使用 `utf-8` 编码读取文件，如果您的文件使用其他编码，请修改 `open` 函数中的 `encoding` 参数。

- **错误处理**：建议在实际使用中添加错误处理机制，捕获文件读取错误或模型调用异常。

## 常见问题

**1. 如何修改分析的维度？**

您可以通过更改 `params` 中的 `prompt_file_path` 和 `bc_knowledge_file_paths` 来调整分析的维度。例如：

```python
# 修改为教学方法维度
params["prompt_file_path"] = "prompt/教学方法.txt"
params["bc_knowledge_file_paths"] = ["背景知识/教学方法.txt"]
```

**2. 如何增加或减少背景知识文件？**

您可以在 `bc_knowledge_file_paths` 列表中添加或移除文件路径。例如：

```python
# 只使用教学效果和教学方法的背景知识
params["bc_knowledge_file_paths"] = [
    "背景知识/教学效果.txt",
    "背景知识/教学方法.txt"
]
```

**3. 如果模型返回的结果过长或过短，如何调整？**

您可以修改 `max_tokens` 参数来控制模型生成的文本长度。

- 增加 `max_tokens`：允许模型生成更长的文本。
- 减少 `max_tokens`：限制模型生成的文本长度。

**4. 如何提高模型生成结果的随机性？**

您可以调整 `temperature` 参数：

- 增加 `temperature`（最高为 `1.0`）：结果更随机，创造性更强。
- 减少 `temperature`（最低为 `0.0`）：结果更确定，保守性更高。

## 联系方式

如果您在使用过程中遇到问题，欢迎与我们联系以获得支持。