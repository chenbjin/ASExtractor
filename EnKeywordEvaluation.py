#-*- encoding: utf-8 -*-
import os
from EnExtractor import EnExtractor
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def get_all_abstracts(basepath):
	return os.listdir(basepath+'/abstracts')

def get_keyphrases(basepath, filelist):
	correct_num = 0
	system_key_num = 0
	for f in filelist:
		#print 'deal with:',f
		evaluation = EnExtractor()
		text = open(basepath+'/abstracts/'+f,'r').read()
		system_keyphrases = evaluation.keyphrase_train(text=text, article_type='Abstract')
		system_key_num += len(system_keyphrases)
		
		#tag_word = evaluation.get_tag(text=text)
		content = open(basepath+'/keywords/'+f,'r').read()
		mannual_keyphrases = content.split(';')
		correct_num += eval_keyphrase(system_keyphrases,mannual_keyphrases,12)
		print correct_num
	return correct_num ,system_key_num

def eval_keyphrase(system_keyphrases,mannual_keyphrases,num):
	correct_num = 0
	system_keyphrases = system_keyphrases[:num]
	for keyphrase in mannual_keyphrases:
		if keyphrase.strip().lower() in system_keyphrases:
			#print keyphrase.strip().lower()
			correct_num += 1
	return correct_num

if __name__ == '__main__':
	
	basepath = '../data_preprocessing/train_data'
	filelist = get_all_abstracts(basepath)

	correct_num = 0
	#system_key_num = 12*len(filelist)
	
	correct_num,system_key_num = get_keyphrases(basepath, filelist)

	mannual_key_num = 8932
	average_num = correct_num*1.0 / len(filelist)
	precision = correct_num*1.0 / system_key_num
	recall = correct_num*1.0 / mannual_key_num
	f_measure = 2*precision*recall / (precision + recall)
	print '-------------------'
	print 'mannual_key_num:' , mannual_key_num
	print 'system_key_num:', system_key_num
	print 'correct_num:', correct_num
	print 'average_num:', average_num
	print 'Precision: ', precision
	print 'Recall:', recall
	print 'F-measure:', f_measure
'''
keyphrase: 12/per, get_keyphrases_maximal
-------------------
mannual_key_num: 8932
system_key_num: 9264
correct_num: 2923
average_num: 3.78626943005
Precision:  0.315522452504
Recall: 0.327250335871
F-measure: 0.321279396882
[Finished in 512.9s]

keyphrase: len(keywords)/3, get_keyphrases_maximal
-------------------
mannual_key_num: 8932
system_key_num: 11439
correct_num: 2861
average_num: 3.70595854922
Precision:  0.250109275286
Recall: 0.320309001343
F-measure: 0.280889499779
[Finished in 541.2s]
'''
