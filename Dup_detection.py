import os
import functions as func

cwd = os.getcwd()
groups = ['Group 1.txt', 'Group 2.txt', 'Group 3.txt', 'Group 4.txt', 'Group 5.txt', 'Group 6.txt']
retry_txt = os.path.join(cwd,'classified','retry.txt')
retry_lst = []
with open(retry_txt, 'r', encoding='utf-8') as f:
    while True:
        line = f.readline()
        if not line: break
        line = line.strip()
        retry_lst.append(line)

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
                splitted_line = line.split('/-/')
                if len(splitted_line) < 2:
                    print(line)
                    continue
                origins.append(splitted_line[0].strip())
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
                        print(origins[j], origins[i])
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

def contains_word(word, origin):
    if len(word) > len(origin):
        return False
    W = len(word)
    O = len(origin)
    for i in range(O-W+1):
        if origin[i:i + W] == word:
            return True
    return False

def contains_word_groups(word, groups):
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
                splitted_line = line.split('/-/')
                if len(splitted_line) < 2:
                    print(line)
                    continue
                origin = splitted_line[0].strip()
                answer = splitted_line[1].strip()
                retry_string = ""
                if origin in retry_lst:
                    retry_string = " - (retry)"
                if contains_word(word, origin):
                    print(f"({group}) {origin}: {answer}{retry_string}")
                    found = True
                elif not func.contains_kanji(word):
                    # if not func.is_kanji_word(origin):
                    if contains_word(word, func.extract_pronounciations(line)):
                        print(f"({group}) {origin}: {answer}{retry_string}")
                        found = True
                
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
            contains_word_groups(word, groups)
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