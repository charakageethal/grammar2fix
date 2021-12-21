from State import State
import copy

class DFA:

	def __init__(self):
		self.__start=State("S",isStart=True)
		self.__state_list={"S":self.__start}


	def gen_dfa(self,input_str_list):

		for input_str in input_str_list:

			if(self.__start.getTransitions() is None):

				q1=State("q1")
				self.__start.setTransitions({input_str[0]:q1})
				self.__state_list["q1"]=q1

				n_i=1
				if(len(input_str)>1):
					for chr in input_str[1:]:

						state_name="q"+str(n_i+1)

						if(n_i==len(input_str)-1):
							n_state=State(state_name,isFinal=True)

						else:
							n_state=State(state_name)
						
						self.__state_list["q"+str(n_i)].setTransitions({chr:n_state})
						self.__state_list[state_name]=n_state

						n_i+=1
				else:
					q1.setFinal(True)


			else:
				curr_state=self.__start

				no_states=False

				last_state_n=int(list(self.__state_list.keys())[-1][1:])


				input_chr_idx=0
				prev_state=curr_state
				for chr in input_str:
					curr_state=curr_state.move(chr)

					if(curr_state is None):
						no_states=True
						break
					else:
						if(input_chr_idx==len(input_str)-1):
							curr_state.setFinal(True)

					prev_state=curr_state
					input_chr_idx+=1

				if(no_states):

					remain_str=input_str[input_chr_idx:]

					n_i=last_state_n
				
					for chr in remain_str:

						state_name="q"+str(n_i+1)


						if(input_chr_idx==len(input_str)-1):
							n_state=State(state_name,isFinal=True)
						else:
							n_state=State(state_name)
						
						#self.__state_list["q"+str(n_i)].setTransitions({chr:n_state})


						state_transitions=prev_state.getTransitions()

						if(state_transitions is not None):
							state_transitions[chr]=n_state
						else:
							prev_state.setTransitions({chr:n_state})

						self.__state_list[state_name]=n_state

						prev_state=n_state

						n_i+=1
						input_chr_idx+=1


	def get_state_list(self):
		return self.__state_list

	def set_state_list(self,state_list):
		self.__state_list=state_list

	def get_start_state(self):
		return self.__start

	def set_start_state(self,start):
		self.__start=start

	def isAccepting(self,input_str):

		state=self.__start

		for chr in input_str:
			state=state.move(chr)

			if(state is None):
				return False

		if (state.isFinal()):
			return True
		else:
			return False

	def getAcceptingFinalState(self,input_str):

		state=self.__start

		for chr in input_str:
			#print("chr:"+chr)

			state=state.move(chr)
			#print(state.name)

			if(state is None):
				return None


		if(state.isFinal()):
			return state
		else:
			return None



	@classmethod
	def rpni_fold(cls,first_state,second_state):
	
		second_state_trans=second_state.getTransitions()

		if(second_state_trans is not None):

			for s_key in second_state_trans.keys():

				first_state_trans=first_state.getTransitions()

				if( (first_state_trans is not None) and (s_key in first_state_trans.keys())):


					if(second_state.isFinal()):
						first_state.setFinal(True)


					if((first_state_trans[s_key]=="self") and (second_state_trans[s_key]=="self")):
						continue

					cls.rpni_fold(first_state.move(s_key),second_state.move(s_key))

				else:
					first_state_trans=first_state.getTransitions()
					if(first_state_trans is None):
						new_state_trans={s_key:second_state_trans[s_key]}
						first_state.setTransitions(new_state_trans)
					else:
						first_state_trans[s_key]=second_state_trans[s_key]
		else:
			if(second_state.isFinal()):
				first_state.setFinal(True)



	@classmethod
	def isAllNegativeFail(cls,dfa,neg_samples):

		for ns in neg_samples:
			accept_state=dfa.isAccepting(ns)

			if(accept_state==True):
				return False

		return True


	@classmethod
	def findStates(cls,root):

		state_set=[root.name]

		state_trans=root.getTransitions()

		if state_trans is None:
			return list(set(state_set))
		else:
			for st_trans_key in state_trans.keys():

				if(state_trans[st_trans_key]=="self"):
					continue

				next_state=root.move(st_trans_key)
				state_set=list(set(state_set+cls.findStates(next_state)))

		return list(set(state_set))


	@classmethod
	#Perform modified RPNI merge
	def conv_rpni_merge(cls,init_dfa,neg_samples,f_min):
		
		further_merge=True
		dfa=init_dfa

		while(further_merge):

			found_new_dfa=False

			state_list=dfa.get_state_list()
			start_state=dfa.get_start_state()

			for st_name in state_list.keys():

				dup_dfa=copy.deepcopy(dfa)
				dup_state_list=dup_dfa.get_state_list()
				dup_state=dup_state_list[st_name]
				state_trans=copy.deepcopy(dup_state.getTransitions())

				if(state_trans is not None):
					for st_trans_key in state_trans.keys():

						if(st_trans_key in f_min):
							continue

						next_state=dup_state.move(st_trans_key)

						if(next_state.name==dup_state.name):
							continue

						if(next_state.isFinal()):
							dup_state.setFinal(True)	

						dup_state_trans=dup_state.getTransitions()
						dup_state_trans[st_trans_key]="self"

						cls.rpni_fold(dup_state,next_state)

						new_states=cls.findStates(dup_state_list["S"])

						new_states.sort()

						new_state_list={}

						for st_name in new_states:
							new_state_list[st_name]=dup_state_list[st_name]


						new_dfa=DFA()
						new_dfa.set_start_state(dup_state_list["S"])
						new_dfa.set_state_list(new_state_list)

						if(cls.isAllNegativeFail(dup_dfa,neg_samples)):
							dfa=new_dfa
							found_new_dfa=True
							break
				else:
					continue

				if(found_new_dfa):
					break

			if(not found_new_dfa):
				further_merge=False
	
		return dfa

