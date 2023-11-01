# -*- coding: utf-8 -*-

import os
import openai
from multiprocessing import Process, Value, Array
from threading import Thread

import functions as func
purpose = "志望動機"
openai.api_key = os.getenv("OPENAI_API_KEY")
response = openai.ChatCompletion.create(
    model = "gpt-4",
    messages=[
    {"role": "user", "content": f"私は{purpose}を書いています。次の文から文法的またはニュアンス的に間違う部分を修正してください。"},
    {"role": "user", "content": f"貴社での業務を通して、人々の生活に役立つサービスを開発したいと考えています。これまで、コンピューター工学、数学、そして統計学を積極的に学んできました。また、インターンシップで画像分類AIを扱った経験があり、データアノテーションプロセスの改善作業を行ったことがあります。私は持っている知識とプログラミングスキルを活かし、新しい技術を学び、新しいサービスを開発し、最終的には人々の生活を豊かにすることが、私が目指しているキャリアパスです。貴社が膨大なデータと先進的な通信インフラを有しているため、私の能力を最大限に活かし、自身のキャリアパスを進める理想的な場所だと感じています。それが、私が貴社を志望する理由です。"}
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

