# -*- coding: utf-8 -*-

import os
from openai import OpenAI
from multiprocessing import Process, Value, Array
from threading import Thread

import functions as func
purpose = "introduction"
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
completion = client.chat.completions.create(
            messages=[
            # {"role": "user", "content": f"私は{purpose}を作成しています。"},
            # {"role": "user", "content": f"次の文を修正してもらえますか？"},
				{"role": "user", "content": f"I'm writing a statement for the {purpose}."},
				{"role": "user", "content": f"Can you revise the followings?"},
				{"role": "user", "content": f"The necessary dependencies include pandas, scipy, numpy, pytorch, as well as all additional libraries required by the original LibAUC. Also, you need CheXpert datasets with a file of train_valid_test.csv, train and valid folders."}
            ],
            model="gpt-4"
        )
content = completion.choices[0].message.content

print(content)
