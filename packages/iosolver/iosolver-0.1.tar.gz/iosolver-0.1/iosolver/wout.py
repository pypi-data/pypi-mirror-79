# -*-encoding=utf-8-*-

from shutil import copyfile
import os


def _del_file(path):
	ls=os.listdir(path)
	for i in ls:
		f_path=os.path.join(path,i)
		if os.path.isdir(f_path):
			_del_file(f_path)
		else:
			os.remove(f_path)




def cp_data_by_ls(select_data_ls,source_data_path,target_data_path):
	source_list=os.listdir(source_data_path)

	if not os.path.isdir(target_data_path):
		os.makedirs(target_data_path)

	_del_file(target_data_path)

	for i in select_data_ls:
		if i in source_list:
			sup_source_path="%s\\%s"%(source_data_path,i)
			sup_sample_path="%s\\%s"%(source_data_path,i)
			copyfile(sup_source_path, sup_sample_path)




def ls2t(ls,target_file_path):
	with open(target_file_path,'w') as f:
		for i in ls:
			f.write(str(i)+'\n')
			
