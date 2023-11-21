# -*- coding: utf-8 -*-

import os
from openai import OpenAI
from multiprocessing import Process, Value, Array
from threading import Thread

import functions as func
purpose = "答弁"
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
completion = client.chat.completions.create(
            messages=[
				{"role": "user", "content": f"次の{purpose}文を修正してください。"},
				{"role": "user", "content": f"私が二重専攻を申し込んだ時期が2020年だったのですけど、コロナ禍後の世界では情報技術が生活に一段と浸透するはずだと思ってこれを学んでみようと思って二重専攻をし始めました。"}
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

