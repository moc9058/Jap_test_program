import os
import openai
import signal
import time
from multiprocessing import Process, Value, Array
from threading import Thread

import functions as func

openai.api_key = os.getenv("OPENAI_API_KEY")
response = openai.ChatCompletion.create(
    model = "gpt-4",
    messages=[
    {"role": "user", "content": f"I want to have a discussion about \"media\" of Korea and Japan. Can you recommend me a proper topic?"},
    {"role": "assistant", "content": f"Be detailed as possible. Exclude a topic about KPOP."}
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

