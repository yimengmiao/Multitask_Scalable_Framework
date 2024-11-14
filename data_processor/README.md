1. **输入**：场景中的师生对话。

2. **Prompt1**：执行“老师四分类任务”。
   - [prompt1_input_data_process.py](prompt1_input_data_process.py)的功能是处理**输入**并生成 Prompt1 的输入数据。
   - 在业务代码 **teacher_classification_api_version.py** 中使用到这个 Prompt1 的输入，并最终输出 Prompt1 的结果。

3. **Prompt2**：查找“讲解断点”。
   - [prompt2_input_data_process.py](prompt2_input_data_process.py)**dialogue_split.py** 用于处理 Prompt1 的输出，并将其构造成 Prompt2 的输入格式。
   - 在业务代码 **topic_extractor_step1.py** 中，使用 Prompt2 的输入并输出 Prompt2 的结果。

4. **Prompt3**：输出场景主题。
   - Prompt2 的结果经过 [prompt3_input_data_process.py](prompt3_input_data_process.py)处理，生成 Prompt3 的输入。
   
