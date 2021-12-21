
import sys
import re
import copy
import time
import json
import trace
from Coverage import Coverage


class QuixbugsDriver:

	def __init__(self,bug_path):
		self.__bug_path=bug_path
		sys.path.insert(0, self.__bug_path)
		self.__module_correct=None
		self.__module_incorrect=None


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
	    buggy_output=self.run_test(algo,*copy.deepcopy(test_input))
	    golden_output=self.run_test(algo,*copy.deepcopy(test_input),correct=True)
	    
	    if(buggy_output==golden_output):
	        return True
	    else:
	        return False


