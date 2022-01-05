import os
import sys
import subprocess
import copy
import re

class IntroClassDriver:

	def __init__(self,path_golden):
		self.__path_golden=path_golden.rstrip('/')
		self.__test_prog_name=self.__path_golden.split('/')[-2]
		self.__n_human_labelled=0
		self.__human_labelled_passing=[]
		self.__human_labelled_failing=[]


	def run_test(self,program,test_input):
		process=subprocess.Popen(('echo', test_input), stdout=subprocess.PIPE)
		test_output=""

		try:
			test_output = subprocess.check_output(["timeout","-k","2s","2s", program], stdin=process.stdout,encoding="utf-8")
		except:
			pass

		return test_output

	def get_test_cases(self):
		test_inputs=[]

		for _, _,file_list in os.walk(self.__path_golden+"/whitebox"):
			for f in file_list:
				if (re.search("in$",f) and (len(f.split('_'))==1)):
					data_in=open(self.__path_golden+"/whitebox/"+f,'r', encoding='utf-8').read()
					fout=f.replace("in","out")
					data_out=open(self.__path_golden+"/whitebox/"+fout,'r', encoding='utf-8').read()
					test_inputs.append([[data_in.rstrip('\n')],data_out])

		return test_inputs

	def ask_human(self,test_input,program):
		if(test_input in self.__human_labelled_passing):
			return True
		elif(test_input in self.__human_labelled_failing):
			return False
		else:
			self.__n_human_labelled+=1
			buggy_output=self.run_test(program,*copy.deepcopy(test_input))
			golden_prog=self.__path_golden+"/"+self.__test_prog_name
			golden_output=self.run_test(golden_prog,*copy.deepcopy(test_input))
			if(buggy_output==golden_output):
				if (test_input not in self.__human_labelled_passing):
					self.__human_labelled_passing.append(test_input)
				return True
			else:
				if(test_input not in self.__human_labelled_failing):
					self.__human_labelled_failing.append(test_input)
				return False

	def get_human_labelled(self):
		return self.__n_human_labelled,self.__human_labelled_passing,self.__human_labelled_failing

	def set_human_labelled_zero(self):
		self.__n_human_labelled=0
		self.__human_labelled_passing=[]
		self.__human_labelled_failing=[]


