class State:

	def __init__(self,name,isStart=False,isFinal=False,transitions=None):

		self.__isStart=isStart
		self.__isFinal=isFinal
		self.__transitions=transitions
		self.name=name

	def isStart(self):
		return self.__isStart

	def isFinal(self):
		return self.__isFinal

	def setFinal(self,state_final):
		self.__isFinal=state_final

	def setTransitions(self,transitions):
		self.__transitions=transitions

	def getTransitions(self):
		return self.__transitions

	def move(self,trans_char):
		if((self.__transitions is not None) and (trans_char in self.__transitions)):
			if(self.__transitions[trans_char]=="self"):
				return self
			else:
				return self.__transitions[trans_char]
		else:
			return None

	def get_info(self):
		str_trainsitions="{"
		if self.__transitions is not None:
			for trans_key,trans_state in self.__transitions.items():
				if(trans_state=="self"):
					str_trainsitions+="'"+str(trans_key)+"': self,"
				else:
					str_trainsitions+="'"+str(trans_key)+"':"+trans_state.name+","
		else:
			str_trainsitions+="None,"
		return self.name+", IsAccepting:"+str(self.__isFinal)+", transitions:"+str_trainsitions[:-1]+"}"






