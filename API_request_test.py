# -*- coding: utf-8 -*-

import os
from openai import OpenAI
from multiprocessing import Process, Value, Array
from threading import Thread

import functions as func
purpose = "自己紹介"
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
completion = client.chat.completions.create(
            messages=[
				{"role": "user", "content": f"Can you revise my professional summary?"},
				{"role": "user", "content": f"Possess a robust academic foundation in quantitative analysis, encompassing areas such as statistics, data visualization and programming. I am seeking a challenging professional position that leverages my strong interpersonal skills, excellent time management abilities, and problem-solving skills within the public sector."}
            ],
            model="gpt-4"
        )
content = completion.choices[0].message.content

print(content)
# def signal_handler(signum, frame):
#     if __name__ != "__main__":
#         pass
# array = Array('i',200)
# pid_num = Value('i')
# def create_contents(pid, array, sec=0):
#     pid.value = os.getpid()
#     i = 0
#     while i < 100:
#         time.sleep(1)
#         i += 1
#         array[0] = i

# if __name__ == '__main__':
#     for i in range(5):
#         p1 = Process(target=create_contents, args=(pid_num, array,))
#         p1.start()
#         time.sleep(4)
#         print(f"parent: {os.getpid()}")
#         print(f"child: {pid_num.value}")
#         print(f"value: {array[0]}")
#         print()
#         try:
#             os.kill(pid_num.value, signal.SIGTERM)
#         except:
#             # Already executed
#             pass
#         p1.join()

