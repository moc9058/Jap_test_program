import os
import openai
import signal
import time
from multiprocessing import Process, Value, Array
from threading import Thread

import functions as func
messages = "\u6628\u65e5\u306e\u96e8\u306f\u4e00\u6669\u4e2d\u7f77\u308a\u901a\u308b\u96e8\u3067\u3001\u5730\u5143\u306e\u5ddd\u304c\u6c3e\u6feb\u3059\u308b\u307e\u3067\u306b\u306a\u3063\u305f\u3002"
# openai.api_key = os.getenv("OPENAI_API_KEY")
# word_1 = '付き合う'
# word_2 = '罷り通る'
# response = openai.ChatCompletion.create(
#     model = "gpt-4",
#     messages=[
#     {"role": "user", "content": f"Compose an example sentence using \"{word_2}\" without any additional explanation."}
#   ]
# )
def signal_handler(signum, frame):
    if __name__ != "__main__":
        pass
array = Array('i',200)
pid_num = Value('i')
def create_contents(pid, array, sec=0):
    pid.value = os.getpid()
    i = 0
    while i < 100:
        time.sleep(1)
        i += 1
        array[0] = i

if __name__ == '__main__':
    for i in range(5):
        p1 = Process(target=create_contents, args=(pid_num, array,))
        p1.start()
        time.sleep(4)
        print(f"parent: {os.getpid()}")
        print(f"child: {pid_num.value}")
        print(f"value: {array[0]}")
        print()
        try:
            os.kill(pid_num.value, signal.SIGTERM)
        except:
            # Already executed
            pass
        p1.join()

