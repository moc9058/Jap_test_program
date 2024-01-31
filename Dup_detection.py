import os
import functions as func
import random

cwd = os.getcwd()
groups = ['Group 1.txt', 'Group 2.txt', 'Group 3.txt', 'Group 4.txt', 'Group 5.txt', 'Group 6.txt']
retry_txt = os.path.join(cwd,'classified','retry.txt')
verbs_txt = os.path.join(cwd,'classified','verbs.txt')
adverbs_txt = os.path.join(cwd,'classified','adverbs.txt')
diff_kanjis_txt = os.path.join(cwd,'classified','diff_kanjis.txt')
katakanas_txt = os.path.join(cwd,'classified','katakanas.txt')
compounds_txt = os.path.join(cwd,'classified','compounds.txt')
expressions_txt = os.path.join(cwd,'classified','expressions.txt')
adjectives_txt = os.path.join(cwd,'classified','adjectives.txt')
pure_kanjis_txt = os.path.join(cwd,'classified','pure_kanjis.txt')
etc_txt = os.path.join(cwd,'classified','etc.txt')

retry_lst = []
verb_lst = []
adverb_lst = []
diff_kanji_lst = []
katakana_lst = []
compound_lst = []
expression_lst = []
adjective_lst = []
pure_kanji_lst = []
etc_lst = []

append_txts = [verbs_txt, adverbs_txt, diff_kanjis_txt, katakanas_txt,\
                compounds_txt, expressions_txt, adjectives_txt, pure_kanjis_txt,\
                etc_txt]
append_lsts = [verb_lst, adverb_lst, diff_kanji_lst, katakana_lst,\
            compound_lst, expression_lst, adjective_lst, pure_kanji_lst,\
            etc_lst]

retry_lst = []
for i in range(len(append_txts)):
    class_txt = append_txts[i]
    with open(class_txt, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line: break
            line = line.strip()
            append_lsts[i].append(line)
verb_total = verb_lst.copy()
verb_total.extend(compound_lst)
verb_total.sort()

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

def contains_word_groups(word, groups, shuffle = True):
    cwd = os.getcwd()
    found = False
    
    retry_lst = []
    with open(retry_txt, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line: break
            line = line.strip()
            retry_lst.append(line)            


    print_lst = ['verbs','others']
    for i in range(2):
        word_print_lst = []
        print("----------------------------------------------------")
        print(f"({print_lst[i]})")
        print("----------------------------------------------------")
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
                        print(f"Error: {line}")
                        continue
                    origin = splitted_line[0].strip()
                    answer = splitted_line[1].strip()
                    retry_string = ""
                    if i == 0 and not origin in verb_total:
                        continue
                    elif i == 1 and origin in verb_total:
                        continue
                    if origin in retry_lst:
                        retry_string = " - (retry)"
                    if contains_word(word, origin):
                        # print(f"({group}) {origin}: {answer}{retry_string}")
                        word_print_lst.append(f"({group}) {origin}: {answer}{retry_string}")
                        found = True
                    elif not func.contains_kanji(word):
                        # if not func.is_kanji_word(origin):
                        if contains_word(word, func.extract_pronounciations(line)):
                            # print(f"({group}) {origin}: {answer}{retry_string}")
                            word_print_lst.append(f"({group}) {origin}: {answer}{retry_string}")
                            found = True
        if shuffle:
            random.shuffle(word_print_lst)
        for word_print in word_print_lst:
            print(word_print)
    if not found:
        print(f"Not found")
    print()
def real_time_dup_detect(groups, shuffle):
    while True:
        word = input()
        if not word:
            break
        word = word.strip()
        if word.lower() in ['x','ｘ']:
            break
        else:
            contains_word_groups(word, groups, shuffle)
            # try:
            #     contains_word_groups(word, groups)
            # except Exception as e:
            #     print(e)
            print()
print("Select mode")
print("Default: find duplication for real time, shuffled.")
print("-----------------------------------------")
print("e: find duplication among existing txts.")
print("n: find duplication among existing txts, ordered.")

mode = input()
if mode in ['E','e','え']:
    automatic_dup_detect(groups)
elif mode in ['N','n','ｎ']:
    real_time_dup_detect(groups, shuffle = False)
else:
    real_time_dup_detect(groups, shuffle = True)

# print(duplicate(os.path.join('test_log','2023_09_01_18_43_53.txt')))