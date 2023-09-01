import os

file = os.path.join(os.getcwd(),'classified','etc.txt')
with open(file, 'r', encoding='utf-8') as f:
    while True:
        line = f.readline()
        if not line: break
        line = line.strip()
        if line[-1] in ['う','る','つ','ぶ','ぬ','む','く','ぐ','す']:
            print(line)