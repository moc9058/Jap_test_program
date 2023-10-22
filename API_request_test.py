import os
import openai
import signal
import time
from threading import Thread

# openai.api_key = os.getenv("OPENAI_API_KEY")
# word_1 = '付き合う'
# word_2 = '罷り通る'
# response = openai.ChatCompletion.create(
#     model = "gpt-4",
#     messages=[
#     {"role": "user", "content": f"Compose an example sentence using \"{word_2}\" without any additional explanation."}
#   ]
# )
# print(response['choices'][0]['message']['content'])

def append_lst(lst):
	count = 0
	while count < 10:
		time.sleep(1)
		lst.append(count)
		print(count)
		count += 1
lst = []
t = Thread(target=append_lst, args=(lst,))
t.start()
print(lst)
time.sleep(2)
try:
	signal.raise_signal(signal.SIGINT)
	t.join()
except KeyboardInterrupt:
	print('hi')
	print(lst)
print(lst)