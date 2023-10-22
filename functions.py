import os
import openai
import time
import threading

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_example_sentence(word, lst, boolean = True):
    # Requires lst in order to pass a data to the main thead.
    if boolean:
        if word[0] == '（':
            word = word[word.find('）')+1:]
        elif word[0] == '～':
            word = word[1:]
        response = openai.ChatCompletion.create(
            model = "gpt-4",
            messages=[
            {"role": "user", "content": f"Compose a Japanese sentence using \"{word}\" without any additional explanation."}
        ]
        )
        lst.append(f"（例文）\n{response['choices'][0]['message']['content']}")

def merge_sorted_lsts(lsts_lst):
    # Assume there exists at least one element
    def get_min_index(lst):
        ans = 0
        while not lst[ans]:
            ans += 1
        for i in range(ans+1, len(lst)):
            if not lst[i]:
                continue
            if lst[i] < lst[ans]:
                ans = i
        return ans
    def only_one_False(bool_elem_lst):
        ans = False
        for bool_elem in bool_elem_lst:
            if not bool_elem and not ans:
                ans = True
            elif not bool_elem and ans:
                return False
        return ans
    result_lst = []
    N = len(lsts_lst)
    indices_lst = [0]*N
    popped_elem_lst = []
    be_finished_lst = [False]*N
    for i in range(N):
        try:
            popped_elem_lst.append(lsts_lst[i][indices_lst[i]])
        except:
            popped_elem_lst.append(None)
            be_finished_lst[i] = True

    while not only_one_False(be_finished_lst):
        min_index = get_min_index(popped_elem_lst)
        result_lst.append(popped_elem_lst[min_index])
        indices_lst[min_index] += 1
        try:
            popped_elem_lst[min_index] = lsts_lst[min_index][indices_lst[min_index]]
        except:
            popped_elem_lst[min_index] = None
            be_finished_lst[min_index] = True

    not_finished_lst_index = 0
    for i in range(N):
        if not be_finished_lst[i]:
            not_finished_lst_index = i
            break
    result_lst.extend(lsts_lst[not_finished_lst_index][indices_lst[not_finished_lst_index]:])
    return result_lst


def merge_txts(txts_lst, new_txt):
    if not os.path.isfile(new_txt):
        create_txt(new_txt)
    lst = []
    for txt in txts_lst:
        with open(txt,'r',encoding='utf-8') as f:
            while True:
                line = f.readline()
                if not line: break
                lst.append(line.strip())
    lst.sort()
    with open(new_txt,'w',encoding='utf-8') as f:
        while lst:
            f.write(lst.pop(0)+'\n')

def is_kanji_word(string):
    # Assume string is either hiragana, katakana, and kanji
    for i in range(len(string)):
        if not is_kanji(string[i]) and string[i] != '～':
            return False
    return True



def extract_pronounciations(string):
    # Assume 日本語/-/にほんご 일본어 or にほんご/-/일본어
    string = string.split('/-/')
    front = string[0].strip()
    back = string[1].strip()
    if contains_kanji(front):
        return back.split()[0].strip()
    else:
        return front

