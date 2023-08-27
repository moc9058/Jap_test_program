import os
from datetime import datetime

cwd = os.path.join(os.getcwd(),"OneDrive","바탕 화면","test_program")
save_folder = os.path.join(cwd,'test_log')
retry_txt = os.path.join(cwd,'classified','retry.txt')
verbs_txt = os.path.join(cwd,'classified','verbs.txt')
adverbs_txt = os.path.join(cwd,'classified','adverbs.txt')
diff_kanjis_txt = os.path.join(cwd,'classified','diff_kanjis.txt')
katakanas_txt = os.path.join(cwd,'classified','katakanas.txt')
jinn_ninn_txt = os.path.join(cwd,'classified','jinn_ninn.txt')
etc_txt = os.path.join(cwd,'classified','etc.txt')

current_txts = [verbs_txt,adverbs_txt,diff_kanjis_txt,etc_txt]
with open(jinn_ninn_txt, 'a', encoding='utf-8') as f:
    for txt in current_txts:
        words = []
        answers = []
        with open(txt,'r', encoding='utf-8') as g:
            while True:
                line = g.readline()
                if not line: break
                words.append(line.split('/-/')[0].strip())
                answers.append(line.split('/-/')[1].strip())

        with open(txt,'w', encoding='utf-8') as g:
            for i in range(len(words)):
                if '人' in words[i]:
                    f.write(f"{words[i]}/-/{answers[i]}\n")
                else:
                    g.write(f"{words[i]}/-/{answers[i]}\n")
