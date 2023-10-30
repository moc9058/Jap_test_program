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
    {"role": "user", "content": f"私は情報革命を進めるために必要な基礎知識および能力を身につけています。１つ目は学業です。私はコンピュータ工学科を二重専攻しつつ、アルゴリズムやコンピュータ構造などのコンピュータ工学全般に渡る基礎知識を身につけました。さらに、数学科で受講したことにより、数学的証明能力を培いました。その結果、数学科の科目で総３０単位、１０科目中８科目でA成績をもらい、数学科の大学院授業では上位１０％以内に入るほど数学的証明に長けています。２つ目の経験はインターンシップです。約3ヶ月間、地雷探知ソフトウェアを開発するベンチャー企業で働いた経験があります。軍部隊から得た地雷の電気信号データを画像データに変換し、画像分類AIを用いて地雷の有無と種類、位置を特定するプログラムの開発が主な業務でした。AIの学習に必要なデータは軍部隊から提供を受け、それにラベルを付けました。しかし、提供されるデータ量の増加に伴い、既存の方法では限界が見えてきました。そのため、私はアノテーションの改善策を社長に提案し、それが認められて改善作業に取り組むことになりました。様々なショートカットキーの導入や、既存のAIモデルを用いて情報入力の速度を上げました。その結果、一人あたり一日の作業効率が約２５０個から約４００個まで上がりました。私が身に付いている知識を用いてAIモデルを学び、プログラミング経験を活かして実際サービス改善に貢献できると思います。"}
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

