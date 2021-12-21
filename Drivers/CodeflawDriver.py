import os
import sys
import subprocess
import copy
import re

class CodeflawDriver:

	def __init__(self,bug_path,iteration=1):
		self.__bug_path=bug_path.rstrip('/')
		self.__iteration=iteration

	def __get_golden_and_buggy(self,bug_folder):

		folder_parts=bug_folder.split('-')

		buggy_version=folder_parts[0]+"-"+folder_parts[1]+"-"+folder_parts[3]
		golden_version=folder_parts[0]+"-"+folder_parts[1]+"-"+folder_parts[4]

		return golden_version,buggy_version

	def get_test_cases(self,bug_folder):

		test_inputs=[]

		for _,_,file_list in os.walk(self.__bug_path+"/"+bug_folder):

			for f in file_list:
				if re.search(".*input-.*",f):
					data_in=open(self.__bug_path+"/"+bug_folder+"/"+f,'r',encoding='utf-8').read()
					fout=f.replace("input","output")
					data_out=open(self.__bug_path+"/"+bug_folder+"/"+fout,'r',encoding='utf-8').read()
					test_inputs.append([[data_in.rstrip('\n')],data_out.rstrip('\n')])

		return test_inputs

	def run_test(self,bug_folder,test_input,correct=False):
		if not correct:
			_,version=self.__get_golden_and_buggy(bug_folder)
		else:
			version,_=self.__get_golden_and_buggy(bug_folder)

		process=subprocess.Popen(('echo', test_input), stdout=subprocess.PIPE)
		test_output=""

		try:
			test_output = subprocess.check_output(["timeout","-k","2s","2s", self.__bug_path+"/"+bug_folder+"/"+version], stdin=process.stdout,encoding="utf-8")
		except:
			pass

		return test_output

	def ask_human(self,test_input,bug_folder):
	    buggy_output=self.run_test(bug_folder,*copy.deepcopy(test_input))
	    golden_output=self.run_test(bug_folder,*copy.deepcopy(test_input),correct=True)
	    
	    if(buggy_output==golden_output):
	        return True
	    else:
	        return False



