#-*- encoding: utf-8 -*-
import os
import string

def getfilelist(path):
	return sorted(os.listdir(path))

def renamefile(path,filename,i):
	oldname = path + filename
	newname = path + "DUC2002-"+ string.zfill(i,3)+'.txt'
	os.rename(oldname, newname)

def main():
	system_path = "/home/chenbjin/SearchJob/DUC2002_Summarization_Documents/ld.system.summary/"
	system_filelist = getfilelist(system_path)

	#model_path = "/home/chenbjin/SearchJob/DUC2002_Summarization_Documents/stand.model.summary2/"
	#model_filelist = getfilelist(model_path)

	#wn_system_path ="/home/chenbjin/SearchJob/ASExtractor/wn.system.summary/"
	#wn_system_filelist = getfilelist(wn_system_path)
 	
 	i = 0
	for filename in system_filelist:
		renamefile(system_path, filename, i)
		#renamefile(model_path, filename, i)
		#renamefile(wn_system_path,filename,i)
		i += 1
	print "--done----"

if __name__ == '__main__':
	main()