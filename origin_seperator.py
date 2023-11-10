import os

cwd = os.getcwd()

group_2_txt = os.path.join(cwd,'Group 2.txt')
group_txt = os.path.join(cwd,'Group_newly_added_origins.txt')
group_lst = []

with open(group_2_txt, 'r', encoding='utf-8') as f:
    while True:
        line = f.readline()
        if not line: break
        line_splitted = line.split('/-/')
        if len(line_splitted) < 2:
            raise Exception(f"{line} has something wrong.")
        group_lst.append(line_splitted[0].strip())

group_lst.sort()
with open(group_txt, 'w', encoding='utf-8') as f:
    while group_lst:
        f.write(group_lst.pop(0)+'\n')