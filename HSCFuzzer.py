from DFA import DFA
import numpy as np
from DFAparser import DFAparser
import collections
import random
import string

class HSCFuzzer:

	def __init__(self,oracle_ob,sub_prog,multiple_inputs):
		self.__prev_passing_test_cases=[]
		self.__prev_failing_test_cases=[]
		self.__oracle_ob=oracle_ob
		self.__sub_prog=sub_prog
		self.__multiple_inputs=multiple_inputs
		self.__human_labelled=[]


	def __gen_random_prefix_suffix(self,dfa_parser,use_fmin=False):
		fmin=dfa_parser.getfmin()
		rand_length=random.randint(1,10)
		rand_p_s=""

		if(use_fmin):		
			if(self.__multiple_inputs):
				fmin=fmin.replace("_","")
			rand_p_s=fmin
		else:
			for i in range(rand_length):
				rand_chr=random.choice(string.ascii_uppercase+string.digits+string.ascii_lowercase)
				if rand_chr not in fmin:
					rand_p_s+=rand_chr
		return rand_p_s

	def prefix_fuzz(self,dfa_parser,init_failng_tcase):

		self.__human_labelled=[]
		dfa_state_list=dfa_parser.getDFAStateList()
		start_state_trans=dfa_state_list["S"].getTransitions()

		if("any_o" not in start_state_trans.keys()):
			rand_prefix=self.__gen_random_prefix_suffix(dfa_parser)
			test_string=(rand_prefix+init_failng_tcase)

			self.__human_labelled.append(test_string)

			test_case=test_string.split("_")
			if((self.__multiple_inputs==True) and (len(test_case)==1)):
				test_case.append("")

			human_label=self.__oracle_ob.ask_human(test_case,self.__sub_prog)
			if(not human_label):
				start_state_trans["any_o"]="self"


	def suffix_fuzz(self,dfa_parser,final_no_trans_strings):
		self.__human_labelled=[]
		dfa_state_list=dfa_parser.getDFAStateList()

		for final_no_key in final_no_trans_strings.keys():
			fmin_rand_suffix=self.__gen_random_prefix_suffix(dfa_parser,True)
			test_case_1_string=(final_no_trans_strings[final_no_key]+fmin_rand_suffix)
			test_case_1=test_case_1_string.split("_")
			if((self.__multiple_inputs==True) and (len(test_case_1)==1)):
				test_case_1.append("")

			rand_suffix=self.__gen_random_prefix_suffix(dfa_parser)
			test_case_2_string=(final_no_trans_strings[final_no_key]+rand_suffix)
			test_case_2=test_case_2_string.split("_")
			if((self.__multiple_inputs==True) and (len(test_case_2)==1)):
				test_case_2.append("")

			t_case_label_1=self.__oracle_ob.ask_human(test_case_1,self.__sub_prog)
			t_case_label_2=self.__oracle_ob.ask_human(test_case_2,self.__sub_prog)

			self.__human_labelled.append(test_case_1_string)
			self.__human_labelled.append(test_case_2_string)

			new_transitions={}	

			if((t_case_label_1==False) and (t_case_label_2==False)):
				new_transitions["any_o"]="self"

			elif(t_case_label_1==False):
				fmin_char=list(collections.Counter(fmin_rand_suffix).keys())
				for i_chr in range(1,len(fmin_char)+1):
					new_transitions["all_fmin"+str(i_chr)]="self"

			if(len(new_transitions)>0):
				dfa_state_list[final_no_key].setTransitions(new_transitions)








			






