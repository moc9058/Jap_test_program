import os
import glob
from datetime import datetime
import time
import random

import functions as func

            
cwd = os.getcwd()
save_folder = os.path.join(cwd,'test_log')
group_1_txt = os.path.join(cwd,'Group 1.txt')
group_2_txt = os.path.join(cwd,'Group 2.txt')
group_3_txt = os.path.join(cwd,'Group 3.txt')

retry_txt = os.path.join(cwd,'classified','retry.txt')
verbs_txt = os.path.join(cwd,'classified','verbs.txt')
adverbs_txt = os.path.join(cwd,'classified','adverbs.txt')
diff_kanjis_txt = os.path.join(cwd,'classified','diff_kanjis.txt')
katakanas_txt = os.path.join(cwd,'classified','katakanas.txt')
hononyms_txt = os.path.join(cwd,'classified','hononyms.txt')
compounds_txt = os.path.join(cwd,'classified','compounds.txt')
expressions_txt = os.path.join(cwd,'classified','expressions.txt')
etc_txt = os.path.join(cwd,'classified','etc.txt')

retry_lst = []
verb_lst = []
adverb_lst = []
diff_kanji_lst = []
katakana_lst = []
hononym_lst = []
compound_lst = []
expression_lst = []
etc_lst = []

classified_txts = [retry_txt, verbs_txt, adverbs_txt, diff_kanjis_txt, katakanas_txt,\
                  hononyms_txt, compounds_txt, expressions_txt,\
                  etc_txt]
classified_lsts = [retry_lst, verb_lst, adverb_lst, diff_kanji_lst, katakana_lst,\
                  hononym_lst, compound_lst, expression_lst,\
                  etc_lst]
append_txts = [verbs_txt, adverbs_txt, diff_kanjis_txt, katakanas_txt,\
              hononyms_txt, compounds_txt, expressions_txt,\
              etc_txt]
append_lsts = [verb_lst, adverb_lst, diff_kanji_lst, katakana_lst,\
              hononym_lst, compound_lst, expression_lst,\
              etc_lst]

if not os.path.exists(save_folder):
    os.mkdir(save_folder)
func.create_txts(classified_txts)

func.copy_txt2lst_combined(classified_lsts, classified_txts)

