class DeltaMinimize:
	"""docstring for DeltaMinimize"""
	def __init__(self,test_prog,oracle_ob,mulitple_inputs):
		self.__prev_passing_test_cases=[]
		self.__prev_failing_test_cases=[]
		self.__passing_test_cases=[]
		self.__failing_test_cases=[]
		self.__passing_tcase_indexes=[]
		self.__failing_tcase_indexes=[]
		self.__n_human_labelled=0
		self.__multiple_inputs=mulitple_inputs
		self.__oracle_ob=oracle_ob
		self.__test_prog=test_prog



	def __create_subsets(self,char_index_list,n):
	    items_per_subset=round(len(char_index_list)/n)
	    start_index=0
	    end_index=start_index+items_per_subset
	    
	    new_subsets=[]
	    
	    while(start_index<len(char_index_list)):
	        new_subsets.append(char_index_list[start_index:end_index])
	        start_index=end_index
	        end_index+=items_per_subset

	    return new_subsets


	def __flattern_failure_minimized(self,minimized_indexes):
	    serialized_failure_minimized_indexes=[]
	    
	    for f_ids in minimized_indexes:
	        if type(f_ids) is list:
	            for f_id in f_ids:
	                serialized_failure_minimized_indexes.append(f_id)
	        else:
	            serialized_failure_minimized_indexes.append(f_ids)
	            
	    return serialized_failure_minimized_indexes

	    
	def __get_string(self,base_input,char_indexes):
	    new_string=""
	    
	    for c_i in char_indexes:
	        new_string+=base_input[c_i]
	        
	    return new_string


	def __ddmin(self,char_index_list,subject_string):
	    for char_indexes in char_index_list:
	        #print("Condition 01")
	        test_string=self.__get_string(subject_string,char_indexes)
	     
	        if (test_string in self.__passing_test_cases):
	        	continue

	        test_case=test_string.split('_')
	        if((self.__multiple_inputs==True) and (len(test_case)==1)):
	            test_case.append("")
	        
	        if(test_string in self.__failing_test_cases):
	        	human_label=False 
	        else:
	        	human_label=self.__oracle_ob.ask_human(test_case,self.__test_prog)
	        
	        if(not human_label):
	            #print("test case fail:"+str(test_case))  
	            if(char_indexes not in self.__failing_tcase_indexes):
	                self.__failing_tcase_indexes.append(char_indexes)
	            
	            if(test_string not in self.__failing_test_cases):
	            	self.__failing_test_cases.append(test_string)
	            
	            if(len(char_indexes)==1):
	                return char_indexes
	            
	            new_char_index_list=self.__create_subsets(char_indexes,2)
	            return self.__ddmin(new_char_index_list,subject_string)
	            break
	        else:
	            if(test_string not in self.__passing_test_cases):
	                self.__passing_test_cases.append(test_string)
	            
	            if(char_indexes not in self.__passing_tcase_indexes):
	                self.__passing_tcase_indexes.append(char_indexes)

	    
	    for i_char_index in range(len(char_index_list)):
	        char_complement_indexes=[]
	        for c_char_index in range(len(char_index_list)):
	            
	            if i_char_index==c_char_index:
	                continue
	            else:
	                char_complement_indexes+=char_index_list[c_char_index]
	         
	        test_string=self.__get_string(subject_string,char_complement_indexes)
	     
	        if (test_string in self.__passing_test_cases):
	        	continue
	        
	        test_case=test_string.split('_')
	        if((self.__multiple_inputs==True) and (len(test_case)==1)):
	            test_case.append("")

	        if(test_string in self.__failing_test_cases):
	        	human_label=False
	        else:
	        	human_label= self.__oracle_ob.ask_human(test_case,self.__test_prog)


	        if(not human_label):
	            if(test_string not in self.__failing_test_cases):
	                self.__failing_test_cases.append(test_string)
	                
	            if(char_complement_indexes not in self.__failing_tcase_indexes):
	                self.__failing_tcase_indexes.append(char_complement_indexes)
	            
	            subset_size=max(len(char_index_list)-1,2)
	            
	            if(len(char_complement_indexes)<subset_size):
	                return char_complement_indexes
	            
	            new_char_index_list=self.__create_subsets(char_complement_indexes,subset_size)
	            return self.__ddmin(new_char_index_list,subject_string)
	            break
	        else:
	            if(test_string not in self.__passing_test_cases):
	                self.__passing_test_cases.append(test_string)
	                
	            if(char_complement_indexes not in self.__passing_tcase_indexes):
	                self.__passing_tcase_indexes.append(char_complement_indexes)
	     
	    truncated_string=""
	    
	    for c_idx in char_index_list:
	        for cid in c_idx:
	            truncated_string+=subject_string[cid]
	     
	    if(len(char_index_list)<len(truncated_string)):
	        subset_size=min(len(truncated_string),2*len(char_index_list))
	        new_merge_list=[]
	        
	        for char_idx in char_index_list:
	            new_merge_list+=char_idx

	        new_char_index_list=self.__create_subsets(new_merge_list,subset_size)
	        return self.__ddmin(new_char_index_list,subject_string)
	    else:
	        return char_index_list



	def find_minimize_input(self,failure_input):
		self.__passing_tcase_indexes=[]
		self.__failing_tcase_indexes=[]
		self.__passing_test_cases=[]
		self.__failing_test_cases=[]		

		char_index_list=[i for i in range(len(failure_input))]

		minimized_indexes=self.__flattern_failure_minimized(self.__ddmin([char_index_list],failure_input))

		minimized_failure_string=self.__get_string(failure_input,minimized_indexes)

		return minimized_failure_string,self.__passing_test_cases,self.__failing_test_cases



