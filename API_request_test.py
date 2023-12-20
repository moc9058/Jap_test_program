# -*- coding: utf-8 -*-

import os
from openai import OpenAI
from multiprocessing import Process, Value, Array
from threading import Thread

import functions as func
purpose = "自己PR"
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
completion = client.chat.completions.create(
            messages=[
            {"role": "user", "content": f"私は{purpose}を作成しています。"},
            {"role": "user", "content": f"次の文を修正してもらえますか？制限は400字です。"},
				# {"role": "user", "content": f"I'm writing a statement for the {purpose}."},
				# {"role": "user", "content": f"Can you revise the followings?"},
				{"role": "user", "content": f"学科のサッカー部（部員３０人）の部長として１年間務めました。部長に就任した年の前年度大会で全競技を負けて、その年には変えたかったのです。問題点が大きく３つあり、一つは毎週訓練参加率が低すぎて自体競技が不可能なこと、もう一つはチームメンバーたちが自信を持っていないこと、あまり一つは個人ドリブル能力が得意な選手がないことでした。それで一応独特な罰金制度を導入し、毎週訓練参加者を平均７人から１４人まで上がりました。そして先輩や担当教授に伺い、およそ１０万円ほどの支援金をもらい、このお金で訓練装備を買い替えました。なお訓練する際にはドリブルよりパスプレーを強調し、チームメンバー同士のコミュニケーション能力を上げました。その結果、その年の大会では全体２０チーム中２０位から１１位まで成績が上がり、チームのコミュニケーションの大切さを感じました。"}
            ],
            model="gpt-4"
        )
content = completion.choices[0].message.content

print(content)
