import collections
import string
import random
import math
import numpy as np
import copy


class CharacterFuzz:
	"""docstring for CharacterFuzz"""

	def __init__(self,oracle_ob,test_prog,multiple_inputs):
		self.__oracle_ob=oracle_ob
		self.__multiple_inputs=multiple_inputs
		self.__test_prog=test_prog
		self.__random_char_class=(string.ascii_uppercase+string.digits+string.ascii_lowercase+string.punctuation.replace("_",""))
		self.__human_labelled=[]


	def set_char_class(self,random_char_class):
		self.__random_char_class=random_char_class


	def __mutated_fmin(self,f_min,prev_assignments):
		mutate_ops=["add_one","subtract_one","add_five","subtract_five"]


		def add_one(input_val):
			return input_val+1

		def subtract_one(input_val):
			return input_val-1

		def add_five(input_val):
			return input_val+5

		def subtract_five(input_val):
			return input_val-5

		def init_chr(input_val):
			return 0

		freq_list=collections.Counter(f_min)

		if(self.__multiple_inputs):
			del freq_list["_"]


		char_pos_list={}
		
		for k in freq_list.keys():
			char_pos_list[k]=[i for i in range(len(f_min)) if f_min[i]==k]


		found_new=False
		new_assignment=None


		while(not found_new):
			rand_assignment=copy.deepcopy(random.choice(prev_assignments))
			isValid=False

			while(not isValid):
				new_chars=[]
				rand_subset=np.random.choice(len(rand_assignment),np.random.randint(low=1,high=len(rand_assignment)+1),replace=False)

				for r_ind in rand_subset:
					found_new_char=False

					if(rand_assignment[r_ind]==" "):
						continue

					while(not found_new_char):
						stack_size=np.random.randint(low=1,high=10)
						random_ops=random.choices(mutate_ops,k=stack_size)

						new_chr_ascii=self.__random_char_class.find(rand_assignment[r_ind])

						try:
							for op in random_ops:
								new_chr_ascii=locals()[op](new_chr_ascii)
					
							new_chr=self.__random_char_class[new_chr_ascii%len(self.__random_char_class)]

							if new_chr not in new_chars:
								rand_assignment[r_ind]=new_chr
								found_new_char=True
								new_chars.append(new_chr)
							else:
								continue
						except:
							break

				if(len(rand_assignment)!=len(list(set(rand_assignment)))):
					continue
				new_assignment=rand_assignment

				if new_assignment not in prev_assignments:
					isValid=True
					if (isValid):
						found_new=True

		f_char_list=list(freq_list.keys())
		f_min_list=list(f_min)

		for	r_i in range(len(f_char_list)):
			for char_pos in char_pos_list[f_char_list[r_i]]:
				f_min_list[char_pos]=new_assignment[r_i] 		

		
		return "".join(f_min_list),new_assignment


	def get_character_class(self,fmin,f_iter=None):
		self.__human_labelled=[]	
		if f_iter is None:
			fuzz_iter=20
		else:
			fuzz_iter=f_iter

		n_ftcase=0
		n_ptcase=0

		char_list=collections.Counter(fmin)

		if(self.__multiple_inputs):
			del char_list["_"]

		F_neg_assignment=[]
		prev_assignment=[]

		prev_assignment.append(list(char_list.keys()))
		max_limit=math.pow(len(self.__random_char_class),len(char_list.keys()))
		completed_iterations=0

		for i in range(fuzz_iter):
			if(len(prev_assignment)==max_limit):
				break

			fnew_min,assignment=self.__mutated_fmin(fmin,prev_assignment)
			prev_assignment.append(assignment)

			self.__human_labelled.append(fnew_min)

			test_case=fnew_min.split('_')
			if((self.__multiple_inputs==True) and (len(test_case)==1)):
				test_case.append("")				
			fmin_human_label=self.__oracle_ob.ask_human(test_case,self.__test_prog)

			if(not fmin_human_label):
				n_ftcase+=1
			else:
				n_ptcase+=1
				F_neg_assignment.append(assignment)

			completed_iterations+=1

		s_rate=(n_ptcase/completed_iterations)

		if(s_rate==1):
			return "All_pass"
		else:
			return F_neg_assignment


