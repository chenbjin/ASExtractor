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

	mannual_key_num = 8875
	average_num = correct_num*1.0 / len(filelist)
	precision = correct_num*1.0 / system_key_num
	recall = correct_num*1.0 / mannual_key_num
	f_measure = 2*precision*recall / (precision + recall)
	print '-------------------'
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
'''
keyphrase: all, get_keyphrases_maximal
-------------------
mannual_key_num: 8932
system_key_num: 13777
correct_num: 4114
average_num: 5.39187418087
Precision:  0.298613631415
Recall: 0.460591133005
F-measure: 0.36232330794
--------------------

keyphrase: all, get_keyphrases_maximal
-------------------
article_num: 763
mannual_key_num: 8875
system_key_num: 13777
correct_num: 4114
average_num: 5.39187418087
Precision:  0.298613631415
Recall: 0.463549295775
F-measure: 0.363235034434
--------------------

keyphrase:len(keywords)/3+1, get_keyphrases_maximal
-------------------
article_num: 763
mannual_key_num: 8875
system_key_num: 11914
correct_num: 3758
average_num: 4.9252948886
Precision:  0.315427228471
Recall: 0.423436619718
F-measure: 0.361537351484s
--------------------

'''