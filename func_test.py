import os
import functions as func

cwd = os.getcwd()

group_txt_lst = ['Group 1.txt', 'Group 2.txt', 'Group 3.txt']
group_1_txt = os.path.join(cwd,'Group 1.txt')
group_2_txt = os.path.join(cwd,'Group 2.txt')
group_3_txt = os.path.join(cwd,'Group 3.txt')
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



retry_completed_txt = os.path.join(cwd,'retry_completed_txt.txt')
retry_completed_lst = []

func.copy_txt2lst_combined(classified_lsts, classified_txts, origin_candidates)
func.copy_txt2lst(retry_completed_lst, retry_completed_txt, origin_candidates)

for i in range(len(origin_candidates)):
    origin = origin_candidates[i]
    answer = answer_candidates[i]
    if func.contains_kanji(origin):
        pronounciation = answer.split()[0].strip()
    else:
        pronounciation = origin
    if '、' in pronounciation:
        print(origin)
# with open(os.path.join(cwd,'remote.ipynb'), 'w') as f:
#     f.write("{\n")
#     f.write(" \"cells\": [\n")

#     f.write("],\n")
#     f.write("}\n")
# print(func.is_kanji('～'))
# print(func.is_kanji('～'))
# print(ord('～'))


# tmp_lsts = [verb_lst, adverb_lst, diff_kanji_lst, katakana_lst,\
#               hononym_lst, compound_lst, expression_lst]

# etc_lst.sort()
# with open(etc_txt, 'w', encoding='utf-8') as f:
#     for i in range(len(etc_lst)):
#         to_write = True
#         etc = etc_lst[i]
#         for tmp_lst in tmp_lsts:
#             if etc in tmp_lst:
#                 to_write = False
#         if to_write:
#             f.write(etc+'\n')
        
# print(ord('ぁ'))
# for i in range(0,86):
#     print(chr(12353+i))
# print(ord('ァ'))
# for i in range(0,92):
#     print(chr(12449+i))