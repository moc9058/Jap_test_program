import os
import glob
import functions as func

cwd = os.path.join(os.getcwd())
save_folder = os.path.join(cwd,'test_log')

group_txt_lst = ['Group 1.txt', 'Group 2.txt', 'Group 3.txt']
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

origin_candidates = []
answer_candidates = []
for answer_group in group_txt_lst:
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



retry_completed_txt = os.path.join(cwd,'retry_completed_txt.txt')
retry_completed_lst = []

func.copy_txt2sorted_lst_combined(classified_lsts, classified_txts, origin_candidates)
func.copy_txt2sorted_lst(retry_completed_lst, retry_completed_txt, origin_candidates)


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
for i in range(len(completed_words_lst)):
    if not completed_words_lst[i] in origin_candidates:
        print(completed_words_lst[i])
# completed_words_lst.sort()
# with open(last_test, 'w', encoding='utf-8') as f:
#     while completed_words_lst:
#         f.write(completed_words_lst.pop(0)+'\n')

# print(ord('ぁ'))
# for i in range(0,86):
#     print(chr(12353+i))
# print(ord('ァ'))
# for i in range(0,92):
#     print(chr(12449+i))


