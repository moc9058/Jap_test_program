import os
import glob
from datetime import datetime
import time
import random
import signal
from openai import OpenAI
from multiprocessing import Process, Value, Array

import functions as func

API_your_key = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

GPT_OK = False

default_num_secs = 2
one_to_one_mode = True
one_to_one_mode_extend_num = 100
pronounciation_mode = False
example_sentence_array = Array('i',200)
example_generating_pid = Value('i')
example_generating_server_access = Value('i')

def generate_example_sentence(word, pronounciation, example_sentence_array, pid_pointer, example_generating_server_access, num_sentences):
    try:
        pid_pointer.value = os.getpid()
        grammer_components = []
        grammer_component = ""
        honorific = ""
        require_additional_sentence = False
        if word[0] == '（':
            require_additional_sentence = True
            if word[1] in ['お','ご']:
                honorific = ['お','ご'][random.randrange(2)]
                word = word[word.find('）')+1:]
            grammer_components = word[1:word.find('）')].split('、')
            for i in range(len(grammer_components)):
                grammer_component = grammer_components[i]
                if grammer_component == 'る':
                    grammer_component = '辞書形'
                elif grammer_component == 'よう':
                    grammer_component = '意志形'
                elif grammer_component == 'い':
                    grammer_component = 'い形容詞'
                elif grammer_component == 'な':
                    grammer_component = 'な形容詞'
                elif grammer_component == 'の':
                    grammer_component = '名詞＋の'
                else:
                    grammer_component = grammer_component + '形の語幹'
                grammer_components[i] = grammer_component
            grammer_component = grammer_components[random.randrange(len(grammer_components))]
            word = word[word.index('）')+1:]
            # （よう）が（る、ない）まいが
            if word.find('（') != -1:
                word = word[:word.find('（')] + '～' + word[word.find('）')+1:]

            if honorific != "":
                word = honorific + '＋' + grammer_component + '＋' + word
            else:
                word = grammer_component + '＋' + word
        else:
            word = f"{word}（{pronounciation}）"
        GPT_input_sentences = [{"role": "user", "content": f"「{word}」の例文を挙げてもらえるかな？{num_sentences}文以内にお願いね！"}]
        if require_additional_sentence:
            GPT_input_sentences.append({"role": "user", "content": f'文法要素の（{grammer_component}を必ず含めてください。）'})
        client = API_your_key
        completion = client.chat.completions.create(
            messages=GPT_input_sentences,
            model="gpt-4"
        )
        content = completion.choices[0].message.content
        for i in range(min(len(content),len(example_sentence_array))):
            example_sentence_array[i] = ord(content[i])
    except Exception as e:
        # print(e)
        example_generating_server_access.value = 0

        

