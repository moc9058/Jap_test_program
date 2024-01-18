import os
import functions as func

cwd = os.getcwd()
paste_copied_source_txt = os.path.join(cwd,'paste_copied_source.txt')
paste_copied_result_txt = os.path.join(cwd,'paste_copied_result.txt')
if not os.path.isfile(paste_copied_source_txt):
    with open(paste_copied_source_txt,'w',encoding='utf-8') as f1:
        pass
origin_classifier = 0
with open(paste_copied_source_txt,'r',encoding='utf-8') as f1:
    with open(paste_copied_result_txt,'w',encoding='utf-8') as f2:
        while True:
            line = f1.readline()
            if not line: break
            line = line.strip()
            if line:
                origin_classifier = (origin_classifier+1)%2
                if origin_classifier == 1:
                    f2.write(line+'\n')