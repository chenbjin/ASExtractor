#-*- encoding: utf-8 -*-
import os
from EnExtractor import EnExtractor
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def get_all_abstracts(basepath):
	return sorted(os.listdir(basepath+'/abstracts'))

def get_keyphrases(basepath, filelist):
	correct_num = 0
	system_key_num = 0
	wrong_file = []
	for f in filelist:
		#print 'deal with:',f
		evaluation = EnExtractor()
		text = open(basepath+'/abstracts/'+f,'r').read()
		system_keyphrases = evaluation.keyphrase_train(text=text, article_type='Abstract')
		system_key_num += len(system_keyphrases)

		#tag_word = evaluation.get_tag(text=text)
		content = open(basepath+'/keywords/'+f,'r').read()
		mannual_keyphrases = content.split(';')
		'''test for 0 corret_num file'''
		tmp = eval_keyphrase(system_keyphrases,mannual_keyphrases)
		correct_num += tmp
		print 'file-',f,':',correct_num
		if tmp == 0:
			wrong_file.append(f)
	return correct_num ,system_key_num , wrong_file

def eval_keyphrase(system_keyphrases,mannual_keyphrases,num=None):
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
	
	correct_num,system_key_num,wrong_file = get_keyphrases(basepath, filelist)

	mannual_key_num = 7884
	average_num = correct_num*1.0 / len(filelist)
	precision = correct_num*1.0 / system_key_num
	recall = correct_num*1.0 / mannual_key_num
	f_measure = 2*precision*recall / (precision + recall)
	print '-------------------15 keyword, modified w=get_similarity(stemmed), get_keyphrases_maximal'
	print 'article_num:',len(filelist)
	print 'mannual_key_num:' , mannual_key_num
	print 'system_key_num:', system_key_num
	print 'correct_num:', correct_num
	print 'average_num:', average_num
	print 'Precision: ', precision
	print 'Recall:', recall
	print 'F-measure:', f_measure
	print '--------------------'
	print 'wrong_file:',wrong_file
'''
-------------------20 keyword, w=1.0, modified get_keyphrases_maximal
-------------------20 keyword, w=get_weight(6,3,1), modified get_keyphrases_maximal
-------------------20 keyword, w=get_weight(6,2,2), modified get_keyphrases_maximal
-------------------20 keyword, w=get_weight(5,3,2), modified get_keyphrases_maximal
article_num: 674
mannual_key_num: 7884
system_key_num: 11187
correct_num: 3590
average_num: 5.32640949555
Precision:  0.320908197014
Recall: 0.455352612887
F-measure: 0.37648786115
--------------------

-------------------20 keyword, modified w=get_weight(5,3,2), get_keyphrases_maximal
article_num: 674
mannual_key_num: 7884
system_key_num: 11246
correct_num: 3598
average_num: 5.33827893175
Precision:  0.319935977236
Recall: 0.45636732623
F-measure: 0.376163094616
--------------------

-------------------20 keyword, modified w=get_weight(8,1,1), get_keyphrases_maximal
article_num: 674
mannual_key_num: 7884
system_key_num: 11220
correct_num: 3600
average_num: 5.3412462908
Precision:  0.320855614973
Recall: 0.456621004566
F-measure: 0.376884422111
--------------------

-------------------20 keyword, modified w=get_weight(7,2,1), get_keyphrases_maximal
article_num: 674
mannual_key_num: 7884
system_key_num: 11242
correct_num: 3600
average_num: 5.3412462908
Precision:  0.320227717488
Recall: 0.456621004566
F-measure: 0.376450904528
--------------------

-------------------20 keyword, modified w=get_similarity, get_keyphrases_maximal
article_num: 674
mannual_key_num: 7884
system_key_num: 9482
correct_num: 3132
average_num: 4.646884273
Precision:  0.330310061169
Recall: 0.397260273973
F-measure: 0.360704825521
--------------------
-------------------20 keyword, modified w=get_similarity(stemmed), get_keyphrases_maximal
article_num: 674
mannual_key_num: 7884
system_key_num: 9486
correct_num: 3135
average_num: 4.65133531157
Precision:  0.330487033523
Recall: 0.397640791476
F-measure: 0.360967184801
--------------------
-------------------15 keyword, modified w=get_similarity(stemmed), get_keyphrases_maximal
article_num: 674
mannual_key_num: 7884
system_key_num: 8854
correct_num: 2966
average_num: 4.40059347181
Precision:  0.334989835103
Recall: 0.376204972095
F-measure: 0.354403154499
--------------------
-------------------10 keyword, modified w=get_similarity(stemmed), get_keyphrases_maximal
article_num: 674
mannual_key_num: 7884
system_key_num: 7769
correct_num: 2632
average_num: 3.90504451039
Precision:  0.33878234007
Recall: 0.333840690005
F-measure: 0.336293362295
--------------------


'''