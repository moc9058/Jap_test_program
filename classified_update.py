import os

cwd = os.path.join(os.getcwd(),"OneDrive","바탕 화면","test_program")
save_folder = os.path.join(cwd,'test_log')

group_1_txt = os.path.join(cwd, 'Group 1.txt')

retry_txt = os.path.join(cwd,'classified','retry.txt')
verbs_txt = os.path.join(cwd,'classified','verbs.txt')
adverbs_txt = os.path.join(cwd,'classified','adverbs.txt')
diff_kanjis_txt = os.path.join(cwd,'classified','diff_kanjis.txt')
katakanas_txt = os.path.join(cwd,'classified','katakanas.txt')
jinn_ninn_txt = os.path.join(cwd,'classified','jinn_ninn.txt')
komu_txt = os.path.join(cwd,'classified','komu.txt')
etc_txt = os.path.join(cwd,'classified','etc.txt')

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
with open(group_1_txt, 'r', encoding='utf-8') as f1:
    group_1_origins = []
    group_1_answers = []
    while True:
        line = f1.readline()
        if not line: break
        line = line.split('/-/')
        group_1_origins.append(line[0].strip())
        group_1_answers.append(line[1].strip())

    for txt in classified_txts:
        origins = []
        answers = []
        with open(txt, 'r', encoding='utf-8') as f2:
            while True:
                line = f2.readline()
                if not line: break
                line = line.split('/-/')
                origins.append(line[0].strip())
                answers.append(line[1].strip())
            
        with open(txt, 'w', encoding='utf-8') as f2:
            for i in range(len(origins)):
                try:
                    j = group_1_origins.index(origins[i])
                    f2.write(f"{group_1_origins[j]}/-/{group_1_answers[j]}\n")
                except:
                    f2.write(f"{origins[i]}/-/{answers[i]}\n")