print('Do you want to test retry words? Default is \"NO\".')
print('A: adverbs.txt')
print('D: diff_kanjis.txt')
print('J: hononym.txt')
print('K: katakanas.txt')
print('C: compound.txt')
print('E: expression.txt')
print('R: retry.txt')
print('V: verbs.txt')
first_input = input()
answer_groups = ['Group 1.txt']
origin_candidates = []
answer_candidates = []
for answer_group in answer_groups:
    filename = os.path.join(cwd,answer_group)

    if not os.path.isfile(filename):
        continue

    with open(filename,'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line: break
            line = line.split('/-/')
            if len(line) < 2:
                print(f"Format error in {answer_group}: {line}")
                continue
            origin_candidates.append(line[0].strip())
            answer_candidates.append(line[1].strip())

date_files = sorted(glob.glob(os.path.join(save_folder,"*.txt")))
katakana_reverse = False

completed_words_lst = []
if len(date_files) > 0:
    last_test = date_files[-1]
    with open(last_test, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line: break
            line = line.strip()
            # print(line)
            if line in origin_candidates:
                completed_words_lst.append(line)



groups = []
if len(first_input) == 0:
    input_retry = False 
    groups = answer_groups
else:
    input_retry = True
    for i in range(len(first_input)):
        if first_input[i].lower() == 'x':
            func.update_lst2txt_combined(classified_lsts,classified_txts, origin_candidates)
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
        elif first_input[i].lower() == 'h':
            groups.append(os.path.join('classified','hononyms.txt'))
        elif first_input[i].lower() == 'c':
            groups.append(os.path.join('classified','compounds.txt'))
        elif first_input[i].lower() == 'e':
            groups.append(os.path.join('classified','expressions.txt'))
        
print()
    

origins = []
answers = []
if not input_retry:
    origins = origin_candidates.copy()
    answers = answer_candidates.copy()
    for i in range(len(completed_words_lst)):
        word = completed_words_lst[i]
        if word in origins:
            j = origins.index(word)
            del origins[j]
            del answers[j]

else:
    for group in groups:
        filename = os.path.join(cwd, group)
        
        if not os.path.isfile(filename):
            continue
        
        with open(filename,'r', encoding='utf-8') as f:
            while True:
                line = f.readline()
                if not line: break
                
                origins.append(line.strip())
    for i in range(len(origins)):
        origin = origins[i]
        try:
            origin_index = origin_candidates.index(origin)
            answers.append(answer_candidates[origin_index])
        except:
            raise Exception(f"{origin} is not included in Groups 1.txt, ...")
        
        

# is_adverb = (first_input == 'a' or first_input == 'A')

while origins:
    rand_index = random.randrange(len(origins))
    origin = origins[rand_index].strip()
    answer = answers[rand_index].strip()
    if not input_retry:
        print(f"(origin: {len(origins)}, completed: {len(completed_words_lst)}, total: {len(origins)+len(completed_words_lst)})", end=" ")
    else:
        print(f"({len(origins)} left)", end=" ")
    try_again = ""
    if origin in retry_lst:
        try_again = "(retry)"
    katakana_reverse = func.is_katakana(origin)
    is_adverb = False

    classified_name = ""
    classified_lst = []
    if origin in adverb_lst:
        classified_lst = adverb_lst
        classified_name = '(adverb.txt)'
        is_adverb = True
    elif origin in diff_kanji_lst:
        classified_lst = diff_kanji_lst
        classified_name = '(diff_kanjis.txt)'
    elif origin in etc_lst:
        classified_lst = etc_lst
        classified_name = '(etc.txt)'
    elif origin in hononym_lst:
        classified_lst = hononym_lst
        classified_name = '(hononym.txt)'
    elif origin in katakana_lst:
        classified_lst = katakana_lst
        classified_name = '(katakanas.txt)'
    elif origin in compound_lst:
        classified_lst = compound_lst
        classified_name = '(compounds.txt)'
    elif origin in expression_lst:
        classified_lst = expression_lst
        classified_name = '(expressions.txt)'
    elif origin in verb_lst:
        classified_lst = verb_lst
        classified_name = '(verbs.txt)'



    if katakana_reverse:
        print(f"{answer} {classified_name}{try_again}", end=" ")
        input_X = input()
        print(origin, end=" ")
    elif is_adverb:
        if func.contains_kanji(origin):
            ans_split_index = answer.find(" ")
            print(f"{answer[:ans_split_index].strip()} {classified_name}{try_again}", end=" ")
            input_X = input()
            print(f"{origin} {answer[ans_split_index:].strip()}", end=" ")
        else:
            print(f"{origin} {classified_name}{try_again}", end=" ")
            input_X = input()
            print(answer, end=" ")
    else:
        print(f"{origin} {classified_name}{try_again}", end=" ")
        input_X = input()
        print(answer, end=" ")
    if input_X.lower() == 'x':
        print()
        break
    time.sleep(0.5)
    if not input_retry:
        input_X = input()
        if input_X.lower() == 'x':
            break
        elif input_X.lower() == 'v':
            try:
                classified_lst.remove(origin)
            except:
                pass

            if not origin in verb_lst:
                verb_lst.append(origin)
            
            completed_words_lst.append(origin)
            del origins[rand_index]
            del answers[rand_index]
        elif input_X.lower() == 'a':
            try:
                classified_lst.remove(origin)
            except:
                pass

            if not origin in adverb_lst:
                adverb_lst.append(origin)   
            completed_words_lst.append(origin)
            del origins[rand_index]
            del answers[rand_index]
        elif input_X.lower() == 'd':
            try:
                classified_lst.remove(origin)
            except:
                pass
            
            if not origin in diff_kanji_lst:
                diff_kanji_lst.append(origin)
            completed_words_lst.append(origin)
            del origins[rand_index]
            del answers[rand_index]
        elif input_X.lower() == 'k':
            try:
                classified_lst.remove(origin)
            except:
                pass
            
            if not origin in katakana_lst:
                katakana_lst.append(origin)
            completed_words_lst.append(origin)
            del origins[rand_index]
            del answers[rand_index]
        elif input_X.lower() == 'h':
            try:
                classified_lst.remove(origin)
            except:
                pass
            
            if not origin in hononym_lst:
                hononym_lst.append(origin)
            completed_words_lst.append(origin)
            del origins[rand_index]
            del answers[rand_index]
        elif input_X.lower() == 'c':
            try:
                classified_lst.remove(origin)
            except:
                pass
            
            if not origin in compound_lst:
                compound_lst.append(origin)
            completed_words_lst.append(origin)
            del origins[rand_index]
            del answers[rand_index]
        elif input_X.lower() == 'e':
            try:
                classified_lst.remove(origin)
            except:
                pass
            
            if not origin in expression_lst:
                expression_lst.append(origin)
            completed_words_lst.append(origin)
            del origins[rand_index]
            del answers[rand_index]
        elif input_X == '2' or input_X.lower() == 'o':
            try:
                classified_lst.remove(origin)
            except:
                pass
            
            if not origin in etc_lst:
                etc_lst.append(origin)
            completed_words_lst.append(origin)
            del origins[rand_index]
            del answers[rand_index]
        else:
            if not origin in retry_lst:
                retry_lst.append(origin)
    else:
        input_X = input()
        if input_X.lower() == 'x':
            break
        elif input_X == '2' or input_X.lower() in ['o','a','v','d','h','c','d','k']:
            del origins[rand_index]
            del answers[rand_index]
    print()

if not input_retry:
    func.update_lst2txt_combined(classified_lsts,classified_txts, origin_candidates)
    currtime_txt = os.path.join(save_folder, datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+".txt")
    with open(currtime_txt, 'wt', encoding='utf-8') as f:
        for word in completed_words_lst:
            if word in origin_candidates:
                f.write(word+"\n")

print()
func.seperation(['人','日','名','存', '下', '大'], hononyms_txt,[adverbs_txt, diff_kanjis_txt, etc_txt])

last_test = sorted(glob.glob(os.path.join(save_folder,"*.txt")))[-1]
func.print_word_duplicated_combined(classified_txts)

print(func.word_count_combined(append_txts), func.word_count(last_test))
print(func.properly_included(append_txts,last_test))

func.sort(group_1_txt)

if os.path.isfile(group_2_txt):
    func.sort(group_2_txt)

if os.path.isfile(group_3_txt):
    func.sort(group_3_txt)