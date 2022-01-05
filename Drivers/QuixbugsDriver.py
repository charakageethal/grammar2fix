
import sys
import re
import copy
import time
import json

class QuixbugsDriver:

	def __init__(self,bug_path):
		self.__bug_path=bug_path
		sys.path.insert(0, self.__bug_path)
		self.__module_correct=None
		self.__module_incorrect=None
		self.__n_human_labelled=0
		self.__human_labelled_passing=[]
		self.__human_labelled_failing=[]


	def run_test(self,algo,*args,correct=False):
		if not correct:
			if self.__module_incorrect is None:
				self.__module_incorrect = __import__("python_programs."+algo)

			module=self.__module_incorrect
		else:
			if self.__module_correct is None:
				self.__module_correct = __import__("correct_python_programs."+algo)

			module=self.__module_correct

		fx = getattr(module, algo)

		try:
			return getattr(fx,algo)(*args)
		except:
			return sys.exc_info()

	def get_test_cases(self,algo,external_path=None):
		py_test_case_list=[]
		if external_path is None:
			working_file = open(self.__bug_path+"/json_testcases/"+algo+".json", 'r')
		else:
			working_file = open(external_path+"/"+algo+".json",'r')

		for line in working_file:

			pytestcase=json.loads(line)
			test_in,test_out=pytestcase
			golden_output=self.run_test(algo,*copy.deepcopy(test_in),correct=True)

			if not isinstance(test_in,list):
				test_in=[test_in]

			py_test_case_list.append([test_in,golden_output])

		return py_test_case_list

	def ask_human(self,test_input,algo):
		if(test_input in self.__human_labelled_passing):
			return True
		elif(test_input in self.__human_labelled_failing):
			return False
		else:
			self.__n_human_labelled+=1
			buggy_output=self.run_test(algo,*copy.deepcopy(test_input))
			golden_output=self.run_test(algo,*copy.deepcopy(test_input),correct=True)
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

