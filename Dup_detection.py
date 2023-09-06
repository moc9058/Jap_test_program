import os
cwd = os.getcwd()
groups = ['Group 1.txt', 'Group 2.txt', 'Group 3.txt', 'Group 4.txt', 'Group 5.txt', 'Group 6.txt']
cumulative_lengths = []
origins = []
origin_index = 0
for group_index in range(len(groups)):
    group = groups[group_index]
    filename = os.path.join(cwd, group)
    
    if not os.path.isfile(filename):
        # print(filename)
        continue
    
    with open(filename,'r', encoding='utf-8') as f:
        num_lines = 0
        while True:
            line = f.readline()
            if not line:break
            if len(line) < 2:
                print(line)
                continue
            origins.append(line.split('/-/')[0])
            num_lines += 1
        cumulative_lengths.append(len(origins))

        for i in range(origin_index, origin_index + num_lines):
            for j in range(i):
                if origins[i] == origins[j]:
                    k = len(cumulative_lengths)-1
                    while k >= 0:
                        if cumulative_lengths[k] <= j:
                            break
                        k -= 1
                    k += 1
                    print(groups[k], group)
                    print(origins[i])
                    print()
                            
        origin_index += num_lines
    print()

def duplicate(txt_name):
    txt = os.path.join(os.getcwd(),txt_name)
    lst = []
    with open(txt, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line: break
            if line in lst:
                return True
            lst.append(line.strip())
    return False

# print(duplicate(os.path.join('test_log','2023_09_01_18_43_53.txt')))