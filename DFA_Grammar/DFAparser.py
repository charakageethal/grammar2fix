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

		if(self.__multiple_inputs):
			del char_list["_"]
			del input_char_list["_"]

		if(self.__fmin_assignment=="All"):
			comb_element_list=itertools.combinations(list(input_char_list.keys()),len(char_list.keys()))
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
							fmin_idx=1
							for el_c in per_list:
								fmin_mapping[el_c]="all_fmin"+str(fmin_idx)
								fmin_idx+=1

							dfa_start_state=self.__dfa.get_start_state()
							state=dfa_start_state
							complete_string=True

							for chr in input_str:
								if(state.getTransitions() is None):
									complete_string=False
									break

								if chr in fmin_mapping.keys():
									map_chr=fmin_mapping[chr]
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
											if(self.__multiple_inputs):
												if ((st_trans_k not in fmin_mapping.values()) and (st_trans_k!="any_o") and (st_trans_k!="_")):
													additional_trans_keys.append(st_trans_k)
											else:
												if ((st_trans_k not in fmin_mapping.values()) and (st_trans_k!="any_o")):
													additional_trans_keys.append(st_trans_k)

										if(len(additional_trans_keys)==0):
											state=state.move("any_o")
										else:
											rand_trans=np.random.choice(additional_trans_keys)
											state=state.move(rand_trans)

								if(state is None):
									break
							if ((state is not None) and (state.isFinal()) and (complete_string)):
								return True
		else:
			for char_comb in self.__fmin_assignment:
				fmin_idx=1
				fmin_mapping={}

				for comb_c in char_comb:
					fmin_mapping[comb_c]="all_fmin"+str(fmin_idx)
					fmin_idx+=1

				dfa_start_state=self.__dfa.get_start_state()
				state=dfa_start_state
				complete_string=True
		
				for chr in input_str:
					if(state.getTransitions() is None):
						complete_string=False
						break

					if chr in fmin_mapping.keys():
						map_chr=fmin_mapping[chr]
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
								if(self.__multiple_inputs):
									if ((st_trans_k not in fmin_mapping.values()) and (st_trans_k!="any_o") and (st_trans_k!="_")):
										additional_trans_keys.append(st_trans_k)
								else:
									if ((st_trans_k not in fmin_mapping.values()) and (st_trans_k!="any_o")):
										additional_trans_keys.append(st_trans_k)
										
							if(len(additional_trans_keys)==0):
								state=state.move("any_o")
							else:
								rand_trans=np.random.choice(additional_trans_keys)
								state=state.move(rand_trans)

					if(state is None):
						break

				if ((state is not None) and (state.isFinal()) and (complete_string)):
					return True

		return False

	# Check the order of the combination
	def __check_linear_eligibility(self,input_str,per_list):
		sub_str=input_str

		for per_it in per_list:
			i_str=sub_str.find(per_it)
			if i_str==-1:
				return False
			sub_str=sub_str[i_str+1:]

		return True










		