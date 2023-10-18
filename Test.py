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
group_4_txt = os.path.join(cwd,'Group 4.txt')

func.txt_sort(group_1_txt)

if os.path.isfile(group_2_txt):
    func.txt_sort(group_2_txt)

if os.path.isfile(group_3_txt):
    func.txt_sort(group_3_txt)

if os.path.isfile(group_4_txt):
    func.txt_sort(group_4_txt)

# Extract origins, answers
group_txt_lst = ['Group 1.txt', 'Group 2.txt', 'Group 3.txt']
group_1_origin = []
group_1_answer = [] 
group_2_origin = []
group_2_answer = [] 
group_3_origin = []
group_3_answer = [] 
group_origin_lsts = [group_1_origin, group_2_origin, group_3_origin]
group_answer_lsts = [group_1_answer, group_2_answer, group_3_answer]
origin_candidates = []
answer_candidates = []
for i in range(len(group_txt_lst)):
    answer_group = group_txt_lst[i]
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
    # origin_candidates.extend(group_origin_lsts[i])
    # answer_candidates.extend(group_answer_lsts[i])

retry_completed_txt = os.path.join(cwd,'retry_completed_txt.txt')
retry_completed_lst = []
classified_words_lst = []
probably_not_verb_lst = []
probably_verb_lst = []

retry_txt = os.path.join(cwd,'classified','retry.txt')
verbs_txt = os.path.join(cwd,'classified','verbs.txt')
adverbs_txt = os.path.join(cwd,'classified','adverbs.txt')
diff_kanjis_txt = os.path.join(cwd,'classified','diff_kanjis.txt')
katakanas_txt = os.path.join(cwd,'classified','katakanas.txt')
hononyms_txt = os.path.join(cwd,'classified','hononyms.txt')
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
hononym_lst = []
compound_lst = []
expression_lst = []
adjective_lst = []
pure_kanji_lst = []
etc_lst = []

classified_txts = [retry_txt, verbs_txt, adverbs_txt, diff_kanjis_txt, katakanas_txt,\
                  hononyms_txt, compounds_txt, expressions_txt, adjectives_txt, pure_kanjis_txt,\
                  etc_txt]
classified_lsts = [retry_lst, verb_lst, adverb_lst, diff_kanji_lst, katakana_lst,\
                  hononym_lst, compound_lst, expression_lst, adjective_lst, pure_kanji_lst,\
                  etc_lst]
append_txts = [verbs_txt, adverbs_txt, diff_kanjis_txt, katakanas_txt,\
              hononyms_txt, compounds_txt, expressions_txt, adjectives_txt, pure_kanjis_txt,\
              etc_txt]
append_lsts = [verb_lst, adverb_lst, diff_kanji_lst, katakana_lst,\
              hononym_lst, compound_lst, expression_lst, adjective_lst, pure_kanji_lst,\
              etc_lst]

if not os.path.exists(save_folder):
    os.mkdir(save_folder)
func.create_txt_combined(classified_txts)
func.create_txt(retry_completed_txt)

func.copy_txt2lst_combined(classified_lsts, classified_txts, origin_candidates)
func.copy_txt2lst(retry_completed_lst, retry_completed_txt, origin_candidates)
for append_lst in append_lsts:
    classified_words_lst.extend(append_lst)
for word in origin_candidates:
    if not word in classified_words_lst:
        if not func.not_verb(word):
            probably_verb_lst.append(word)
        else:
            probably_not_verb_lst.append(word)

random.shuffle(probably_verb_lst)
random.shuffle(probably_not_verb_lst)

unclassified_words_lst = probably_verb_lst

# Iniatiate retry_completed_lst
if len(retry_lst) <= len(retry_completed_lst):
    with open(retry_completed_txt, 'w', encoding='utf-8') as f:
        pass
    retry_completed_lst = []



date_files = sorted(glob.glob(os.path.join(save_folder,"*.txt")))
is_katakana = False

