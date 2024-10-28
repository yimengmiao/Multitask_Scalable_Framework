import pandas as pd
import re


# 定义一个函数来去除中文和英文标点符号
def remove_punctuation(text):
    punctuation = '，。！？、；：「」『』（）《》〈〉＂＇［］〔〕【】—…–·,.;:?!"\'()[]{}<>~`@#$%^&*_+-=/\\|'
    return re.sub(f"[{re.escape(punctuation)}]", "", text)


# 定义最长公共子串函数
def longest_common_substring(s1, s2):
    m = len(s1)
    n = len(s2)
    # 创建一个二维数组来存储中间结果
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    longest = 0
    lcs_end = 0
    for i in range(m):
        for j in range(n):
            if s1[i] == s2[j]:
                dp[i + 1][j + 1] = dp[i][j] + 1
                if dp[i + 1][j + 1] > longest:
                    longest = dp[i + 1][j + 1]
                    lcs_end = i + 1
    # 返回最长公共子串和其长度
    return s1[lcs_end - longest:lcs_end], longest


# 创建 original_data DataFrame
data = {
    'start_time': [234250, 238210, 240550, 250810, 258080, 260290, 261380, 265710, 270090, 270470,
                   273660, 275480, 278850, 280310, 284180, 286960, 288810, 292830, 295810, 299640,
                   299640, 303240, 304160, 307170, 309490, 310540],
    'end_time': [238210, 240480, 244470, 253750, 260120, 260900, 265140, 270090, 270450, 273170,
                 275280, 278210, 279650, 284180, 286520, 288220, 291850, 295810, 299640, 300270,
                 300270, 303880, 305640, 309070, 310190, 313990],
    'text': [
        '瞧那么一句话，就能把故事的意思讲出来了，',
        '小朋友们真能干，好，',
        '那我们来看看哦，他为什么什么树都没种成呢？',
        '我们来读课文的第一段，来，谁来读？',
        '等一下啊，张老师困扰了。嗯，',
        '好，你来读',
        '猴子，种了一棵梨树苗天，',
        '天浇水施肥等着将来吃梨子，',
        '嗯，',
        '你不要坐下，是不天天说明什么呀？',
        '就是每天',
        '哎每天对呀，就说明这个猴子怎么样',
        '很细心，',
        '很细心，还有呢，他每天都去浇，',
        '天天都去浇水，施肥说明他怎么样',
        '勤劳淡实，',
        '英语非常勤劳，猴子是不是很好，你们看，',
        '这个猴子种树啊，它有一个动作的过程，',
        '你找到了动作的吗？它有哪些动作？好，',
        '那就好了，',
        '那就好了，',
        '浇水',
        '天气就直接浇水了吗？',
        '所以先说重好的，然后呢，',
        '胶水',
        '嗯浇，嗯，施肥，'
    ],
    'label': [0, 0, 0, 0, 0, 0, 1, 1, 1, 0,
              1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
              0, 1, 0, 0, 1, 0]
}

original_data = pd.DataFrame(data)

# 在 original_data 中创建一个新的列，去除标点符号
original_data['text_no_punct'] = original_data['text'].apply(remove_punctuation)

# 提供更新后的 test 数据
test = {
    'split': {
        'sub1': {
            'd_number': [1],
            'sub_theme': '老师问学生猴子为什么没有种成树，但没有学生回答。',
            'sub_text': '发起：好，那我们来看看哦，他为什么什么树都没种成呢？\n回应：[空白]'
        },
        'sub2': {
            'd_number': [2, 3, 4],
            'sub_theme': '老师要求学生读课文，学生读了部分内容，老师引导学生理解“天天”的意思。',
            'sub_text': '发起：我们来读课文的第一段，来，谁来读？\n回应：[空白]\n\n发起：嗯，好，你来读\n回应：猴子，种了一棵梨树苗天，天浇水施肥等着将来吃梨子，嗯，\n\n发起：是不天天说明什么呀？\n回应：就是每天\n讲解：英语非常勤劳，'
        },
        'sub3': {
            'd_number': [5],
            'sub_theme': '老师讲解猴子的行为，并引导学生观察猴子的行为，但没有得到回应。',
            'sub_text': '讲解：猴子是不是很好，\n发起：你们看，\n回应：[空白]'
        },
        'sub4': {
            'd_number': [6],
            'sub_theme': '老师引导学生找出猴子种树的动作，学生回答了一个动作。',
            'sub_text': '发起：这个猴子种树啊，它有一个动作的过程，你找到了动作的吗？它有哪些动作？\n回应：浇水'
        }
    },
    'theme': {
        'theme': '老师通过提问和解释，引导学生理解猴子种树的过程和其行为的意义。'
    }
}

