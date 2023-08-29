import os

cwd = os.path.join(os.getcwd(),"OneDrive","바탕 화면","test_program")
groups = ['Group 1.txt','Group 2.txt','Group 3.txt']
group_1 = os.path.join(cwd,'Group 1.txt')
new_group = os.path.join(cwd,'tmp.txt')
with open(new_group,'w',encoding='utf-8') as f1:
    for group in groups:
        if not os.path.isfile(os.path.join(cwd,group)):
            continue
        with open(os.path.join(cwd,group),'r',encoding='utf-8') as f2:
            while True:
                line = f2.readline()
                if not line: break
                f1.write(line)

with open(group_1, 'w', encoding='utf-8') as f1:
    with open(new_group, 'r', encoding='utf-8') as f2:
        while True:
            line = f2.readline()
            if not line: break
            f1.write(line)