# Extract completed_words_lst
completed_words_lst = []
if len(date_files) > 0:
    last_test = date_files[-1]
    with open(last_test, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line: break
            line = line.strip()
            # print(line)
            if line in origin_candidates and not line in completed_words_lst:
                completed_words_lst.append(line)

# Check and extract duplicated words of completed_words_lst in classified folder.
tmp_completed_words = completed_words_lst.copy()
tmp_duplicated_count = 0
while tmp_completed_words:
    tmp_word = tmp_completed_words.pop(0)
    tmp_count = 0
    tmp_first_txt = ""
    for tmp_append_lst in append_lsts:
        if tmp_word in tmp_append_lst:
            tmp_count += 1
            if tmp_count == 1:
                tmp_first_txt = os.path.basename(append_txts[append_lsts.index(tmp_append_lst)])
            if tmp_count == 2:
                tmp_duplicated_count += 1
                print(f"{tmp_word}: {tmp_first_txt} {os.path.basename(append_txts[append_lsts.index(tmp_append_lst)])}", end=' ')
            if tmp_count > 2:
                print(os.path.basename(append_txts[append_lsts.index(tmp_append_lst)]), end=' ')
    
    if tmp_count > 1:
        print()
if tmp_duplicated_count > 1:
    print(f"Total number of duplicated words is {tmp_duplicated_count}.")



# Trace the number of classified words
num_classified = 0
num_candidates = len(origin_candidates)
for append_lst in append_lsts:
    num_classified += len(append_lst)


# Initiate program!
func.update_lst2txt(retry_lst, retry_txt, origin_candidates)
todays_retry = []
print('Do you want to test retry words? Default is \"NO\" and applying 1:1 mode.')
print('A: adverbs.txt')
print('D: diff_kanjis.txt')
print('K: katakanas.txt')
print('C: compounds.txt')
print('E: expressions.txt')
print('J: adjectives.txt')
print('P: pure_kanjis.txt')
print('R: retry.txt')
print('V: verbs.txt')
first_input = input()

groups = []
one_to_one_mode = False
pronounciation_mode = True
if len(first_input) == 0:
    input_retry = False 
    groups = group_txt_lst
    one_to_one_mode = True
elif not first_input[0].lower() in ['a','d','k','c','e','j','p','r','v','h','x']:
    input_retry = False
    groups = group_txt_lst
else:
    input_retry = True
    for i in range(len(first_input)):
        if first_input[i].lower() == 'x':
            func.update_lst2txt_combined(classified_lsts,classified_txts, origin_candidates)
            break
        elif first_input[i].lower() == 'r':
            groups = [os.path.join('classified','retry.txt')]
            first_input = 'r'
            break
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
        elif first_input[i].lower() == 'j':
            groups.append(os.path.join('classified','adjectives.txt'))
        elif first_input[i].lower() == 'p':
            groups.append(os.path.join('classified','pure_kanjis.txt'))
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
elif first_input == 'r':
    with open(retry_txt,'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line: break
            line = line.strip()
            if not line in retry_completed_lst:
                origins.append(line.strip())
    
    for i in range(len(origins)):
        origin = origins[i]
        try:
            origin_index = origin_candidates.index(origin)
            answers.append(answer_candidates[origin_index])
        except:
            raise Exception(f"{origin} is not included in groups, ...")
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
    

one_to_one_indicator = 0
unclassified_indicator = 0
while origins:
    # len(probably_not_verb_lst) == 0
    if len(unclassified_words_lst) == 0 and unclassified_indicator == 0:
        unclassified_words_lst = probably_not_verb_lst
        unclassified_indicator = 1
    elif len(unclassified_words_lst) == 0 and unclassified_indicator == 1:
        print("All words are classified!!")
        unclassified_words_lst = retry_lst.copy()
        for i in range(len(adjective_lst)):
            if not adjective_lst[i] in unclassified_words_lst:
                unclassified_words_lst.append(adjective_lst[i])
        for i in range(len(adverb_lst)):
            if not adverb_lst[i] in unclassified_words_lst:
                unclassified_words_lst.append(adverb_lst[i])
        unclassified_indicator = 2

    if not input_retry:
        print(f"(total: {len(origins)}, unclassified: {len(probably_verb_lst) + len(probably_not_verb_lst)})", end=" ")
    else:
        print(f"({len(origins)} left)", end=" ")
    rand_index = random.randrange(len(origins))
    origin = origins[rand_index].strip()
    answer = answers[rand_index].strip()
    is_katakana = func.is_katakana(origin)
    is_kanji = False
    classified_name = ""
    print_reverse = True
    
    if one_to_one_mode and one_to_one_indicator %2 == 1 and len(unclassified_words_lst) > 0 and not input_retry:
        tmp_rand_index = random.randrange(len(unclassified_words_lst))
        rand_index = origins.index(unclassified_words_lst[tmp_rand_index])
        origin = origins[rand_index].strip()
        answer = answers[rand_index].strip()
        is_katakana = func.is_katakana(origin)
        # print_reverse = not func.is_kanji_word(origin)
    else:
        classified_lst = []
        if origin in adverb_lst:
            classified_lst = adverb_lst
            classified_name = '(adverb.txt)'
        elif origin in diff_kanji_lst:
            classified_lst = diff_kanji_lst
            classified_name = '(diff_kanjis.txt)'
            # print_reverse = False
            is_kanji = True
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
        elif origin in adjective_lst:
            classified_lst = adjective_lst
            classified_name = '(adjectives.txt)'
        elif origin in pure_kanji_lst:
            classified_lst = pure_kanji_lst
            classified_name = '(pure_kanjis.txt)'
            # print_reverse = False
            is_kanji = True
        elif origin in verb_lst:
            classified_lst = verb_lst
            classified_name = '(verbs.txt)'


    try:
        if origin.index('（') == 0:
            origin_to_print = origin
        else:
            origin_to_print = origin[:origin.index('（')]
    except:
        origin_to_print = origin


    try_again = ""
    if origin in retry_lst:
        try_again = " - (retry)"
    
    one_to_one_indicator = (one_to_one_indicator+1)%2
    
    if func.contains_kanji(origin):
        pronounciation = answer.split()[0].strip()
    else:
        pronounciation = origin


    if (is_kanji or (origin in unclassified_words_lst and func.is_kanji_word(origin))) and pronounciation_mode:
        for i in range(len(origins)):
            tmp_origin = origins[i]
            tmp_answer = answers[i]
            if i != rand_index and tmp_answer.split()[0].strip() == pronounciation:
                if func.is_kanji_word(tmp_origin):
                    answer = f"{answer}\n{tmp_origin} {tmp_answer[tmp_answer.find(' ')+1:].strip()}"

    


    if is_katakana:
        print(f"{origin_to_print}{try_again}", end=" ")
        input_X = input()
        print(f"{answer} {classified_name}", end=" ")
    elif print_reverse:
        if func.contains_kanji(origin):
            ans_split_index = answer.find(" ")
            print(f"{answer[:ans_split_index].strip()}{try_again}", end=" ")
            input_X = input()
            print(f"{origin_to_print} {answer[ans_split_index:].strip()} {classified_name}", end=" ")
        else:
            print(f"{origin_to_print}{try_again}", end=" ")
            input_X = input()
            print(f"{answer} {classified_name}", end=" ")
    else:
        print(f"{origin_to_print}{try_again}", end=" ")
        input_X = input()
        print(f"{answer} {classified_name}", end=" ")
    
    if len(input_X) > 1:
        input_X = input_X[0]
    if input_X.lower() == 'x':
        print()
        break
    time.sleep(0.5)
    if not input_retry:
        input_X = input()
        input_Y = ""
        if len(input_X) > 1:
            input_Y = input_X[1]
            input_X = input_X[0]
        if input_X.lower() == 'x':
            break
        elif input_X.lower() == 'v':
            try:
                classified_lst.remove(origin)
            except:
                pass

            if not origin in verb_lst:
                verb_lst.append(origin)
                try:
                    unclassified_words_lst.remove(origin)
                except:
                    pass
                if not origin in classified_words_lst:
                    classified_words_lst.append(origin)

            if not origin in todays_retry:
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
                try:
                    unclassified_words_lst.remove(origin)
                except:
                    pass
                if not origin in classified_words_lst:
                    classified_words_lst.append(origin)

            if not origin in todays_retry:
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
                try:
                    unclassified_words_lst.remove(origin)
                except:
                    pass
                if not origin in classified_words_lst:
                    classified_words_lst.append(origin)

            if not origin in todays_retry:
                completed_words_lst.append(origin)
                if not origin in retry_lst:
                    del origins[rand_index]
                    del answers[rand_index]

        elif input_X.lower() == 'k':
            try:
                classified_lst.remove(origin)
            except:
                pass
            
            if not origin in katakana_lst:
                katakana_lst.append(origin)
                try:
                    unclassified_words_lst.remove(origin)
                except:
                    pass
                if not origin in classified_words_lst:
                    classified_words_lst.append(origin)

            if not origin in todays_retry:
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
                try:
                    unclassified_words_lst.remove(origin)
                except:
                    pass
                if not origin in classified_words_lst:
                    classified_words_lst.append(origin)

            if not origin in todays_retry:
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
                try:
                    unclassified_words_lst.remove(origin)
                except:
                    pass
                if not origin in classified_words_lst:
                    classified_words_lst.append(origin)

            if not origin in todays_retry:
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
                try:
                    unclassified_words_lst.remove(origin)
                except:
                    pass
                if not origin in classified_words_lst:
                    classified_words_lst.append(origin)

            if not origin in todays_retry:
                completed_words_lst.append(origin)
                del origins[rand_index]
                del answers[rand_index]
        elif input_X.lower() == 'j':
            try:
                classified_lst.remove(origin)
            except:
                pass
            
            if not origin in adjective_lst:
                adjective_lst.append(origin)
                try:
                    unclassified_words_lst.remove(origin)
                except:
                    pass
                if not origin in classified_words_lst:
                    classified_words_lst.append(origin)

            if not origin in todays_retry:
                completed_words_lst.append(origin)
                del origins[rand_index]
                del answers[rand_index]
        elif input_X.lower() == 'p':
            try:
                classified_lst.remove(origin)
            except:
                pass
            
            if not origin in pure_kanji_lst:
                pure_kanji_lst.append(origin)
                try:
                    unclassified_words_lst.remove(origin)
                except:
                    pass
                if not origin in classified_words_lst:
                    classified_words_lst.append(origin)

            if not origin in todays_retry:
                completed_words_lst.append(origin)
                if not origin in retry_lst:
                    del origins[rand_index]
                    del answers[rand_index]
        elif input_X == '2' or input_X.lower() == 'o':
            try:
                classified_lst.remove(origin)
            except:
                pass
            
            if not origin in etc_lst:
                etc_lst.append(origin)
                try:
                    unclassified_words_lst.remove(origin)
                except:
                    pass
                if not origin in classified_words_lst:
                    classified_words_lst.append(origin)

            if not origin in todays_retry:
                completed_words_lst.append(origin)
                del origins[rand_index]
                del answers[rand_index]
        elif not input_X.lower() == 'n':
            if not (origin in pure_kanji_lst or origin in diff_kanji_lst):
                if not origin in retry_lst:
                    retry_lst.append(origin)
                if not origin in todays_retry:
                    todays_retry.append(origin)

        if input_Y:
            break
    elif first_input == 'r':
        input_X = input()
        if input_X.lower() == 'x':
            break
        elif input_X.lower() in ['o','a','v','d','h','c','d','k','e','j','p']:
            retry_completed_lst.append(origins[rand_index])
            del origins[rand_index]
            del answers[rand_index]
        elif input_X.lower() == '2':
            retry_lst.remove(origin)
            retry_completed_lst.append(origins[rand_index])
            del origins[rand_index]
            del answers[rand_index]

    else:
        input_X = input()
        if input_X.lower() == 'x':
            break
        elif input_X == '2' or input_X.lower() in ['o','a','v','d','h','c','d','k','e','j','p']:
            del origins[rand_index]
            del answers[rand_index]
    print()

if not input_retry:
    func.update_lst2txt_combined(classified_lsts, classified_txts, origin_candidates)
    currtime_txt = os.path.join(save_folder, datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+".txt")
    with open(currtime_txt, 'wt', encoding='utf-8') as f:
        for word in completed_words_lst:
            for append_lst in append_lsts:
                if word in append_lst and word in origin_candidates:
                    f.write(word+"\n")
                    break
elif first_input == 'r':
    func.update_lst2txt(retry_lst, retry_txt, origin_candidates, mode=1)
    func.update_lst2txt(retry_completed_lst, retry_completed_txt, origin_candidates)

print()
func.seperation(['人','大'], hononyms_txt,[adverbs_txt, diff_kanjis_txt, etc_txt])

last_test = sorted(glob.glob(os.path.join(save_folder,"*.txt")))[-1]
func.print_word_duplicated_combined(classified_txts)

print(func.word_count_combined(append_txts), func.word_count(last_test))
print(func.properly_included(append_txts,last_test))

print(f"Classified words: {len(classified_words_lst)}")
print(f"Unlassified words: {len(probably_verb_lst) + len(probably_not_verb_lst)}")
