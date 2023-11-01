# -*- coding: utf-8 -*-

import os
import openai
from multiprocessing import Process, Value, Array
from threading import Thread

import functions as func

openai.api_key = os.getenv("OPENAI_API_KEY")
response = openai.ChatCompletion.create(
    model = "gpt-4",
    messages=[
    {"role": "user", "content": f"私は自己紹介を書いています。次の文から文法的に間違う部分を修正してください。"},
    {"role": "user", "content": f"私はムン・ヒョンウと申します。今、ソウル大学農学部４年です。アピールが大きく２つあります。まず、１つ目は学業です。私はコンピュータ工学を二重専攻しつつ、コンピュータ工学全般に渡る知識を身に付けました。さらに、数学に得意があって８割の授業でA成績をもらいました。２つ目はインターンシップ経験です。AIモデルを開発する会社で働いた際にデータアノテーションの効率を約６０％改善したことがあります。私が持っている知識と実務経験を活かして新しい技術を学びながら新しいサービスを実現できると思っております。"}
  ]
)

content = response['choices'][0]['message']['content']
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

