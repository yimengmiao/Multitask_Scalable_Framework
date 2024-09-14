import json

import pandas as pd


# 老师四分类任务中的数据处理逻辑，具体是：将课堂音频转译文本分割为一个个师生对话文本段。
class TeacherDialogueClassificationProcessor:
    def __init__(self, dataset, T):
        """
        初始化教师对话分类处理器
        :param dataset: DataFrame格式的数据
        :param T: 时间差阈值
        """
        self.dataset = dataset
        self.T = T

    def discard_student_before_first_teacher(self):
        """
        去掉第一个label为0的老师话语之前的所有学生话语（label为1的记录）
        """
        if (self.dataset['label'] == 0).any():
            first_teacher_idx = self.dataset[self.dataset['label'] == 0].index[0]
            self.dataset = self.dataset.loc[first_teacher_idx:].reset_index(drop=True)
        else:
            raise ValueError("No label=0 rows found in the dataset")

    def split_dataset(self):
        """
        按时间差和标签分割数据集
        """
        df = self.dataset
        last_teacher_end_time = df.iloc[0]['end_time']  # 第一个教师话语的 end_time 作为初始时间
        current_start = 0  # 当前分割的起始点
        sub_datasets = []  # 存储子数据集

        for i in range(1, len(df)):
            if df.iloc[i]['label'] == 0:  # 遇到教师话语
                time_interval = df.iloc[i]['start_time'] - last_teacher_end_time  # 计算时间间隔

                # 检查是否需要分割
                if time_interval > self.T or any(df.iloc[j]['label'] == 1 for j in range(current_start, i)):
                    # 触发分割
                    sub_datasets.append(df.iloc[current_start:i])  # 将current_start到i-1的记录作为子数据集
                    current_start = i  # 更新分割起点为当前教师话语的索引

                # 更新last_teacher_end_time为当前教师话语的end_time
                last_teacher_end_time = df.iloc[i]['end_time']

        # 如果遍历结束后仍有数据未分割，处理最后一个子数据集
        if current_start < len(df):
            sub_datasets.append(df.iloc[current_start:])

        return sub_datasets

    def convert_punctuation_to_chinese(self, text):
        """
        将英文标点符号转换为中文标点符号
        """
        punctuations = {
            ',': '，',
            '.': '。',
            '?': '？',
            '!': '！',
            ':': '：',
            ';': '；',
            '"': '“',
            '\'': '‘',
            '(': '（',
            ')': '）',
            '[': '【',
            ']': '】'
        }

        for eng_punc, zh_punc in punctuations.items():
            text = text.replace(eng_punc, zh_punc)

        return text

    def merge_text_by_label(self, sub_df):
        """
        按相同的label合并文本，并处理特殊情况
        """
        merged_rows = []
        current_text = self.convert_punctuation_to_chinese(sub_df.iloc[0]['text'])  # 转换标点符号
        current_start_time = sub_df.iloc[0]['start_time']
        current_end_time = sub_df.iloc[0]['end_time']
        current_label = sub_df.iloc[0]['label']

        for i in range(1, len(sub_df)):
            row = sub_df.iloc[i]
            if row['label'] == current_label:
                current_text += row['text']
                current_end_time = row['end_time']
            else:
                merged_rows.append({
                    'start_time': current_start_time,
                    'end_time': current_end_time,
                    'text': current_text,
                    'label': current_label
                })
                current_text = row['text']
                current_start_time = row['start_time']
                current_end_time = row['end_time']
                current_label = row['label']

        merged_rows.append({
            'start_time': current_start_time,
            'end_time': current_end_time,
            'text': current_text,
            'label': current_label
        })

        if len(merged_rows) == 1 and merged_rows[0]['label'] == 0:
            merged_rows.append({
                'start_time': merged_rows[0]['start_time'],
                'end_time': merged_rows[0]['end_time'],
                'text': "",
                'label': 1
            })

        return pd.DataFrame(merged_rows)

    def process(self):
        """
        处理教师对话分类任务
        """
        # 丢弃第一个老师话语（label为0）之前的学生话语
        self.discard_student_before_first_teacher()

        # 分割数据
        sub_dfs = self.split_dataset()

        json_list = []
        for sub_df in sub_dfs:
            processed_sub_df = self.merge_text_by_label(sub_df)
            json_list.append(processed_sub_df.to_json(orient='records', force_ascii=False))
        json_list = [json.loads(item) for item in json_list]
        t_s_list = []
        for item in json_list:
            teacher_text = ""
            student_text = ""

            # 处理item中的每个对话
            for sub_item in item:
                if sub_item['label'] == 0:
                    teacher_text += sub_item['text'] + " "
                elif sub_item['label'] == 1:
                    student_text += sub_item['text'] + ""

            # 构建分析师生对话段文本
            # 如果学生话语为空字符串，那么text_to_analyze改为f"""“老师话语”：{teacher_text.strip()}"""

            if student_text:
                text_to_analyze = f"""
                “老师话语”：{teacher_text}
                “学生话语”：{student_text}
                """
            else:
                text_to_analyze = f"""“老师话语”：{teacher_text}"""
            t_s_list.append(text_to_analyze)
        return t_s_list