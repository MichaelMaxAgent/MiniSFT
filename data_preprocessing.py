import requests
import json
import os
import re

url = 'https://api.xty.app/v1/chat/completions'

# 替换为您自己的API密钥
api_key = 'sk-6ANYYKAIQ9Z9qrou67D52bBd025e446f905dF34e2a5aA6Fd'

model = "gpt-3.5-turbo"

prompt1 = '''
#01 你是一个问答对数据集处理专家。

#02 你的任务是根据我给出的内容，生成适合作为问答对数据集的问题。

#03 问题要尽量短，不要太长。

#04 一句话中只能有一个问题。

#05 生成的问题必须宏观、价值，不要生成特别细节的问题。

#06 生成问题示例：

"""

权益型基金的特点有哪些方面？

介绍一下产品经理。

"""

#07 以下是我给出的内容：

"""

{{此处替换成你的内容}}

"""
'''

prompt2 = '''
#01 你是一个问答对数据集处理专家。

#02 你的任务是根据我的问题和我给出的内容，生成对应的问答对。

#03 答案要全面，多使用我的信息，内容要更丰富。

#04 你必须根据我的问答对示例格式来生成：

"""

{"prompt": "基金分类有哪些", "response": "基金分类主要包括股票型基金、债券型基金、货币市场基金、混合型基金、指数基金、QDII基金以及FOF基金等。"}

{"prompt": "基金是什么", "response": "基金，英文是fund，广义是指为了某种目的而设立的具有一定数量的资金。主要包括公积金、信托投资基金、保险基金、退休基金，各种基金会的基金。从会计角度透析，基金是一个狭义的概念，意指具有特定目的和用途的资金。我们提到的基金主要是指证券投资基金。"}

#05 我的问题如下：

"""

{{此处替换成你上一步生成的问题}}

"""

#06 我的内容如下：

"""

{{此处替换成你的内容}}

"""
'''

def generate_question(text_content, more=False):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    content = "生成适合作为问答对的问题"
    if more:
        content = "尽可能多生成适合作为问答对的问题"
    prompt = prompt1.replace("{{此处替换成你的内容}}", text_content)
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": content}
        ]
    }
    response = requests.post(url, headers=headers, json=data, verify=False)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]['content']
    else:
        print(f"Error: {response.status_code}")
        print(response.content)
        return None

def generate_qa(text_content, question_text=None):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    prompt = prompt2.replace("{{此处替换成你上一步生成的问题}}", question_text).replace("{{此处替换成你的内容}}", text_content)
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": "拼成问答对"}
        ]
    }
    response = requests.post(url, headers=headers, json=data, verify=False)
    if response.status_code == 200:
        print(response.json()["choices"][0]["message"]['content'])
        return response.json()["choices"][0]["message"]['content']
    else:
        print(f"Error: {response.status_code}")
        print(response.content)
        return None

def read_file(file_path):
    with open(file_path, "r", encoding='utf-8') as file:
        return file.read()

def write_to_json(data, file_path):
    with open(file_path, "w", encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def main():
    directory_path = './txt'
    all_qa_data = []

    # 遍历目录下的所有文件
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory_path, filename)
            text_content = read_file(file_path)

            # 生成问答对
            question_text = generate_question(text_content=text_content, more=True)
            qa_string = generate_qa(text_content=text_content, question_text=question_text)

            # 正确地分割 JSON 字符串，并确保每个部分都是有效的 JSON
            json_objects = re.split(r'\}(?=\s*\{)', qa_string)
            json_objects = [obj + '}' if not obj.strip().endswith('}') else obj for obj in json_objects]

            # 将字符串转换成 JSON 对象
            qa_data = [json.loads(obj) for obj in json_objects]
            all_qa_data.extend(qa_data)

    # 将所有问答对写入到一个 JSON 文件中
    json_output_path = './data/sft_train.json'
    write_to_json(all_qa_data, json_output_path)
    print(f"QA 对已经被写入 {json_output_path}")


if __name__ == "__main__":
    main()