import os
import re

def split_text_by_sentences_and_save(input_file_name, max_length=1500, directory='./txt'):
    try:
        with open(input_file_name, "r", encoding='utf-8') as file:
            text = file.read()

        # 使用正则表达式查找句号来分割文本，同时保留句号
        sentences = re.split(r'(\S.+?。)', text)
        sentences = [s for s in sentences if s.strip()]  # 去除空白项

        # 重新组合句子，使分段每部分尽可能不超过最大长度
        segments = []
        current_segment = ""

        for sentence in sentences:
            # 检查当前句子加入后是否会超过最大长度
            if len(current_segment) + len(sentence) <= max_length:
                current_segment += sentence
            else:
                # 如果添加当前句子会超出长度限制，则先保存当前段落
                segments.append(current_segment)
                current_segment = sentence  # 开始新的段落

        # 添加最后一个段落，如果有的话
        if current_segment:
            segments.append(current_segment)

        # 确保目标目录存在
        os.makedirs(directory, exist_ok=True)

        # 将每个段落保存为一个文件
        for index, segment in enumerate(segments, start=1):
            file_path = os.path.join(directory, f"{index}.txt")
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(segment)

        print(f"共生成了{len(segments)}个文件。")
    except Exception as e:
        print(f"处理过程中出现错误: {e}")

# 调用函数，传入 input.txt
split_text_by_sentences_and_save('input.txt')