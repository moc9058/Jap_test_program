import os
import functions as func

cwd = os.getcwd()
group_1_txt = os.path.join(cwd,'Group 1.txt')
group_2_txt = os.path.join(cwd,'Group 2.txt')
verbs_txt = os.path.join(cwd,'classified','verbs.txt')
compounds_txt = os.path.join(cwd,'classified','compounds.txt')
extracted_txt = os.path.join(cwd,'extracted_verbs.txt')

extracted_lst = []
verb_lst = []
compound_lst = []

def KNK(three_chars):
    if len(three_chars) != 3:
        raise Exception()
    return func.is_kanji(three_chars[0]) and not func.is_kanji(three_chars[1]) and func.is_kanji(three_chars[2])

with open(extracted_txt,'r',encoding='utf-8') as f:
    while True:
        line = f.readline()
        if not line: break
        line = line.strip()
        extracted_lst.append(line)

with open(verbs_txt,'r',encoding='utf-8') as f:
    while True:
        line = f.readline()
        if not line: break
        line = line.strip()
        verb_lst.append(line)

with open(compounds_txt,'r',encoding='utf-8') as f:
    while True:
        line = f.readline()
        if not line: break
        line = line.strip()
        compound_lst.append(line)

with open(verbs_txt,'w',encoding='utf-8') as f:
    while verb_lst:
        line = verb_lst.pop(0)
        if not line in extracted_lst:
            f.write(line+'\n')


with open(compounds_txt,'w',encoding='utf-8') as f:
    while compound_lst:
        line = compound_lst.pop(0)
        if not line in extracted_lst:
            f.write(line+'\n')
# print(ord('ぁ'))
# for i in range(0,86):
#     print(chr(12353+i))
# print(ord('ァ'))
# for i in range(0,92):
#     print(chr(12449+i))