# 初始化全局 current_index
global_current_index = 0
previous_end_time = None  # 用于存储前一个条目的 end_time

# 处理 test['split'] 中的每个子条目
for key in test['split']:
    entry = test['split'][key]
    sub_text = entry['sub_text']
    # 处理 sub_text，得到 modified_strings
    original_strings = [item for item in sub_text.split("\n") if "回应" not in item and item != ""]
    modified_strings = [s.replace("发起：", "").replace("讲解：", "") for s in original_strings]
    modified_strings_no_punct = [remove_punctuation(s) for s in modified_strings]

    # 初始化 start_time 和 end_time
    start_time = None
    end_time = None

    # 判断 modified_strings 的长度
    if len(modified_strings) == 1:
        # 处理单个字符串的情况
        single_string_no_punct = modified_strings_no_punct[0]
        found = False
        # 首先尝试快速匹配
        for idx in range(global_current_index, len(original_data)):
            row = original_data.iloc[idx]
            if (single_string_no_punct in row['text_no_punct']) or (row['text_no_punct'] in single_string_no_punct):
                start_time = row['start_time']
                end_time = row['end_time']
                global_current_index = idx  # 更新全局 current_index
                found = True
                break
        # 如果快速匹配失败，尝试最长公共子串匹配
        if not found:
            max_length = 0
            match_idx = -1
            for idx in range(global_current_index, min(global_current_index + 3, len(original_data))):
                row = original_data.iloc[idx]
                lcs, length = longest_common_substring(single_string_no_punct, row['text_no_punct'])
                # 判断最长公共子串长度是否占比超过70%
                if length >= 0.7 * len(single_string_no_punct) or length >= 0.7 * len(row['text_no_punct']):
                    if length > max_length:
                        max_length = length
                        match_idx = idx
            if match_idx != -1:
                row = original_data.iloc[match_idx]
                start_time = row['start_time']

                end_time = row['end_time']
                global_current_index = match_idx  # 更新全局 current_index
            else:
                print(f"未找到匹配的文本：{modified_strings[0]}")
                # 为 start_time 和 end_time 赋予默认值
                if previous_end_time is not None:
                    start_time = previous_end_time
                    end_time = start_time
                    print(f"使用前一个条目的 end_time 作为当前的 start_time: {start_time}")
                else:
                    start_time = original_data.iloc[0]['start_time']
                    end_time = start_time
                    print(f"使用 original_data 第一行的 start_time 作为当前的 start_time: {start_time}")
    else:
        # 处理多个字符串的情况，只匹配第一个和最后一个字符串
        # 匹配第一个字符串，获取 start_time
        first_string_no_punct = modified_strings_no_punct[0]
        found_start = False
        # 首先尝试快速匹配
        for idx in range(global_current_index, len(original_data)):
            row = original_data.iloc[idx]
            if (first_string_no_punct in row['text_no_punct']) or (row['text_no_punct'] in first_string_no_punct):
                start_time = row['start_time']
                global_current_index = idx  # 更新全局 current_index
                found_start = True
                break
        # 如果快速匹配失败，尝试最长公共子串匹配
        if not found_start:
            max_length = 0
            match_idx = -1
            for idx in range(global_current_index, min(global_current_index + 3, len(original_data))):
                row = original_data.iloc[idx]
                lcs, length = longest_common_substring(first_string_no_punct, row['text_no_punct'])
                if length >= 0.7 * len(first_string_no_punct) or length >= 0.7 * len(row['text_no_punct']):
                    if length > max_length:
                        max_length = length
                        match_idx = idx
            if match_idx != -1:
                row = original_data.iloc[match_idx]
                start_time = row['start_time']
                global_current_index = match_idx  # 更新全局 current_index
                found_start = True
            else:
                print(f"未找到匹配的起始文本：{modified_strings[0]}")
                # 为 start_time 赋予默认值
                if previous_end_time is not None:
                    start_time = previous_end_time
                    print(f"使用前一个条目的 end_time 作为当前的 start_time: {start_time}")
                else:
                    start_time = original_data.iloc[0]['start_time']
                    print(f"使用 original_data 第一行的 start_time 作为当前的 start_time: {start_time}")

        # 匹配最后一个字符串，获取 end_time
        last_string_no_punct = modified_strings_no_punct[-1]
        found_end = False
        # 首先尝试快速匹配
        for idx in range(global_current_index, len(original_data)):
            row = original_data.iloc[idx]
            if (last_string_no_punct in row['text_no_punct']) or (row['text_no_punct'] in last_string_no_punct):

                end_time = row['end_time']
                global_current_index = idx  # 更新全局 current_index
                found_end = True
                break
        # 如果快速匹配失败，尝试最长公共子串匹配
        if not found_end:
            max_length = 0
            match_idx = -1
            for idx in range(global_current_index, min(global_current_index + 3, len(original_data))):
                row = original_data.iloc[idx]
                lcs, length = longest_common_substring(last_string_no_punct, row['text_no_punct'])
                if length >= 0.7 * len(last_string_no_punct) or length >= 0.7 * len(row['text_no_punct']):
                    if length > max_length:
                        max_length = length
                        match_idx = idx
            if match_idx != -1:
                row = original_data.iloc[match_idx]
                # todo:要解决end_time匹配短的问题，再往original_data的下一行与single_string_no_punct再进行一次文本匹配或者是最长公共子文本匹配，如果满足其中一个，就把end_time更新为当前行的end_time

                end_time = row['end_time']
                global_current_index = match_idx  # 更新全局 current_index
                found_end = True
            else:
                print(f"未找到匹配的结束文本：{modified_strings[-1]}")
                # 为 end_time 赋予默认值
                temp_start_time = None
                # 尝试从下一个条目中获取 start_time
                keys = list(test['split'].keys())
                current_idx = keys.index(key)
                if current_idx + 1 < len(keys):
                    next_key = keys[current_idx + 1]
                    next_entry = test['split'][next_key]
                    if 'start_time' in next_entry:
                        temp_start_time = next_entry['start_time']
                    elif 'end_time' in next_entry:
                        temp_start_time = next_entry['end_time']
                    if temp_start_time is not None:
                        end_time = temp_start_time
                        print(f"使用下一个条目的 start_time 作为当前的 end_time: {end_time}")
                    else:
                        # 使用 original_data 最后一行的 end_time
                        end_time = original_data.iloc[-1]['end_time']
                        print(f"使用 original_data 最后一行的 end_time 作为当前的 end_time: {end_time}")
                else:
                    # 当前条目是最后一个，使用 original_data 最后一行的 end_time
                    end_time = original_data.iloc[-1]['end_time']
                    print(f"使用 original_data 最后一行的 end_time 作为当前的 end_time: {end_time}")

    # 更新 entry，并保存 previous_end_time
    # 检查时间顺序
    if start_time is not None and end_time is not None:
        if start_time > end_time:
            print(f"时间顺序错误，start_time({start_time}) > end_time({end_time})，交换之")
            entry['start_time'], entry['end_time'] = end_time, start_time
        else:
            entry['start_time'] = start_time
            entry['end_time'] = end_time
    else:
        if start_time is not None:
            entry['start_time'] = start_time
        if end_time is not None:
            entry['end_time'] = end_time
    previous_end_time = entry.get('end_time', previous_end_time)  # 更新 previous_end_time
print("test", test)
# 输出处理后的 test['split']
for key in test['split']:
    entry = test['split'][key]
    print(f"{key}:")
    print(entry)
    print()
