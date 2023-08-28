import os

cwd = os.path.join(os.getcwd(),"OneDrive","바탕 화면","test_program")

verbs_txt = os.path.join(cwd,'classified','verbs.txt')
adverbs_txt = os.path.join(cwd,'classified','adverbs.txt')
diff_kanjis_txt = os.path.join(cwd,'classified','diff_kanjis.txt')
etc_txt = os.path.join(cwd,'classified','etc.txt')

if not os.path.isfile(verbs_txt):
    with open(verbs_txt, 'w') as f:
        pass
if not os.path.isfile(adverbs_txt):
    with open(adverbs_txt, 'w') as f:
        pass
if not os.path.isfile(diff_kanjis_txt):
    with open(diff_kanjis_txt, 'w') as f:
        pass
if not os.path.isfile(etc_txt):
    with open(etc_txt, 'w') as f:
        pass

current_txts = [verbs_txt,adverbs_txt,diff_kanjis_txt,etc_txt]

def seperation(new_seperator, new_txt_name):
    new_txt = os.path.join(cwd,'classified',new_txt_name)
    
    if not os.path.isfile(new_txt):
        with open(new_txt, 'w') as f:
            pass
    
    with open(new_txt, 'a', encoding='utf-8') as f:
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
                    if new_seperator in words[i]:
                        f.write(f"{words[i]}/-/{answers[i]}\n")
                    else:
                        g.write(f"{words[i]}/-/{answers[i]}\n")

seperation('人','jinn_ninn.txt')
seperation('込む','komu.txt')