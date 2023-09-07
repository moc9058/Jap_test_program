import os
import glob
from datetime import datetime
import time
import random


def create_txts(lst):
    for txt in lst:
        if not os.path.isfile(txt):
            with open(txt, 'w') as f:
                pass

def is_katakana(string):
    for i in range(len(string)):
        char = string[i]
        if ord(char) < 12449 or ord(char) >= 12541:
            return False
    return True

def contains_kanji(string):
    for i in range(len(string)):
        char = string[i]
        if ord(char) < 12353:
            return True
        elif ord(char) >= 12439 and ord(char) < 12449:
            return True
        elif ord(char) >= 12541:
            return True
    return False

def print_word_duplicated(txt_name):
    origin_lst = []
    dup_lst = []
    with open(txt_name, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line: break
            origin_lst.append(line.strip())
    for i in range(len(origin_lst)):
        for j in range(i):
            if origin_lst[i] == origin_lst[j]:
                dup_lst.append(origin_lst[i])
    if dup_lst:
        print(f"{os.path.basename(txt_name)}\n{dup_lst}")
    else:
        return
    
def word_count(txt_name):
    count = 0
    with open(txt_name, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line: break
            count += 1
    return count

def properly_included(member_txt_lst, group_txt):
    improper_words = []
    group_words = []
    with open(group_txt, 'r', encoding='utf-8') as group_f:
        while True:
            line = group_f.readline()
            if not line: break
            group_words.append(line.strip())
    
    for member_txt in member_txt_lst:
        with open(member_txt, 'r', encoding='utf-8') as member_f:
            while True:
                line = member_f.readline()
                if not line: break
                line = line.split('/-/')[0].strip()
                if not (line in group_words):
                    improper_words.append(f"{os.path.basename(member_txt)}, {line}")
                else:
                    group_words.remove(line)
    return improper_words, group_words

def copy_txt2lst(lst,txt):
    with open(txt,'r',encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line: break
            lst.append(line.strip()+'\n')

def copy_txt2lst_combined(lsts, txts):
    if len(lsts) != len(txts):
        print("Lengths are different.")
        return
    for i in range(len(lsts)):
        copy_txt2lst(lsts[i],txts[i])

def append_lst2txt(lst,txt):
    txt_words_lst = []
    with open(txt,'r',encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line: break
            txt_words_lst.append(line.strip())
    with open(txt,'a',encoding='utf-8') as f:
        while lst:
            word = lst.pop(0).strip()
            if not word in txt_words_lst:
                f.write(f"{word}\n")

def append_lst2txt_combined(lsts, txts):
    if len(lsts) != len(txts):
        print("Lengths are different.")
        return
    for i in range(len(lsts)):
        append_lst2txt(lsts[i], txts[i])

def word_count_combined(txts):
    result = 0
    for txt in txts:
        result += word_count(txt)
    return result

def print_word_duplicated_combined(txts):
    for txt in txts:
        print_word_duplicated(txt)

cwd = os.getcwd()
save_folder = os.path.join(cwd,'test_log')

retry_txt = os.path.join(cwd,'classified','retry.txt')
verbs_txt = os.path.join(cwd,'classified','verbs.txt')
adverbs_txt = os.path.join(cwd,'classified','adverbs.txt')
diff_kanjis_txt = os.path.join(cwd,'classified','diff_kanjis.txt')
katakanas_txt = os.path.join(cwd,'classified','katakanas.txt')
jinn_ninn_txt = os.path.join(cwd,'classified','jinn_ninn.txt')
komu_txt = os.path.join(cwd,'classified','komu.txt')
etc_txt = os.path.join(cwd,'classified','etc.txt')

retry_lst = []
verb_lst = []
adverb_lst = []
diff_kanji_lst = []
katakana_lst = []
jinn_ninn_lst = []
komu_lst = []
etc_lst = []


classified_txts = [retry_txt, verbs_txt, adverbs_txt, diff_kanjis_txt, katakanas_txt,\
                  jinn_ninn_txt, komu_txt,\
                  etc_txt]
classified_lsts = [retry_lst, verb_lst, adverb_lst, diff_kanji_lst, katakana_lst,\
                  jinn_ninn_lst, komu_lst,\
                  etc_lst]
append_txts = [verbs_txt, adverbs_txt, diff_kanjis_txt, katakanas_txt,\
              jinn_ninn_txt, komu_txt,\
              etc_txt]
append_lsts = [verb_lst, adverb_lst, diff_kanji_lst, katakana_lst,\
              jinn_ninn_lst, komu_lst,\
              etc_lst]

if not os.path.exists(save_folder):
    os.mkdir(save_folder)
create_txts(classified_txts)

date_files = sorted(glob.glob(os.path.join(save_folder,"*.txt")))
katakana_reverse = False

completed_words_lst = []
if len(date_files) > 0:
    last_test = date_files[-1]
    with open(last_test, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line: break
            completed_words_lst.append(line.strip())

copy_txt2lst_combined(classified_lsts, classified_txts)

print('Do you want to test retry words? Default is \"NO\".')
print('A: adverbs.txt')
print('D: diff_kanjis.txt')
print('J: jinn_ninn.txt')
print('K: katakanas.txt')
print('M: komu.txt')
print('R: retry.txt')
print('V: verbs.txt')
first_input = input()
answer_groups = ['Group 1.txt', 'Group 2.txt', 'Group 3.txt', 'Group 4.txt', 'Group 5.txt', 'Group 6.txt']
groups = []
if len(first_input) == 0:
    input_retry = False 
    groups = answer_groups.copy()
else:
    input_retry = True
    for i in range(len(first_input)):
        if first_input[i].lower() == 'x':
            break
        elif first_input[i].lower() == 'r':
            groups.append(os.path.join('classified','retry.txt'))
        elif first_input[i].lower() == 'v':
            groups.append(os.path.join('classified','verbs.txt'))
        elif first_input[i].lower() == 'k':
            groups.append(os.path.join('classified','katakanas.txt'))
        elif first_input[i].lower() == 'a':
            groups.append(os.path.join('classified','adverbs.txt'))
        elif first_input[i].lower() == 'd':
            groups.append(os.path.join('classified','diff_kanjis.txt'))
        elif first_input[i].lower() == 'j' or first_input[i].lower() == 'n':
            groups.append(os.path.join('classified','jinn_ninn.txt'))
        elif first_input[i].lower() == 'm':
            groups.append(os.path.join('classified','komu.txt'))
        
print()


origins = []
answers = []
if not input_retry:
    for group_index in range(len(groups)):
        group = groups[group_index]
        filename = os.path.join(cwd, group)
        
        if not os.path.isfile(filename):
            continue
        
        with open(filename,'r', encoding='utf-8') as f:
            while True:
                line = f.readline()
                if not line: break
                line = line.split('/-/')
                if len(line) < 2:
                    print(f"Format error in {group}: {line}")
                    continue
                origin = line[0].strip()
                answer = line[1].strip()
                if not input_retry:
                    if not origin in completed_words_lst:
                        if not origin in origins:
                            origins.append(origin)
                            answers.append(answer)
                else:
                    if not origin in origins:
                        origins.append(origin)
                        answers.append(answer)
else:
    for group_index in range(len(groups)):
        group = groups[group_index]
        filename = os.path.join(cwd, group)
        
        if not os.path.isfile(filename):
            continue
        
        with open(filename,'r', encoding='utf-8') as f:
            while True:
                line = f.readline()
                if not line: break
                line = line.split('/-/')
                if len(line) < 2:
                    print(f"Format error in {group}: {line}")
                    continue
                origin = line[0].strip()
                answer = line[1].strip()
                if not input_retry:
                    if not origin in completed_words_lst:
                        if not origin in origins:
                            origins.append(origin)
                            answers.append(answer)
                else:
                    if not origin in origins:
                        origins.append(origin)
                        answers.append(answer)

is_adverb = (first_input == 'a' or first_input == 'A')

while origins:
    rand_index = random.randrange(len(origins))
    word = origins[rand_index]
    if not input_retry:
        print(f"(origin: {len(origins)}, completed: {len(completed_words_lst)}, total: {len(origins)+len(completed_words_lst)})", end=" ")
    else:
        print(f"({len(origins)} left)", end=" ")
    try_again = ""
    group = ""

    if origins[rand_index] in retry_lst:
        try_again = "(retry)"
    katakana_reverse = is_katakana(origins[rand_index])
    if katakana_reverse:
        print(f"{answers[rand_index]} {group}{try_again}", end=" ")
        input_X = input()
        print(origins[rand_index], end=" ")
    elif is_adverb:
        if contains_kanji(origins[rand_index]):
            ans_split_index = answers[rand_index].find(" ")
            print(f"{answers[rand_index][:ans_split_index].strip()} {group}{try_again}", end=" ")
            input_X = input()
            print(f"{origins[rand_index]} {answers[rand_index][ans_split_index:].strip()}", end=" ")
        else:
            print(f"{origins[rand_index]} {group}{try_again}", end=" ")
            input_X = input()
            print(answers[rand_index], end=" ")
    else:
        print(f"{origins[rand_index]} {group}{try_again}", end=" ")
        input_X = input()
        print(answers[rand_index], end=" ")
    if input_X.lower() == 'x':
        if not input_retry:
            append_lst2txt_combined(append_lsts,append_txts)
        break
    time.sleep(0.5)
    if not input_retry:
        input_X = input()
        if input_X.lower() == 'x':
            append_lst2txt_combined(append_lsts,append_txts)
            break
        elif input_X.lower() == 'v':
            verb_lst.append(f"{origins[rand_index]}/-/{answers[rand_index]}")
            completed_words_lst.append(origins[rand_index])
            del origins[rand_index]
            del answers[rand_index]
        elif input_X.lower() == 'a':
            adverb_lst.append(f"{origins[rand_index]}/-/{answers[rand_index]}")
            completed_words_lst.append(origins[rand_index])
            del origins[rand_index]
            del answers[rand_index]
        elif input_X.lower() == 'd':
            diff_kanji_lst.append(f"{origins[rand_index]}/-/{answers[rand_index]}")
            completed_words_lst.append(origins[rand_index])
            del origins[rand_index]
            del answers[rand_index]
        elif input_X.lower() == 'k':
            katakana_lst.append(f"{origins[rand_index]}/-/{answers[rand_index]}")
            completed_words_lst.append(origins[rand_index])
            del origins[rand_index]
            del answers[rand_index]
        elif input_X.lower() == 'j' or input_X.lower() == 'n':
            jinn_ninn_lst.append(f"{origins[rand_index]}/-/{answers[rand_index]}")
            completed_words_lst.append(origins[rand_index])
            del origins[rand_index]
            del answers[rand_index]
        elif input_X.lower() == 'm':
            komu_lst.append(f"{origins[rand_index]}/-/{answers[rand_index]}")
            completed_words_lst.append(origins[rand_index])
            del origins[rand_index]
            del answers[rand_index]
        elif input_X == '2' or input_X.lower() == 'o':
            etc_lst.append(f"{origins[rand_index]}/-/{answers[rand_index]}")
            completed_words_lst.append(origins[rand_index])
            del origins[rand_index]
            del answers[rand_index]
        else:
            if not origins[rand_index] in retry_lst:
                with open(retry_txt, 'a', encoding='utf-8') as f:
                    f.write(f"{origins[rand_index]}/-/{answers[rand_index]}\n")
                retry_lst.append(origins[rand_index])
    else:
        input_X = input()
        if input_X.lower() == 'x':
            break
        elif input_X == '2' or input_X.lower() in ['o','a','v','d','j','n','m','d','k']:
            completed_words_lst.append(origins[rand_index])
            del origins[rand_index]
            del answers[rand_index]
    print()
if not input_retry:
    append_lst2txt_combined(append_lsts,append_txts)
    currtime_txt = os.path.join(save_folder, datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+".txt")
    with open(currtime_txt, 'wt', encoding='utf-8') as f:
        for word in completed_words_lst:
            f.write(word+"\n")

print()

last_test = sorted(glob.glob(os.path.join(save_folder,"*.txt")))[-1]
print_word_duplicated_combined(classified_txts)

print(word_count_combined(append_txts) , word_count(last_test))
print(properly_included(append_txts,last_test))

# print(ord('ぁ'))
# for i in range(0,86):
#     print(chr(12353+i))
# print(ord('ァ'))
# for i in range(0,92):
#     print(chr(12449+i))