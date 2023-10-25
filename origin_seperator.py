import os

cwd = os.getcwd()

group_3_txt = os.path.join(cwd,'Group 3.txt')
group_3_lst = []

with open(group_3_txt, 'r', encoding='utf-8') as f:
    while True:
        line = f.readline()
        if not line: break
        line_splitted = line.split('/-/')
        if len(line_splitted) < 2:
            raise Exception(f"{line} has something wrong.")
        group_3_lst.append(line_splitted[0].strip())

with open(group_3_txt, 'w', encoding='utf-8') as f:
    while group_3_lst:
        f.write(group_3_lst.pop(0)+'\n')