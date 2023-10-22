import os
import openai
import signal
import time
from multiprocessing import Process, Array
from threading import Thread

import functions as func

# openai.api_key = os.getenv("OPENAI_API_KEY")
# word_1 = '付き合う'
# word_2 = '罷り通る'
# response = openai.ChatCompletion.create(
#     model = "gpt-4",
#     messages=[
#     {"role": "user", "content": f"Compose an example sentence using \"{word_2}\" without any additional explanation."}
#   ]
# )
array = Array('i',200)
def create_contents(array):
    generated_contents = "\u6628\u65e5\u306e\u96e8\u306f\u4e00\u6669\u4e2d\u7f77\u308a\u901a\u308b\u96e8\u3067\u3001\u5730\u5143\u306e\u5ddd\u304c\u6c3e\u6feb\u3059\u308b\u307e\u3067\u306b\u306a\u3063\u305f\u3002"
    for i in range(len(generated_contents)):
        array[i]= ord(generated_contents[i])
create_contents(array)
contents = ""
for i in range(len(array)):
    contents += chr(array[i])
print(contents)
print(len(contents))