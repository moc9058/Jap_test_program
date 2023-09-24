import os
groups = ['Group 1.txt', 'Group 2.txt', 'Group 3.txt', 'Group 4.txt', 'Group 5.txt', 'Group 6.txt']
    
def automatic_dup_detect(groups):
    cwd = os.getcwd()
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

def contains_word(word, groups):
    cwd = os.getcwd()
    found = False
    for group_index in range(len(groups)):
        group = groups[group_index]
        filename = os.path.join(cwd, group)
        
        if not os.path.isfile(filename):
            # print(filename)
            continue
        
        with open(filename,'r', encoding='utf-8') as f:
            while True:
                line = f.readline()
                if not line:break
                if len(line) < 2:
                    print(line)
                    continue
                origin = line.split('/-/')[0].strip()
                if len(origin) < len(word):
                    continue
                else:
                    for i in range(len(origin)-len(word)+1):
                        if origin[i:i+len(word)] == word:
                            print(f"{group}: {origin}")
                            group_index = len(groups) + 1
                            found = True
                            break
                
    if not found:
        print(f"Not found")
def real_time_dup_detect(groups):
    while True:
        word = input()
        if not word:
            break
        elif word.lower() == 'x':
            break
        else:
            contains_word(word, groups)
            print()
print("Select mode")
print("e: find duplication among existing txts.")
print("r: find duplication for real time.")
mode = input()
if mode.lower() == 'e':
    automatic_dup_detect(groups)
elif mode.lower() == 'r':
    real_time_dup_detect(groups)

# print(duplicate(os.path.join('test_log','2023_09_01_18_43_53.txt')))