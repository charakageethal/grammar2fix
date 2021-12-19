from DFA import DFA
import numpy as np
import copy
import collections
import itertools

class DFAparser:
	"""docstring for ClassName"""
	def __init__(self,fmin_assignment,dfa,fmin,multiple_inputs):
		self.__fmin_assignment=fmin_assignment
		self.__neg_fmin_assignment=[]
		self.__dfa=dfa
		self.__fmin=fmin
		self.__multiple_inputs=multiple_inputs

		self.__generalize_dfa()



	def __generalize_dfa(self):

		dfa_states=self.__dfa.get_state_list()
		dfa_start_state=self.__dfa.get_start_state()



		char_list=collections.Counter(self.__fmin)

		if(self.__multiple_inputs):
			del char_list["_"]


		fmin_char_list=list(char_list.keys())
		
		fmin_dict={}
		for ch_i in range(1,len(fmin_char_list)+1):
			fmin_dict[fmin_char_list[ch_i-1]]="all_fmin"+str(ch_i)

		for dfa_st_key,dfa_st_val in dfa_states.items():
			st_trans=dfa_st_val.getTransitions()

			if(st_trans is not None):
				new_transisitions={}

				if("self" in st_trans.values()):
					new_transisitions["any_o"]="self"

				for st_key in st_trans.keys():
					if(st_key in fmin_dict.keys()):
						new_transisitions[fmin_dict[st_key]]=st_trans[st_key]
					elif(self.__multiple_inputs and st_key=="_"):
						new_transisitions["_"]=st_trans["_"]
					else:
						if(st_trans[st_key]!="self"):
							new_transisitions[st_key]=st_trans[st_key]

				dfa_st_val.setTransitions(new_transisitions)
			else:
				continue

	def getDFAStateList(self):
		return self.__dfa.get_state_list()

	def getDFA(self):
		return self.__dfa

	def getfmin(self):
		return self.__fmin


	def getfmin_assignment(self):
		return self.__fmin_assignment

	def get_neg_fmin_assignment(self):
		return self.__neg_fmin_assignment


	def setfmin_assignment(self,fmin_assignment):
		self.__fmin_assignment=fmin_assignment

	def set_negfmin_assignment(self,neg_fmin_assignment):
		self.__neg_fmin_assignment=neg_fmin_assignment


	def isAccepting(self,input_str):
		char_list=collections.Counter(self.__fmin)
		input_char_list=collections.Counter(input_str)
		#eligible_list={}	

		#print("input char list:"+str(input_char_list))
		if(self.__multiple_inputs):
			del char_list["_"]
			del input_char_list["_"]


		#print("initial char list:"+str(char_list))
		#print("input char_list"+str(input_char_list))
		
		if(self.__fmin_assignment=="All"):

			#print("eligible_list:"+str(self.get_eligible_character_combiations(char_list.values(),input_char_list)))
			comb_element_list=itertools.combinations(list(input_char_list.keys()),len(char_list.keys()))

			#per_element_list=self.get_eligible_character_combiations(char_list.values(),input_char_list)

			# print("eligible_list:"+str(self.get_eligible_character_combiations(char_list.values(),input_char_list)))

			# with open("test_func.txt","a") as f:
			# 	f.write("reached\n")

			#print(list(per_element_list))

			freq_list=list(char_list.values())

			for ele in comb_element_list:

				comb_list=list(ele)

				comb_eligible=True

				if((" " in char_list.keys()) and (" " not in comb_list)):
					continue

				for comb_char in comb_list:
					if (input_char_list[comb_char]<min(freq_list)):
						comb_eligible=False
						break



				if(not comb_eligible):
					continue
				else:
					per_element_list=itertools.permutations(comb_list)

					for p_ele in per_element_list:

						per_list=list(p_ele)

						if(not self.__check_linear_eligibility(input_str,per_list)):
							continue

						if (per_list in self.__neg_fmin_assignment):
							continue


						all_eligible=True

						for pl_i in range(len(per_list)):
							if(input_char_list[per_list[pl_i]] < freq_list[pl_i]):
								all_eligible=False
								break


						fmin_mapping={}

						if(all_eligible):
							#print(per_list)

							fmin_idx=1
							for el_c in per_list:
								fmin_mapping[el_c]="all_fmin"+str(fmin_idx)
								fmin_idx+=1

							#print(fmin_mapping)

							dfa_start_state=self.__dfa.get_start_state()

							state=dfa_start_state
							complete_string=True


							for chr in input_str:


								if(state.getTransitions() is None):
									complete_string=False
									break

								if chr in fmin_mapping.keys():

									map_chr=fmin_mapping[chr]

									#print("map_chr:"+str(map_chr))

									if map_chr in state.getTransitions().keys():
										state=state.move(map_chr)
									else:
										state=state.move("any_o")

								elif((self.__multiple_inputs) and (chr=="_")):

									if "_" in state.getTransitions().keys():
										state=state.move("_")
									else:
										state=state.move("any_o")
								else:
									if chr in state.getTransitions().keys():
										state=state.move(chr)
									else:

										additional_trans_keys=[]
										for st_trans_k in state.getTransitions().keys():
											# if ((st_trans_k not in fmin_mapping.values()) and (st_trans_k!="any_o") and (self.__multiple_inputs and st_trans_k!="_")):
											# 	print("reached:"+st_trans_k)
											# 	additional_trans_keys.append(st_trans_k)

											if(self.__multiple_inputs):
												if ((st_trans_k not in fmin_mapping.values()) and (st_trans_k!="any_o") and (st_trans_k!="_")):
													#print("reached-A")
													additional_trans_keys.append(st_trans_k)
											else:
												if ((st_trans_k not in fmin_mapping.values()) and (st_trans_k!="any_o")):
													#print("reached-B")
													additional_trans_keys.append(st_trans_k)


										if(len(additional_trans_keys)==0):
											state=state.move("any_o")
										else:
											rand_trans=np.random.choice(additional_trans_keys)
											state=state.move(rand_trans)


								if(state is None):
									#print("None state reached...")
									break


							if ((state is not None) and (state.isFinal()) and (complete_string)):
								#print("True : sss")
								return True
		else:

			for char_comb in self.__fmin_assignment:
				fmin_idx=1

				fmin_mapping={}

				for comb_c in char_comb:
					fmin_mapping[comb_c]="all_fmin"+str(fmin_idx)
					fmin_idx+=1

				#print(fmin_mapping)

				dfa_start_state=self.__dfa.get_start_state()

				state=dfa_start_state
				complete_string=True
		
				for chr in input_str:

					if(state.getTransitions() is None):
						complete_string=False
						break

					if chr in fmin_mapping.keys():

						map_chr=fmin_mapping[chr]

							#print("map_chr:"+str(map_chr))

						if map_chr in state.getTransitions().keys():
							state=state.move(map_chr)
						else:
							state=state.move("any_o")

					elif((self.__multiple_inputs) and (chr=="_")):

						if "_" in state.getTransitions().keys():
							state=state.move("_")
						else:
							state=state.move("any_o")
					else:
						if chr in state.getTransitions().keys():
							state=state.move(chr)
						else:
							additional_trans_keys=[]
							for st_trans_k in state.getTransitions().keys():

								# if ((st_trans_k not in fmin_mapping.values()) and (st_trans_k!="any_o") and (self.__multiple_inputs and st_trans_k!="_")):
								# 	print("reached:"+st_trans_k)
								# 	additional_trans_keys.append(st_trans_k)

								if(self.__multiple_inputs):
									if ((st_trans_k not in fmin_mapping.values()) and (st_trans_k!="any_o") and (st_trans_k!="_")):
										#print("reached-C")
										additional_trans_keys.append(st_trans_k)
								else:
									if ((st_trans_k not in fmin_mapping.values()) and (st_trans_k!="any_o")):
										additional_trans_keys.append(st_trans_k)
										#print("reached-D")


							if(len(additional_trans_keys)==0):
								state=state.move("any_o")
							else:
								rand_trans=np.random.choice(additional_trans_keys)
								state=state.move(rand_trans)

					if(state is None):
						break

				if ((state is not None) and (state.isFinal()) and (complete_string)):
					#print("True : sss")
					return True

		return False


	def __check_linear_eligibility(self,input_str,per_list):

		sub_str=input_str

		for per_it in per_list:

			i_str=sub_str.find(per_it)

			if i_str==-1:
				return False
			
			sub_str=sub_str[i_str+1:]

		return True



	def isAcceptingDup(self,input_str):
		char_list=collections.Counter(self.__fmin)
		input_char_list=collections.Counter(input_str)
		#eligible_list={}	

		#print("input char list:"+str(input_char_list))
		if(self.__multiple_inputs):
			del char_list["_"]
			del input_char_list["_"]


		#print("initial char list:"+str(char_list))
		#print("input char_list"+str(input_char_list))
		
		if(self.__fmin_assignment=="All"):

			#print("eligible_list:"+str(self.get_eligible_character_combiations(char_list.values(),input_char_list)))

			#print("**************************reached********************************")

			#per_element_list=itertools.permutations(list(input_char_list.keys()),len(char_list.keys()))
			per_element_list=self.get_eligible_character_combiations(char_list.values(),input_char_list)

			if per_element_list is None:
				return False

			#print(list(per_element_list))

			for ele in per_element_list:

				per_list=list(ele)

				#print(per_list)

				if (per_list in self.__neg_fmin_assignment):
					continue

				freq_list=list(char_list.values())
				#print("freq list:"+str(freq_list))

				if((" " in char_list.keys()) and (" " not in per_list)):
					continue

				all_eligible=True

				for pl_i in range(len(per_list)):
					if(input_char_list[per_list[pl_i]] < freq_list[pl_i]):
						all_eligible=False
						break


				fmin_mapping={}

				if(all_eligible):
					#print(per_list)
					fmin_idx=1
					for el_c in per_list:
						fmin_mapping[el_c]="all_fmin"+str(fmin_idx)
						fmin_idx+=1

					#print(fmin_mapping)

					dfa_start_state=self.__dfa.get_start_state()

					state=dfa_start_state
					complete_string=True


					for chr in input_str:


						if(state.getTransitions() is None):
							complete_string=False
							break

						if chr in fmin_mapping.keys():

							map_chr=fmin_mapping[chr]

							#print("map_chr:"+str(map_chr))

							if map_chr in state.getTransitions().keys():
								state=state.move(map_chr)
							else:
								state=state.move("any_o")

						elif((self.__multiple_inputs) and (chr=="_")):

							if "_" in state.getTransitions().keys():
								state=state.move("_")
							else:
								state=state.move("any_o")
						else:
							if chr in state.getTransitions().keys():
								state=state.move(chr)
							else:

								additional_trans_keys=[]
								for st_trans_k in state.getTransitions().keys():
									if ((st_trans_k not in fmin_mapping.values()) and (st_trans_k!="any_o") and (self.__multiple_inputs and st_trans_k!="_")):
										#print("reached:"+st_trans_k)
										additional_trans_keys.append(st_trans_k)

								if(len(additional_trans_keys)==0):
									state=state.move("any_o")
								else:
									rand_trans=np.random.choice(additional_trans_keys)
									state=state.move(rand_trans)


						if(state is None):
							#print("None state reached...")
							break


					if ((state is not None) and (state.isFinal()) and (complete_string)):
						#print("True : sss")
						return True
		else:

			for char_comb in self.__fmin_assignment:
				fmin_idx=1

				fmin_mapping={}

				for comb_c in char_comb:
					fmin_mapping[comb_c]="all_fmin"+str(fmin_idx)
					fmin_idx+=1

				#print(fmin_mapping)

				dfa_start_state=self.__dfa.get_start_state()

				state=dfa_start_state
				complete_string=True
		
				for chr in input_str:

					if(state.getTransitions() is None):
						complete_string=False
						break

					if chr in fmin_mapping.keys():

						map_chr=fmin_mapping[chr]

							#print("map_chr:"+str(map_chr))

						if map_chr in state.getTransitions().keys():
							state=state.move(map_chr)
						else:
							state=state.move("any_o")

					elif((self.__multiple_inputs) and (chr=="_")):

						if "_" in state.getTransitions().keys():
							state=state.move("_")
						else:
							state=state.move("any_o")
					else:
						if chr in state.getTransitions().keys():
							state=state.move(chr)
						else:
							additional_trans_keys=[]
							for st_trans_k in state.getTransitions().keys():
								if ((st_trans_k not in fmin_mapping.values()) and (st_trans_k!="any_o") and (self.__multiple_inputs and st_trans_k!="_")):
									#print("reached:"+st_trans_k)
									additional_trans_keys.append(st_trans_k)

							if(len(additional_trans_keys)==0):
								state=state.move("any_o")
							else:
								rand_trans=np.random.choice(additional_trans_keys)
								state=state.move(rand_trans)

					if(state is None):
						break

				if ((state is not None) and (state.isFinal()) and (complete_string)):
					#print("True : sss")
					return True

		return False


	def get_eligible_character_combiations(self,min_freq_list,input_unique_char_list):
		
		eligible_list=[]
		chr_list_counter=[]
		chr_list_sizes=[]

		min_freq_list=list(min_freq_list)
		min_freq_list.sort(reverse=True)

		for c_freq in min_freq_list:
			el_chars=[]
			for unique_char_key in input_unique_char_list.keys():
				if(c_freq <= input_unique_char_list[unique_char_key]):
					el_chars.append(unique_char_key)

			chr_list_counter.append(0)
			chr_list_sizes.append(len(el_chars))		
			eligible_list.append(el_chars)
			
		#print("min_freq_list:"+str(min_freq_list))
		#print("eligible_list_i:"+str(eligible_list))


		if(all([len(el_c)>0 for el_c in eligible_list])):
			
			char_combinations=[]

			while(chr_list_counter[0]<len(eligible_list[0])):
				
				comb=[]

				for el_i in range(len(min_freq_list)):

					selected_char=eligible_list[el_i][chr_list_counter[el_i]]	

					if selected_char not in comb:
						comb.append(selected_char)
					else:
						comb=[]
						break

				if(len(comb)!=0):
					char_combinations.append(comb)

				#print("char combinations:"+str(char_combinations))
				#print("chr list counter:"+str(chr_list_counter))

				isIncrement_next=True

				for r_el_i in range(len(min_freq_list)-1,-1,-1):
					
					if(isIncrement_next):

						next_idx=chr_list_counter[r_el_i]+1

						if((next_idx==chr_list_sizes[r_el_i]) and (r_el_i!=0)):
							chr_list_counter[r_el_i]=0
							isIncrement_next=True
						else:
							chr_list_counter[r_el_i]=next_idx
							isIncrement_next=False

			if (len(char_combinations)!=0):
				return char_combinations
			else:
				return None

		else:
			return None


		#cartesian_comb=itertools.product(*eligible_list)

		# el_combs=[]

		# for car_c in cartesian_comb:

		# 	print(car_c)

		# 	if(len(list(car_c))==len(list(set(car_c)))):
		# 		el_combs.append(car_c)

	def pick_element(self,el_chars,el_idx):
		return 	el_chars[el_idx]


	def unique_cartesian_product(self,*args):

		pools=[pool for pool in args]

		#print("pools:"+str(pools))

		result=[[]]

		for pool in pools:
			#result=[x+[y] for x in result for y in pool if y not in x]

			for x in result:
				for y in pool:
					if y not in x:
						result=[x+[y]]
			#print("r"+str(result))

		return result




	def merge_new_dfa_parser(self,new_dfa_parser):

		new_dfa=copy.deepcopy(new_dfa_parser.getDFA())

		initial_state_list=self.__dfa.get_state_list()

		max_state_index=max([int(st_k[1:]) for st_k in initial_state_list.keys() if st_k !="S"])

		#print("max state index:"+str(max_state_index))

		new_index=max_state_index+1

		new_state_list={}

		for new_st_key,new_st_val in new_dfa.get_state_list().items():

			if(new_st_key!="S"):
				new_state_name="q"+str(new_index)
				new_st_val.name=new_state_name
				new_state_list[new_state_name]=new_st_val
				new_index+=1
			else:
				new_state_list["S"]=new_st_val

		new_dfa.set_state_list(new_state_list)

		#print("new state list:"+str(new_dfa.get_state_list()))

		DFA.rpni_fold(self.__dfa.get_start_state(),new_state_list["S"])

		new_state_list_n=DFA.findStates(self.__dfa.get_start_state())


		for n_state in new_state_list_n:
			if n_state not in initial_state_list.keys():
				#print("newly added state:"+str(n_state))
				initial_state_list[n_state]=new_state_list[n_state]

		fmin_list=self.__fmin_assignment

		#print("fmin_list:"+str(fmin_list))

		if((fmin_list!="All") and (new_dfa_parser.getfmin_assignment()!="All")):

			new_assignments=new_dfa_parser.getfmin_assignment()

			for n_assign in new_assignments:
				#print("n_assign:"+str(n_assign))

				if(n_assign not in fmin_list):
					fmin_list.append(n_assign)


		#self.__dfa.get_state_list().update(new_state_list)










		