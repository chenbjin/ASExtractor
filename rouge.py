#-*- encoding: utf-8 -*-
from pyrouge import Rouge155

r = Rouge155()
#r.system_dir = '/home/chenbjin/SearchJob/DUC2002_Summarization_Documents/system'
#r.model_dir = '/home/chenbjin/SearchJob/DUC2002_Summarization_Documents/model'

r.system_dir = '/home/chenbjin/SearchJob/DUC2002_Summarization_Documents/wordnet.system.summary/'
r.model_dir = '/home/chenbjin/SearchJob/DUC2002_Summarization_Documents/model.summary/'

r.system_filename_pattern = "DUC2002.(\d+).txt"
r.model_filename_pattern = "DUC2002.[A-Z].#ID#.txt"

output = r.convert_and_evaluate()
print(output)
output_dict = r.output_to_dict(output)
'''

system_input_dir = '/home/chenbjin/SearchJob/DUC2002_Summarization_Documents/system.summary'
system_output_dir = '/home/chenbjin/SearchJob/DUC2002_Summarization_Documents/system.output'
Rouge155.convert_summaries_to_rouge_format(system_input_dir, system_output_dir)
'''