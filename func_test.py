import os

file = os.path.join(os.getcwd(),'Group 1.txt')

def is_sorted(txt):
    curr_line = None
    with open(txt, 'r', encoding='utf-8') as f:
        while True:
            new_line = f.readline()
            if not new_line: break
            if not curr_line:
                curr_line = new_line
                continue
            if curr_line > new_line:
                return False
    return True

print(is_sorted(file))