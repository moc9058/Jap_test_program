import os
import functions as func

cwd = os.getcwd()
group_2_txt = os.path.join(cwd,'Group 2.txt')
extracted_txt = os.path.join(cwd,'extracted_verbs.txt')
extracted_txt_retry = os.path.join(cwd,'extracted_verbs_retry.txt')
func.verb_extractor(group_2_txt,extracted_txt, 1)
func.verb_extractor(group_2_txt,extracted_txt_retry, 0)

