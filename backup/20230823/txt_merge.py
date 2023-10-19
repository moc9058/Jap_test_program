import os
import glob
from datetime import datetime
import time
import random


cwd = os.path.join(os.getcwd(),"OneDrive","바탕 화면","test_program")
groups = ['Group 1_before.txt','Group 2_before.txt','Group 3_before.txt']
new_group = os.path.join(cwd,'Group 1.txt')
with open(new_group,'w',encoding='utf-8') as f1:
    for group in groups:
        with open(os.path.join(cwd,group),'r',encoding='utf-8') as f2:
            while True:
                line = f2.readline()
                if not line: break
                f1.write(line)