# Assume groups, classified units are always sorted
# Assume retry_txt is not sorted
# Assume origins_candidates is sorted
if __name__ == '__main__':
    cwd = os.path.join(os.getcwd())
    save_folder = os.path.join(cwd,'test_log')
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)

    # Group 1.txt is always sorted.
    group_1_txt = os.path.join(cwd,'Group 1.txt')
    # func.txt_sort(group_1_txt)
    # Group 2.txt always needs to be sorted.
    group_2_txt = os.path.join(cwd,'Group 2.txt')
    func.txt_sort(group_2_txt)

    # Extract origins, answers
    group_txt_lst = ['Group 1.txt', 'Group 2.txt']
    origin_candidates = []
    answer_candidates = []

    group_1_finished = False
    group_2_finished = False
    with open(os.path.join(cwd,group_txt_lst[0]), 'r', encoding='utf-8') as f1:
        with open(os.path.join(cwd,group_txt_lst[1]), 'r', encoding='utf-8') as f2:
            line_1 = f1.readline()
            if not line_1:
                group_1_finished = True
            line_2 = f2.readline()
            if not line_2:
                group_2_finished = True
            while not (group_1_finished or group_2_finished):
                if line_1 < line_2:
                    line_1_splitted = line_1.split('/-/')
                    if len(line_1_splitted) >= 2:
                        origin_candidates.append(line_1_splitted[0].strip())
                        answer_candidates.append(line_1_splitted[1].strip())
                    else:
                        print(f"Format error in Group 1.txt: {line_1}")
                    line_1 = f1.readline()
                    if not line_1:
                        group_1_finished = True
                else:
                    line_2_splitted = line_2.split('/-/')
                    if len(line_2_splitted) >= 2:
                        origin_candidates.append(line_2_splitted[0].strip())
                        answer_candidates.append(line_2_splitted[1].strip())
                    else:
                        print(f"Format error in Group 2.txt: {line_2}")
                    line_2 = f2.readline()
                    if not line_2:
                        group_2_finished = True

            if group_1_finished and group_2_finished:
                pass
            elif group_1_finished and not group_2_finished:
                line_2_splitted = line_2.split('/-/')
                if len(line_2_splitted) >= 2:
                    origin_candidates.append(line_2_splitted[0].strip())
                    answer_candidates.append(line_2_splitted[1].strip())
                else:
                    print(f"Format error in Group 1.txt: {line_2}")
                while line_2:
                    line_2 = f2.readline()
                    if not line_2: break
                    line_2_splitted = line_2.split('/-/')
                    if len(line_2_splitted) >= 2:
                        origin_candidates.append(line_2_splitted[0].strip())
                        answer_candidates.append(line_2_splitted[1].strip())
                    else:
                        print(f"Format error in Group 2.txt: {line_2}")
            elif not group_1_finished and group_2_finished:
                line_1_splitted = line_1.split('/-/')
                if len(line_1_splitted) >= 2:
                    origin_candidates.append(line_1_splitted[0].strip())
                    answer_candidates.append(line_1_splitted[1].strip())
                else:
                    print(f"Format error in Group 1.txt: {line_1}")
                while line_1:
                    line_1 = f1.readline()
                    if not line_1: break
                    line_1_splitted = line_1.split('/-/')
                    if len(line_1_splitted) >= 2:
                        origin_candidates.append(line_1_splitted[0].strip())
                        answer_candidates.append(line_1_splitted[1].strip())
                    else:
                        print(f"Format error in Group 1.txt: {line_1}")
    for i in range(len(origin_candidates)-1):
        if origin_candidates[i] >= origin_candidates[i+1]:
            print("Something wrong with origin_candidates!")
            print(f"{origin_candidates[i]}, {origin_candidates[i+1]}")


    retry_completed_txt = os.path.join(cwd,'retry_completed_txt.txt')
    retry_completed_lst = []

    retry_txt = os.path.join(cwd,'retry.txt')
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

    classified_txts = [retry_txt, verbs_txt, adverbs_txt, diff_kanjis_txt, katakanas_txt,\
                    compounds_txt, expressions_txt, adjectives_txt, pure_kanjis_txt,\
                    etc_txt]
    classified_lsts = [retry_lst, verb_lst, adverb_lst, diff_kanji_lst, katakana_lst,\
                    compound_lst, expression_lst, adjective_lst, pure_kanji_lst,\
                    etc_lst]
    append_txts = [verbs_txt, adverbs_txt, diff_kanjis_txt, katakanas_txt,\
                compounds_txt, expressions_txt, adjectives_txt, pure_kanjis_txt,\
                etc_txt]
    append_lsts = [verb_lst, adverb_lst, diff_kanji_lst, katakana_lst,\
                compound_lst, expression_lst, adjective_lst, pure_kanji_lst,\
                etc_lst]

    func.create_txt_combined(classified_txts)
    func.create_txt(retry_completed_txt)

    func.copy_txt2sorted_lst_combined(append_lsts, append_txts, origin_candidates)
    func.copy_txt2sorted_lst(retry_lst, retry_txt, origin_candidates, delete_dup=1)
    func.copy_txt2sorted_lst(retry_completed_lst, retry_completed_txt, origin_candidates)
    

    #################################アピールポイント１#################################
    # 単純にリストをイックステンドしてから整列するのより私の整列アルゴリズムの効率がもっと高い！
    classified_words_lst = []
    for append_lst in append_lsts:
        classified_words_lst.extend(append_lst)
    classified_words_lst.sort()
    
    for i in range(len(classified_words_lst)-1):
        if classified_words_lst[i] >= classified_words_lst[i+1]:
            print(classified_words_lst[i], classified_words_lst[i+1])

    
    unclassified_words_lst = []
    i = j = 0
    while j < len(classified_words_lst):
        while origin_candidates[i] == classified_words_lst[j]:
            i += 1
            j += 1
            if j >= len(classified_words_lst):
                break
        if j >= len(classified_words_lst):
            break
        while origin_candidates[i] < classified_words_lst[j]:
            unclassified_words_lst.append(origin_candidates[i])
            i += 1
    while i < len(classified_words_lst):
        unclassified_words_lst.append(origin_candidates[i])
        i += 1

    for i in range(len(unclassified_words_lst)-1):
        if unclassified_words_lst[i] >= unclassified_words_lst[i+1]:
            print("Something wrong with unclassified_words_lst!")
            print(f"{unclassified_words_lst[i]}, {unclassified_words_lst[i+1]}")


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
                if line in origin_candidates and not line in completed_words_lst:
                    completed_words_lst.append(line)
                # completed_words_lst.append(line)

    for i in range(len(completed_words_lst)-1):
        if completed_words_lst[i] >= completed_words_lst[i+1]:
            print("Something wrong with completed_words_lst!")
            print(f"{completed_words_lst[i]}, {completed_words_lst[i+1]}")
    

    # Initiate program!
    print('Default is \"NO\" and applying 1:1 mode. If you press T, GPT generates examples.')
    print('(Classified Mode)')
    print('A: adverbs.txt')
    print('C: compounds.txt')
    print('D: diff_kanjis.txt')
    print('E: expressions.txt')
    print('J: adjectives.txt')
    print('K: katakanas.txt')
    print('P: pure_kanjis.txt')
    print('V: verbs.txt')
    print('(Retry Mode)')
    print('R: retry.txt')
    first_input = input()
    input_retry = True
    groups = []
    if len(first_input) == 0:
        input_retry = False 
        groups = group_txt_lst
        one_to_one_mode = True
        GPT_OK = False
    elif first_input in ['t','T','ｔ']:
        first_input = ""
        input_retry = False 
        groups = group_txt_lst
        one_to_one_mode = True
        GPT_OK = True
    elif first_input[0] in ['r','R','ｒ']:
        groups = [os.path.join('retry.txt')]
        first_input = 'r'
    else:
        first_input_alphabets = []
        for i in range(len(first_input)):
            if not first_input[i] in first_input_alphabets:
                first_input_alphabets.append(first_input[i])
        first_input = ""
        for i in range(len(first_input_alphabets)):
            first_input = first_input + first_input_alphabets[i]
        
        for i in range(len(first_input)):
            if first_input[i] in ['x','X','ｘ']:
                func.update_lst2sorted_txt_combined(classified_lsts,classified_txts, origin_candidates)
                break
            elif first_input[i]  in ['v','V','ｖ']:
                groups.append(os.path.join('classified','verbs.txt'))
            elif first_input[i] in ['k','K','ｋ']:
                groups.append(os.path.join('classified','katakanas.txt'))
            elif first_input[i] in ['a','A','あ']:
                groups.append(os.path.join('classified','adverbs.txt'))
            elif first_input[i] in ['d','D','ｄ']:
                groups.append(os.path.join('classified','diff_kanjis.txt'))
            elif first_input[i] in ['c','C','ｃ']:
                groups.append(os.path.join('classified','compounds.txt'))
            elif first_input[i] in ['e','E','え']:
                groups.append(os.path.join('classified','expressions.txt'))
            elif first_input[i] in ['j','J','ｊ']:
                groups.append(os.path.join('classified','adjectives.txt'))
            elif first_input[i] in ['p','P','ｐ']:
                groups.append(os.path.join('classified','pure_kanjis.txt'))
    print()
        
    
    origins = []
    answers = []
    if not input_retry:
        origins = []
        answers = []
        i = j = 0
        while j < len(completed_words_lst):
            while origin_candidates[i] == completed_words_lst[j]:
                i += 1
                j += 1
                if j >= len(completed_words_lst):
                    break
            if j >= len(completed_words_lst):
                    break
            while origin_candidates[i] < completed_words_lst[j]:
                origins.append(origin_candidates[i])
                answers.append(answer_candidates[i])
                i += 1
        while i < len(origin_candidates):
            origins.append(origin_candidates[i])
            answers.append(answer_candidates[i])
            i += 1
        for i in range(len(origins)-1):
            if origins[i] >= origins[i+1]:
                print("Something wrong with origins!")
                print(f"{origins[i]}, {origins[i+1]}")
            
        
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
        
    # easy verbs
    easy_txt = os.path.join(cwd,'easy.txt')
    easy_lst = []
    func.copy_txt2sorted_lst(easy_lst, easy_txt, origin_candidates)

    easy_verb_lst = []
    easy_compound_lst = []
    easy_etc_lst = []
    for easy_word in easy_lst:
        try:
            origin.remove(easy_word)
        except:
            pass

        if easy_word in verb_lst:
            easy_verb_lst.append(easy_word)
            verb_lst.remove(easy_word)
        elif easy_word in compound_lst:
            easy_compound_lst.append(easy_word)
            compound_lst.remove(easy_word)
        elif easy_word in etc_lst:
            easy_etc_lst.append(easy_word)
            etc_lst.remove(easy_word)
    
    one_to_one_lst = []
    if not first_input and len(unclassified_words_lst) > 0:
        one_to_one_lst = unclassified_words_lst
    else:
        if not first_input and len(unclassified_words_lst) == 0:
            print("All words are classified!!")
        one_to_one_lst = []
        one_to_one_lst.extend(compound_lst)
        one_to_one_lst.extend(expression_lst)
        one_to_one_lst.sort()
        for i in range(len(one_to_one_lst)-1):
            if one_to_one_lst[i] == one_to_one_lst[i+1]:
                print(f"Duplicated in one_to_one_lst: {one_to_one_lst[i]}")
        
    
    retry_banned_lst = []
    try:
        while origins:
            # print(len(one_to_one_lst))
            num_secs = default_num_secs
            num_sentences = 1
            one_to_one_indicator = random.randrange(one_to_one_mode_extend_num)
            
            pronounciation_mode = False
            if not input_retry:
                if len(unclassified_words_lst) > 0:
                    print(f"(left: {len(origins)}, unclassified: {len(unclassified_words_lst)})", end=" ")
                else:
                    if len(one_to_one_lst) == 0:
                        print("All words are classified!!")
                        one_to_one_lst = []
                        one_to_one_lst.extend(compound_lst)
                        one_to_one_lst.extend(expression_lst)
                        one_to_one_lst.sort()
                        for i in range(len(one_to_one_lst)-1):
                            if one_to_one_lst[i] == one_to_one_lst[i+1]:
                                print(f"Duplicated in one_to_one_lst: {one_to_one_lst[i]}")
                    print(f"(left: {len(origins)})", end=" ")

            else:
                print(f"({len(origins)} left)", end=" ")
            

            if not first_input and one_to_one_mode:
                if len(unclassified_words_lst) > 0:
                    # unclassified : 50%
                    if one_to_one_indicator < 50:
                        tmp_rand_index = random.randrange(len(one_to_one_lst))
                        try:
                            rand_index = origins.index(one_to_one_lst[tmp_rand_index])
                            origin = origins[rand_index].strip()
                            answer = answers[rand_index].strip()
                        except:
                            rand_index = -1
                            origin = one_to_one_lst[tmp_rand_index].strip()
                            answer = answer_candidates[origin_candidates.index(origin)].strip()
                    # retry : 50%
                    else:
                        tmp_rand_index = random.randrange(len(retry_lst))
                        try:
                            rand_index = origins.index(retry_lst[tmp_rand_index])
                            origin = origins[rand_index].strip()
                            answer = answers[rand_index].strip()
                        except:
                            rand_index = -1
                            origin = retry_lst[tmp_rand_index].strip()
                            answer = answer_candidates[origin_candidates.index(origin)].strip()
                else:
                    # compound, expression : 20%
                    if one_to_one_indicator < 20:
                        tmp_rand_index = random.randrange(len(one_to_one_lst))
                        try:
                            rand_index = origins.index(one_to_one_lst[tmp_rand_index])
                            origin = origins[rand_index].strip()
                            answer = answers[rand_index].strip()
                        except:
                            rand_index = -1
                            origin = one_to_one_lst[tmp_rand_index].strip()
                            answer = answer_candidates[origin_candidates.index(origin)].strip()
                    # verb : 60%
                    elif one_to_one_indicator < 80:
                        tmp_rand_index = random.randrange(len(verb_lst))
                        try:
                            rand_index = origins.index(verb_lst[tmp_rand_index])
                            origin = origins[rand_index].strip()
                            answer = answers[rand_index].strip()
                        except:
                            rand_index = -1
                            origin = verb_lst[tmp_rand_index].strip()
                            answer = answer_candidates[origin_candidates.index(origin)].strip()
                    # retry : 10%
                    elif one_to_one_indicator < 90:
                        tmp_rand_index = random.randrange(len(retry_lst))
                        try:
                            rand_index = origins.index(retry_lst[tmp_rand_index])
                            origin = origins[rand_index].strip()
                            answer = answers[rand_index].strip()
                        except:
                            rand_index = -1
                            origin = retry_lst[tmp_rand_index].strip()
                            answer = answer_candidates[origin_candidates.index(origin)].strip()
                    else:
                        tmp_rand_index = random.randrange(len(origin_candidates))
                        try:
                            rand_index = origins.index(origin_candidates[tmp_rand_index])
                            origin = origins[rand_index].strip()
                            answer = answers[rand_index].strip()
                        except:
                            rand_index = -1
                            origin = origin_candidates[tmp_rand_index].strip()
                            answer = answer_candidates[origin_candidates.index(origin)].strip()
            else:
                rand_index = random.randrange(len(origins))
                origin = origins[rand_index].strip()
                answer = answers[rand_index].strip()
            

            is_katakana = func.is_katakana(origin)

            is_kanji = False
            classified_name = ""
            classified_lst = []
            case_for_GPT = False
            if origin in adverb_lst:
                classified_lst = adverb_lst
                classified_name = '(adverb.txt)'
                pronounciation_mode = True
                num_sentences = 2
                num_secs = 3
                case_for_GPT = True
            elif origin in diff_kanji_lst:
                classified_lst = diff_kanji_lst
                classified_name = '(diff_kanjis.txt)'
                is_kanji = True
            elif origin in etc_lst:
                classified_lst = etc_lst
                classified_name = '(etc.txt)'
                case_for_GPT = True
            elif origin in katakana_lst:
                classified_lst = katakana_lst
                classified_name = '(katakanas.txt)'
            elif origin in compound_lst:
                classified_lst = compound_lst
                classified_name = '(compounds.txt)'
                num_sentences = 2
                num_secs = 3
                case_for_GPT = True
            elif origin in expression_lst:
                classified_lst = expression_lst
                classified_name = '(expressions.txt)'
                case_for_GPT = True
            elif origin in adjective_lst:
                classified_lst = adjective_lst
                classified_name = '(adjectives.txt)'
                pronounciation_mode = True
                case_for_GPT = True
            elif origin in pure_kanji_lst:
                classified_lst = pure_kanji_lst
                classified_name = '(pure_kanjis.txt)'
                is_kanji = True
            elif origin in verb_lst:
                classified_lst = verb_lst
                classified_name = '(verbs.txt)'
                pronounciation_mode = True
                num_sentences = 2
                num_secs = 3
                case_for_GPT = True
            
            if origin in easy_lst:
                case_for_GPT = False
            
            if not GPT_OK:
                case_for_GPT = False
            
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

            
            if func.contains_kanji(origin):
                pronounciation = answer.split()[0].strip()
            else:
                pronounciation = origin


            # hononyms
            answer_hononyms = ""
            origin_count = 0
            if is_kanji or (origin in unclassified_words_lst and func.is_kanji_word(origin)):
                for i in range(len(origin_candidates)):
                    tmp_origin = origin_candidates[i]
                    tmp_answer = answer_candidates[i]
                    tmp_is_completed = ""
                    if tmp_origin != origin and tmp_answer.split()[0].strip() == pronounciation:
                        if tmp_origin in completed_words_lst:
                            tmp_is_completed = "(completed)"
                        if func.is_kanji_word(tmp_origin):
                            origin_count += 1
                            if origin_count == 1:
                                answer_hononyms = f"\n（同音異義語）\n{tmp_origin} {tmp_answer[tmp_answer.find(' ')+1:].strip()}{tmp_is_completed}"
                            else:
                                answer_hononyms = f"{answer_hononyms}\n{tmp_origin} {tmp_answer[tmp_answer.find(' ')+1:].strip()}{tmp_is_completed}"
            else:
                for i in range(len(origin_candidates)):
                    tmp_origin = origin_candidates[i]
                    tmp_answer = answer_candidates[i]
                    tmp_is_completed = ""
                    if tmp_origin != origin and tmp_answer.split()[0].strip() == pronounciation:
                        if tmp_origin in completed_words_lst:
                            tmp_is_completed = "(completed)"
                        # if tmp_origin in classified_lst:
                        origin_count += 1
                        if origin_count == 1:
                            answer_hononyms = f"\n（同音異義語）\n{tmp_origin} {tmp_answer[tmp_answer.find(' ')+1:].strip()}{tmp_is_completed}"
                        else:
                            answer_hononyms = f"{answer_hononyms}\n{tmp_origin} {tmp_answer[tmp_answer.find(' ')+1:].strip()}{tmp_is_completed}"

            # Multiprocessing begins
            # case_for_GPT = classified_name in ['(compounds.txt)', '(verbs.txt)', '(adverb.txt)', '(adjectives.txt)']
            # case_for_GPT = not classified_name in ['(diff_kanjis.txt)', '(pure_kanjis.txt)']
            

            if case_for_GPT:
                for i in range(len(example_sentence_array)):
                    example_sentence_array[i] = 0
                example_generating_server_access.value = 1
                process = Process(target=generate_example_sentence, args=(origin_to_print, pronounciation, example_sentence_array, example_generating_pid, example_generating_server_access, num_sentences))
                # print(f'{pronounciation}（{origin_to_print}）')
                try:
                    process.start()
                except Exception as e:
                    print('error in multiprocessing')
                    print(e)
                
            if is_katakana:
                print(f"{origin_to_print}{try_again}", end=" ")
                input_X = input()
                print(f"（正解）\n{answer} {classified_name}{answer_hononyms}")
            elif pronounciation_mode and not is_kanji:
                if func.contains_kanji(origin):
                    ans_split_index = answer.find(" ")
                    print(f"{answer[:ans_split_index].strip()}{try_again}", end=" ")
                    input_X = input()
                    print(f"（正解）\n{origin_to_print} {answer[ans_split_index:].strip()} {classified_name}{answer_hononyms}")
                else:
                    print(f"{origin_to_print}{try_again}", end=" ")
                    input_X = input()
                    print(f"（正解）\n{answer} {classified_name}{answer_hononyms}")
            else:
                print(f"{origin_to_print}{try_again}", end=" ")
                input_X = input()
                print(f"（正解）\n{answer} {classified_name}{answer_hononyms}")
            
            #################################アピールポイント３#################################
            # Wait for at most 3~4 seconds.
            if case_for_GPT:
                GPT_time_count = 0
                while GPT_time_count < 2*num_secs:
                    if example_generating_server_access.value == 0:
                        break
                    # print('sleep 0.5sec')
                    time.sleep(0.5)
                    GPT_time_count += 1
                    if example_sentence_array[0]:
                        GPT_time_count = 6

                try:
                    # print('I killed child process')
                    os.kill(example_generating_pid.value, signal.SIGTERM)
                except Exception as e:
                    pass
                
                # print("Would you guess the result?")
                # the value of example_generating_server_access can be changed
                if example_generating_server_access.value == 1 and example_sentence_array[0] > 0:
                    example_sentence = ""
                    for i in range(len(example_sentence_array)):
                        example_sentence += chr(example_sentence_array[i])
                    print(f"（例文）\n{example_sentence}")
                else:
                    print("（例文）\nThere\'s a problem with GPT connection.")

            try:
                process.join()
            except Exception as e:
                # print(e)
                pass

            # try:
            #     os.kill(example_generating_pid.value, signal.SIGTERM)
            # except Exception as e:
            #     print(e)
            
            if len(input_X) > 1:
                input_X = input_X[0]
            if input_X in ['x','X','ｘ']:
                print()
                break
            time.sleep(0.5)
            if not input_retry:
                input_X = input()
                input_Y = ""
                if len(input_X) > 1:
                    input_Y = input_X[1]
                    input_X = input_X[0]
                if input_X in ['x','X','ｘ']:
                    break
                save2completed_words_lst = True
                save2retry_lst = False
                
                if try_again != "" and classified_name != "":
                    retry_banned_lst.append(origin)
                    save2completed_words_lst = False
                    save2retry_lst = True


                if input_X.lower() == 'n':
                    save2completed_words_lst = False
                    save2retry_lst = False
                    if input_Y.lower() in ['v','a','d','k','c','e','j','p','2','o']:
                        input_X = input_Y.lower()
                        input_Y = ""
                elif input_X.lower() == 'r':
                    save2retry_lst = True
                    if input_Y.lower() in ['v','a','d','k','c','e','j','p','2','o']:
                        input_X = input_Y.lower()
                        input_Y = ""
                

                if input_X.lower() == 'v':
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


                if (input_X.lower() in ['v','a','d','k','c','e','j','p','2','o'] or try_again == "") and len(classified_lst) > 0:
                    if rand_index != -1 and save2completed_words_lst:
                        completed_words_lst.append(origin)
                        del origins[rand_index]
                        del answers[rand_index]

                if save2retry_lst:
                    if not origin in retry_lst:
                        retry_lst.append(origin)
                    try:
                        retry_banned_lst.remove(origin)
                    except:
                        pass
                
                if input_X:
                    if input_X.lower() == input_Y.lower():
                        break
            elif first_input == 'r':
                input_X = input()
                if input_X.lower() in ['x','ｘ']:
                    break
                elif input_X.lower() in ['o','a','v','d','c','d','k','e','j','p'] and rand_index != -1:
                    retry_completed_lst.append(origin)
                    del origins[rand_index]
                    del answers[rand_index]
                elif input_X.lower() in ['2','２'] and rand_index != -1:
                    retry_lst.remove(origin)
                    retry_completed_lst.append(origin)
                    try:
                        completed_words_lst.remove(origin)
                    except:
                        pass
                    del origins[rand_index]
                    del answers[rand_index]

            else:
                input_X = input()
                if input_X in ['x','X','ｘ']:
                    break
                elif input_X.lower() in ['2','２'] or input_X.lower() in ['o','a','v','d','c','d','k','e','j','p']:
                    del origins[rand_index]
                    del answers[rand_index]
            print()
    except KeyboardInterrupt as keyboard_interrupt:
        print(keyboard_interrupt)
    except Exception as e:
        print(e)

    for easy_word in easy_verb_lst:
        if not easy_word in verb_lst:
            verb_lst.append(easy_word)
    for easy_word in easy_compound_lst:    
        if not easy_word in compound_lst:
            compound_lst.append(easy_word)
    for easy_word in easy_etc_lst:
        if not easy_word in etc_lst:
            etc_lst.append(easy_word)

    if not input_retry:
        func.update_lst2sorted_txt_combined(append_lsts, append_txts, origin_candidates)
        func.update_lst2sorted_txt(retry_lst, retry_txt, origin_candidates, get_mode=1, banned_lst=retry_banned_lst)
        currtime_txt = os.path.join(save_folder, datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+".txt")
        completed_words_lst.sort()
        with open(currtime_txt, 'wt', encoding='utf-8') as f:
            for word in completed_words_lst:
                f.write(word+"\n")
        # アピールポイント４
        # Update Group 1.txt, Group 2.txt
        classified_words_lst.sort()
        with open(group_1_txt, 'w', encoding='utf-8') as f1:
            with open(group_2_txt, 'w', encoding='utf-8') as f2:
                i = j = 0
                while j < len(classified_words_lst):
                    while origin_candidates[i] == classified_words_lst[j]:
                        f1.write(f"{origin_candidates[i]}/-/{answer_candidates[i]}\n")
                        i += 1
                        j += 1
                        if j >= len(classified_words_lst):
                            break
                    if j >= len(classified_words_lst):
                            break
                    while origin_candidates[i] < classified_words_lst[j]:
                        f2.write(f"{origin_candidates[i]}/-/{answer_candidates[i]}\n")
                        i += 1
                while i < len(origin_candidates):
                    f1.write(f"{origin_candidates[i]}/-/{answer_candidates[j]}\n")
                    i += 1
    elif first_input == 'r':
        func.update_lst2sorted_txt(completed_words_lst, last_test, origin_candidates)
        func.update_lst2sorted_txt(retry_lst, retry_txt, origin_candidates, get_mode=1)
        func.update_lst2sorted_txt(retry_completed_lst, retry_completed_txt, retry_lst, get_mode=1)

    func.update_lst2sorted_txt(easy_lst, easy_txt, origin_candidates, get_mode=1)

        

    print()

    print(f"Classified words: {len(classified_words_lst)}")
    print(f"Unlassified words: {len(unclassified_words_lst)}")
    print(f"Total: {len(classified_words_lst) + len(unclassified_words_lst)}")