import os

cwd = os.getcwd()
group_1_txt = os.path.join(cwd,'Group 1.txt')
group_2_txt = os.path.join(cwd,'Group 2.txt')
group_3_txt = os.path.join(cwd,'Group 3.txt')

tmp = []
with open(group_1_txt,'r',encoding='utf-8') as f1:
    with open(group_2_txt,'r',encoding='utf-8') as f2:
        group_1_finished = False
        group_2_finished = False
        line_1 = f1.readline()
        if not line_1:
            group_1_finished = True
        line_2 = f2.readline()
        if not line_2:
            group_2_finished = True
        
        while not (group_1_finished or group_2_finished):
            if line_1 < line_2:
                tmp.append(line_1)
                line_1 = f1.readline()
            else:
                tmp.append(line_2)
                line_2 = f2.readline()
            if not line_1:
                group_1_finished = True
                break
            if not line_2:
                group_2_finished = True
                break
        
        if group_1_finished:
            tmp.append(line_2)
            while True:
                line_2 = f2.readline()
                if not line_2: break
                tmp.append(line_2)
        else: #group_2_finished
            tmp.append(line_1)
            while True:
                line_1 = f1.readline()
                if not line_1: break
                tmp.append(line_1)



            


with open(group_1_txt, 'w', encoding='utf-8') as f:
    while tmp:
        f.write(tmp.pop(0))
