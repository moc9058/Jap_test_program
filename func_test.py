import os
import time
import functions as func

cwd = os.path.join(os.getcwd())
save_folder = os.path.join(cwd,'test_log')
if not os.path.exists(save_folder):
    os.mkdir(save_folder)

# Group 1.txt is always sorted.
group_1_txt = os.path.join(cwd,'Group 1.txt')
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

func.copy_txt2sorted_lst_combined(classified_lsts, classified_txts, origin_candidates)
func.copy_txt2sorted_lst(retry_completed_lst, retry_completed_txt, origin_candidates)


# easy verbs
easy_txt = os.path.join(cwd,'easy.txt')
easy_lst = []
func.copy_txt2sorted_lst(easy_lst, easy_txt, origin_candidates)

with open(os.path.join('C:\\','Users','moc90','OneDrive','바탕 화면','quizlet.txt'), 'w', encoding='utf-8') as f:
    for i in range(len(origin_candidates)):
        word = origin_candidates[i]
        answer = answer_candidates[i]
        if word in easy_lst:
            continue
        elif word in verb_lst:
            f.write(f'{word}/-/{answer}\n')

    
# print(ord('ぁ'))
# for i in range(0,86):
#     print(chr(12353+i))
# print(ord('ァ'))
# for i in range(0,92):
#     print(chr(12449+i))