def txt_merge(branch_txt, body_txt):
    body_lst = []
    branch_lst = []
    with open(body_txt, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line: break
            body_lst.append(line.strip())

    with open(branch_txt, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line: break
            branch_lst.append(line.strip())
    
    while branch_lst:
        branch_pop = branch_lst.pop(0)
        if not branch_pop in body_lst:
            body_lst.append(branch_pop)
            
    body_lst.sort()
    with open(body_txt,'w',encoding='utf-8') as f:
        while body_lst:
            f.write(body_lst.pop(0)+'\n')

def verb_extractor(original_txt, extracted_txt, mode = 0):
    # Assume 日本語/-/にほんご 일본어
    # mode = 0: retry
    # mode = 1: full
    lines = []
    with open(original_txt, 'r', encoding='utf-8') as f:
        if not mode:
            while True:
                line = f.readline()
                if not line: break
                line = line.strip()
                line_stripped = line.split('/-/')[0].strip()
                if not not_verb(line_stripped):
                    lines.append(line_stripped)
        else:
            while True:
                line = f.readline()
                if not line: break
                line = line.strip()
                line_stripped = line.split('/-/')[0].strip()
                if not not_verb(line_stripped):
                    lines.append(line)
                
    with open(extracted_txt,'w',encoding='utf-8') as f:
        while lines:
            f.write(lines.pop(0)+'\n')

def not_verb(string):
    # assume string has been stripped.
    return not string[-1] in ['う','る','つ','ぶ','ぬ','む','く','ぐ','す']

def txt_sort(txt):
    lines = []
    with open(txt, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line: break
            lines.append(line)
    lines.sort()
    with open(txt, 'w', encoding='utf-8') as f:
        while lines:
            f.write(lines.pop(0))

def create_txt(txt):
    if not os.path.isfile(txt):
        with open(txt, 'w') as f:
            pass

def create_txt_combined(lst):
    for txt in lst:
        create_txt(txt)

def is_katakana(string):
    for i in range(len(string)):
        char = string[i]
        if ord(char) < 12449 or ord(char) >= 12541:
            return False
    return True

def is_kanji(char):
    # Assume char is either hiragana, katakana, and kanji
    if ord(char) < 12289:
        return True
    elif ord(char) >= 12290 and ord(char) < 12353:
        return True
    elif ord(char) >= 12439 and ord(char) < 12449:
        return True
    elif ord(char) >= 12541 and ord(char) < 65288:
        return True
    elif ord(char) >= 65290 and ord(char) < 65374:
        return True
    elif ord(char) >= 65375:
        return True
    else:
        return False

def contains_kanji(string):
    for i in range(len(string)):
        char = string[i]
        if is_kanji(char):
            return True
    return False

def print_word_duplicated(txt_name):
    origin_lst = []
    dup_lst = []
    with open(txt_name, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line: break
            origin_lst.append(line.strip())
    for i in range(len(origin_lst)):
        for j in range(i):
            if origin_lst[i] == origin_lst[j]:
                dup_lst.append(origin_lst[i])
    if dup_lst:
        print(f"{os.path.basename(txt_name)}\n{dup_lst}")
    else:
        return
    

def properly_included(member_txt_lst, group_txt):
    improper_words = []
    group_words = []
    with open(group_txt, 'r', encoding='utf-8') as group_f:
        while True:
            line = group_f.readline()
            if not line: break
            group_words.append(line.split('/-/')[0].strip())
    
    for member_txt in member_txt_lst:
        with open(member_txt, 'r', encoding='utf-8') as member_f:
            while True:
                line = member_f.readline()
                if not line: break
                line = line.strip()
                if not (line in group_words):
                    improper_words.append(f"{os.path.basename(member_txt)}, {line}")
                else:
                    group_words.remove(line)
    return group_words

def copy_txt2sorted_lst(lst,txt, candidate_lst):
    with open(txt,'r',encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line: break
            line = line.strip()
            if line in candidate_lst:
                lst.append(line.strip())
    lst.sort()

def copy_txt2sorted_lst_combined(lsts, txts, candidate_lst):
    if len(lsts) != len(txts):
        print("Lengths are different.")
        return
    for i in range(len(lsts)):
        copy_txt2sorted_lst(lsts[i],txts[i], candidate_lst)

def update_lst2sorted_txt(lst, txt, candidate_lst, mode = 0):
    tmp_lst = lst.copy()
    if mode == 0 and (os.path.basename(txt) == 'retry.txt' or os.path.basename(txt) == 'retry_completed_txt.txt'):
        txt_lst = []
        with open(txt, 'r', encoding='utf-8') as f:
            while True:
                line = f.readline()
                if not line: break
                txt_lst.append(line.strip())
        
        for txt_word in txt_lst:
            if not txt_word in lst:
                tmp_lst.append(txt_word)
    
    tmp_lst.sort()
    tmp_tmp_lst = tmp_lst.copy()
    for i in range(len(tmp_tmp_lst)-1):
        if tmp_tmp_lst[i] == tmp_tmp_lst[i+1]:
            tmp_lst.remove(tmp_tmp_lst[i])
    
    with open(txt,'w',encoding='utf-8') as f:
        while tmp_lst:
            word = tmp_lst.pop(0).strip()
            if word in candidate_lst:
                f.write(word + '\n')
            else:
                print(f"({os.path.basename(txt)}){word} is not included in the Group.")

def update_lst2sorted_txt_combined(lsts, txts, candidate_lst):
    if len(lsts) != len(txts):
        print("Lengths are different.")
        return
    for i in range(len(lsts)):
        update_lst2sorted_txt(lsts[i], txts[i], candidate_lst)

def word_count(txt_name):
    count = 0
    with open(txt_name, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line: break
            count += 1
    return count


def word_count_combined(txts):
    result = 0
    for txt in txts:
        result += word_count(txt)
    return result

def print_word_duplicated_combined(txts):
    for txt in txts:
        print_word_duplicated(txt)

def seperation(new_seperators, new_txt, curr_txts):
    words = []
    with open(new_txt, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line: break
            line = line.strip()
            if not line in words:
                words.append(line)
    
    with open(new_txt, 'w', encoding='utf-8') as f:
        for txt in curr_txts:
            txt_words = []
            with open(txt,'r', encoding='utf-8') as g:
                while True:
                    line = g.readline()
                    if not line: break
                    txt_words.append(line.strip())
            txt_words.sort()

            with open(txt,'w', encoding='utf-8') as g:
                for txt_word in txt_words:
                    seperated = False
                    for new_seperator in new_seperators:
                        if new_seperator in txt_word:
                            if not txt_word in words:
                                words.append(txt_word)
                            seperated = True
                            break
                    if not seperated:
                        g.write(txt_word+'\n')
        words.sort()
        for word in words:
            f.write(word+'\n')