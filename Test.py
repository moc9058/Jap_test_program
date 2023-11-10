import os
import glob
from datetime import datetime
import time
import random
import signal
import openai
from multiprocessing import Process, Value, Array

import functions as func



one_to_one_mode = True
one_to_one_mode_extend_num = 5
pronounciation_mode = True
example_sentence_array = Array('i',200)
example_generating_pid = Value('i')
example_generating_server_access = Value('i')
def generate_example_sentence(word, example_sentence_array, pid_pointer, example_generating_server_access):
    pid_pointer.value = os.getpid()
    if word[0] == '（':
        word = word[word.find('）')+1:]
    try:
        response = openai.ChatCompletion.create(
            model = "gpt-4",
            messages=[
            {"role": "user", "content": f"Compose a Japanese sentence using \"{word}\" without any additional explanation."}
        ]
        )
        content = response['choices'][0]['message']['content']
        for i in range(min(len(content),len(example_sentence_array))):
            example_sentence_array[i] = ord(content[i])
    except Exception as e:
        example_generating_server_access.value = 0
        print()
        print("Cannot access openai server.")
        pass

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

    func.copy_txt2sorted_lst_combined(classified_lsts, classified_txts, origin_candidates)
    func.copy_txt2sorted_lst(retry_completed_lst, retry_completed_txt, origin_candidates)

    #################################アピールポイント１#################################
    # 単純にリストをイックステンドしてから整列するのより私の整列アルゴリズムの効率がもっと高い！
    classified_words_lst = []
    for append_lst in append_lsts:
        classified_words_lst.extend(append_lst)
    classified_words_lst.sort()
    # classified_words_lst = func.merge_sorted_lsts(append_lsts)
    # for i in range(len(classified_words_lst)-1):
    #     if not classified_words_lst[i] in origin_candidates:
    #         print(classified_words_lst[i])
    #     if classified_words_lst[i] >= classified_words_lst[i+1]:
    #         print("Something wrong with classified_words_lst!")
    #         print(f"{classified_words_lst[i]}, {classified_words_lst[i+1]}")
    # if not classified_words_lst[i] in origin_candidates:
    #     print(classified_words_lst[i])

    #################################アピールポイント２#################################
    # ただ各単語の分類有無を一々確認するより自分が考案したアルゴリズムが速やか！
    # unclassified_words_lst = []
    # for word in origin_candidates:
    #     if not word in classified_words_lst:
    #         unclassified_words_lst.append(word)
    # unclassified_words_lst.sort()

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
                if line in origin_candidates:
                    completed_words_lst.append(line)
                # completed_words_lst.append(line)

    for i in range(len(completed_words_lst)-1):
        if completed_words_lst[i] >= completed_words_lst[i+1]:
            print("Something wrong with completed_words_lst!")
            print(f"{completed_words_lst[i]}, {completed_words_lst[i+1]}")
    # Check and extract duplicated words of completed_words_lst in classified folder.
    # ex)諮る in words and compound
    # tmp_completed_words = completed_words_lst.copy()
    # tmp_duplicated_count = 0
    # while tmp_completed_words:
    #     tmp_word = tmp_completed_words.pop(0)
    #     tmp_count = 0
    #     tmp_first_txt = ""
    #     for tmp_append_lst in append_lsts:
    #         if tmp_word in tmp_append_lst:
    #             tmp_count += 1
    #             if tmp_count == 1:
    #                 tmp_first_txt = os.path.basename(append_txts[append_lsts.index(tmp_append_lst)])
    #             if tmp_count == 2:
    #                 tmp_duplicated_count += 1
    #                 print(f"{tmp_word}: {tmp_first_txt} {os.path.basename(append_txts[append_lsts.index(tmp_append_lst)])}", end=' ')
    #             if tmp_count > 2:
    #                 print(os.path.basename(append_txts[append_lsts.index(tmp_append_lst)]), end=' ')
        
    #     if tmp_count > 1:
    #         print()
    # if tmp_duplicated_count > 1:
    #     print(f"Total number of duplicated words is {tmp_duplicated_count}.")


    # Initiate program!
    # func.update_lst2sorted_txt(retry_lst, retry_txt, origin_candidates)
    print('Default is \"NO\" and applying 1:1 mode.')
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
    elif first_input[0].lower() == 'r':
        groups = [os.path.join('classified','retry.txt')]
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
            if first_input[i].lower() == 'x':
                func.update_lst2sorted_txt_combined(classified_lsts,classified_txts, origin_candidates)
                break
            elif first_input[i].lower() == 'v':
                groups.append(os.path.join('classified','verbs.txt'))
            elif first_input[i].lower() == 'k':
                groups.append(os.path.join('classified','katakanas.txt'))
            elif first_input[i].lower() == 'a':
                groups.append(os.path.join('classified','adverbs.txt'))
            elif first_input[i].lower() == 'd':
                groups.append(os.path.join('classified','diff_kanjis.txt'))
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
            
        # origins_1 = origin_candidates.copy()
        # answers_1 = answer_candidates.copy()
        # for i in range(len(completed_words_lst)):
        #     word = completed_words_lst[i]
        #     if word in origins_1:
        #         j = origins_1.index(word)
        #         del origins_1[j]
        #         del answers_1[j]
        # for i in range(len(origins)):
        #     print(f"{origins[i]}/-/{answers[i]}")
        
        # raise Exception("Hi")
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
    one_to_one_lst = unclassified_words_lst
    retry_banned_lst = []
    try:
        while origins:
            if len(one_to_one_lst) == 0:
                print("All words are classified!!")
                one_to_one_lst = []
                one_to_one_lst.extend(verb_lst)
                one_to_one_lst.extend(compound_lst)
                one_to_one_lst.extend(expression_lst)
                for one_to_one_word in retry_lst:
                    if not one_to_one_word in one_to_one_lst:
                        one_to_one_lst.append(one_to_one_word)
                one_to_one_lst.sort()
                for i in range(len(one_to_one_lst)-1):
                    if one_to_one_lst[i] == one_to_one_lst[i+1]:
                        print(f"Duplicated in one_to_one_lst: {one_to_one_lst[i]}")

            if not input_retry:
                if len(unclassified_words_lst) > 0:
                    print(f"(left: {len(origins)}, unclassified: {len(unclassified_words_lst)})", end=" ")
                else:
                    print(f"(left: {len(origins)})", end=" ")

            else:
                print(f"({len(origins)} left)", end=" ")
            rand_index = random.randrange(len(origins))
            origin = origins[rand_index].strip()
            answer = answers[rand_index].strip()
            is_katakana = func.is_katakana(origin)
            is_kanji = False
            classified_name = ""
            
            # verb, compound, expressions
            if one_to_one_mode and one_to_one_indicator % one_to_one_mode_extend_num in [4] and not input_retry:
                tmp_rand_index = random.randrange(len(one_to_one_lst))
                try:
                    rand_index = origins.index(one_to_one_lst[tmp_rand_index])
                    origin = origins[rand_index].strip()
                    answer = answers[rand_index].strip()
                except:
                    rand_index = -1
                    origin = one_to_one_lst[tmp_rand_index].strip()
                    answer = answer_candidates[origin_candidates.index(origin)].strip()
                is_katakana = func.is_katakana(origin)
            # adverbs
            elif one_to_one_mode and one_to_one_indicator % one_to_one_mode_extend_num == 2 and not input_retry:
                tmp_rand_index = random.randrange(len(adverb_lst))
                try:
                    rand_index = origins.index(adverb_lst[tmp_rand_index])
                    origin = origins[rand_index].strip()
                    answer = answers[rand_index].strip()
                except:
                    rand_index = -1
                    origin = adverb_lst[tmp_rand_index].strip()
                    answer = answer_candidates[origin_candidates.index(origin)].strip()
                is_katakana = func.is_katakana(origin)
            # grammers in adverbs
            elif one_to_one_mode and one_to_one_indicator % one_to_one_mode_extend_num in [1,3] and not input_retry:
                tmp_rand_index = 0
                for i in range(len(adverb_lst)):
                    # Grammar part
                    if adverb_lst[i][0] == '（' or adverb_lst[i][0] == '～':
                        tmp_rand_index = i
                        break
                tmp_rand_index = random.randrange(tmp_rand_index, len(adverb_lst))
                try:
                    rand_index = origins.index(adverb_lst[tmp_rand_index])
                    origin = origins[rand_index].strip()
                    answer = answers[rand_index].strip()
                except:
                    rand_index = -1
                    origin = adverb_lst[tmp_rand_index].strip()
                    answer = answer_candidates[origin_candidates.index(origin)].strip()
                is_katakana = func.is_katakana(origin)
            one_to_one_indicator = (one_to_one_indicator+1) % one_to_one_mode_extend_num

            classified_lst = []
            if origin in adverb_lst:
                classified_lst = adverb_lst
                classified_name = '(adverb.txt)'
            elif origin in diff_kanji_lst:
                classified_lst = diff_kanji_lst
                classified_name = '(diff_kanjis.txt)'
                is_kanji = True
            elif origin in etc_lst:
                classified_lst = etc_lst
                classified_name = '(etc.txt)'
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
            case_for_GPT = classified_name in ['(compounds.txt)', '(verbs.txt)', '(adverb.txt)', '(adjectives.txt)']
            
            # case_for_GPT = True

            if case_for_GPT:
                for i in range(len(example_sentence_array)):
                    example_sentence_array[i] = 0
                example_generating_server_access.value = 1
                process = Process(target=generate_example_sentence, args=(origin_to_print, example_sentence_array, example_generating_pid, example_generating_server_access))
                try:
                    if example_generating_server_access.value == 1:
                        process.start()
                except Exception as e:
                    print(e)
                
            if is_katakana:
                print(f"{origin_to_print}{try_again}", end=" ")
                input_X = input()
                print(f"（正解）\n{answer} {classified_name}{answer_hononyms}")
            elif pronounciation_mode:
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
                while GPT_time_count < 6:
                    if example_generating_server_access.value == 0:
                        break
                        time.sleep(0.5)
                    GPT_time_count += 1
                    if example_sentence_array[0]:
                        GPT_time_count = 6

                try:
                    os.kill(example_generating_pid.value, signal.SIGTERM)
                except Exception as e:
                    pass

                # the value of example_generating_server_access can be changed
                if example_generating_server_access.value == 1:
                    if example_sentence_array[0] > 0:
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
                save2completed_words_lst = True
                # retry_lst and classified
                if try_again != "" and classified_name != "":
                    print("retry and classified")
                    # At first, it gets removed from retry_lst. If you want to keep it in retry_lst, just press enter or 'r'.
                    try:
                        retry_lst.remove(origin)
                    except Exception as e:
                        print(e)
                    retry_banned_lst.append(origin)
                    print(retry_banned_lst)
                    save2completed_words_lst = False
                if input_X.lower() == 'n' and input_Y.lower() in ['v','a','d','k','c','e','j','p','2','o']:
                    save2completed_words_lst = False
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

                    if rand_index != -1 and save2completed_words_lst:
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

                    if rand_index != -1 and save2completed_words_lst:
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

                    if rand_index != -1 and save2completed_words_lst:
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
                        try:
                            unclassified_words_lst.remove(origin)
                        except:
                            pass
                        if not origin in classified_words_lst:
                            classified_words_lst.append(origin)

                    if rand_index != -1 and save2completed_words_lst:
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

                    if rand_index != -1 and save2completed_words_lst:
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

                    if rand_index != -1 and save2completed_words_lst:
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

                    if rand_index != -1 and save2completed_words_lst:
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

                    if rand_index != -1 and save2completed_words_lst:
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
                        try:
                            unclassified_words_lst.remove(origin)
                        except:
                            pass
                        if not origin in classified_words_lst:
                            classified_words_lst.append(origin)

                    if rand_index != -1 and save2completed_words_lst:
                        completed_words_lst.append(origin)
                        del origins[rand_index]
                        del answers[rand_index]
                elif not (input_X.lower() == 'n' or input_X.lower() == 'r'):
                    if not (origin in pure_kanji_lst or origin in diff_kanji_lst):
                        retry_lst.append(origin)
                        try:
                            retry_banned_lst.remove(origin)
                        except:
                            pass

                elif input_X.lower() == 'r':
                    retry_lst.append(origin)
                    try:
                        retry_banned_lst.remove(origin)
                    except:
                        pass

                if input_X:
                    if input_X == input_Y:
                        break
            elif first_input == 'r':
                input_X = input()
                if input_X.lower() == 'x':
                    break
                elif input_X.lower() in ['o','a','v','d','c','d','k','e','j','p']:
                    retry_completed_lst.append(origins[rand_index])
                    del origins[rand_index]
                    del answers[rand_index]
                elif input_X.lower() == '2':
                    retry_lst.remove(origin)
                    retry_completed_lst.append(origins[rand_index])
                    try:
                        completed_words_lst.remove(origin)
                    except:
                        pass
                    del origins[rand_index]
                    del answers[rand_index]

            else:
                input_X = input()
                if input_X.lower() == 'x':
                    break
                elif input_X == '2' or input_X.lower() in ['o','a','v','d','c','d','k','e','j','p']:
                    del origins[rand_index]
                    del answers[rand_index]
            print()
    except Exception as e:
        print(e)
    except KeyboardInterrupt as keyboard_interrupt:
        print(keyboard_interrupt)

    if not input_retry:
        func.update_lst2sorted_txt_combined(append_lsts, append_txts, origin_candidates)
        func.update_lst2sorted_txt(retry_lst, retry_txt, origin_candidates, banned_lst=retry_banned_lst)
        currtime_txt = os.path.join(save_folder, datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+".txt")
        completed_words_lst.sort()
        with open(currtime_txt, 'wt', encoding='utf-8') as f:
            for word in completed_words_lst:
                f.write(word+"\n")
    elif first_input == 'r':
        func.update_lst2sorted_txt(completed_words_lst, last_test, origin_candidates, mode=1)
        func.update_lst2sorted_txt(retry_lst, retry_txt, origin_candidates, mode=1)
        func.update_lst2sorted_txt(retry_completed_lst, retry_completed_txt, retry_lst)

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

        

    print()

    print(f"Classified words: {len(classified_words_lst)}")
    print(f"Unlassified words: {len(unclassified_words_lst)}")
    print(f"Total: {len(classified_words_lst) + len(unclassified_words_lst)}")