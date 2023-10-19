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

def seperation(new_seperator_lst, new_txt_name, curr_txts):
    new_txt = os.path.join(cwd,'classified',new_txt_name)
    
    with open(new_txt, 'w', encoding='utf-8') as f:
        for txt in curr_txts:
            words = []
            with open(txt,'r', encoding='utf-8') as g:
                while True:
                    line = g.readline()
                    if not line: break
                    words.append(line.strip())

            with open(txt,'w', encoding='utf-8') as g:
                for i in range(len(words)):
                    seperated = False
                    for new_seperator in new_seperator_lst:
                        if new_seperator in words[i]:
                            f.write(f"{words[i]}\n")
                            seperated = True
                            break
                    if not seperated:
                        g.write(f"{words[i]}\n")

# seperation('人','jinn_ninn.txt',current_txts)

def take_origin_only(curr_txt_name, new_txt_name):
    # assume curr_txt_name as 日本語/-/にほんご 일본어
    with open(curr_txt_name, 'r', encoding='utf-8') as f1:
        with open(new_txt_name, 'w', encoding='utf-8') as f2:
            while True:
                line = f1.readline()
                if not line: break
                line = line.split('/-/')[0].split()
                f2.write(line)
