# -*- coding: utf-8 -*-

import os
from openai import OpenAI
from multiprocessing import Process, Value, Array
from threading import Thread

import functions as func
purpose = "お知らせ"
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
completion = client.chat.completions.create(
            messages=[
				{"role": "user", "content": f"次の{purpose}文を修正してください。"},
				{"role": "user", "content": f"皆さん、こんばんは！担当実行委員、ひょんうです。重要なお知らせをご案内させていただきます。\n１)OT日の決定について\n日程上、OTを来週に進行することとなりました。それに伴い、OT参加可能時間帯の入力の締切を11月23日（木曜日）13時に設定します！急な進行ですみません。\n２)自己紹介シート作成について\nOTでは、行事の概要説明、自己紹介、そして事前学習日程の設定などが行われます。その中で、自己紹介についてのミッションがあります！OTの日まで下のシートを作成していただくことをお願いします！言語は日本語、韓国語どちらでも対応可能です。\n忙しい中、ご協力ありがとうございます！私たちも全力を尽くして本番を準備しておりますので、どうぞ楽しみにお待ちください。どうぞよろしくお願いします！"}
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

