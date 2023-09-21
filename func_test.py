import os
import functions as func

cwd = os.getcwd()

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

retry_completed_txt = os.path.join(cwd,'retry_completed_txt.txt')
retry_completed_lst = []

func.copy_txt2lst_combined(classified_lsts, classified_txts)
func.copy_txt2lst(retry_completed_lst, retry_completed_txt)

for tmp in retry_completed_lst:
    try:
        retry_lst.remove(tmp)
    except:
        print(tmp)
retry_lst.sort()
with open(retry_txt,'w',encoding='utf-8') as f:
    while retry_lst:
        f.write(retry_lst.pop(0)+'\n')


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