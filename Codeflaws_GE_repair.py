import sys
sys.path.insert(0,"DFA_Grammar")
sys.path.insert(0,"Drivers")
sys.path.insert(0,"Utils")

from DFA_Grammar.State import State
from Drivers.CodeflawsDriver import CodeflawsDriver
from Utils.DeltaMinimize import DeltaMinimize
from Utils.HSCFuzzer import HSCFuzzer
from Utils.CharacterFuzz import CharacterFuzz
from DFA_Grammar.DFA import DFA
from DFA_Grammar.DFAparser import DFAparser
import numpy as np
import collections
from string import printable
import argparse
from decimal import Decimal,DecimalException
import random
import subprocess
import string
import copy
import os
import glob


parser=argparse.ArgumentParser()
parser.add_argument("-s","--subject",help="Buggy Subject",required=True)
parser.add_argument("-p","--path",help="path to codeflaws",required=True)
parser.add_argument("-i","--iteration",help="iteration",default=1,type=int)
parser.add_argument("-d","--debug",help="Enable Debug",action="store_true")
args=parser.parse_args()

iteration=args.iteration
bug_path=args.path
debug=args.debug
buggy_subject=args.subject


def custom_mutations(input_val):
    mutate_functions=["delete_random_character","insert_random_character","shuffle_random_character"]
    
    def delete_random_character(s):
        if s == "":
            return s
        pos = np.random.randint(0, len(s) - 1)
        return s[:pos] + s[pos + 1:]
    
    def insert_random_character(s):
        pos = np.random.randint(0, len(s))
        random_character = random.choice(string.ascii_uppercase+string.digits+string.ascii_lowercase+"()")
        return s[:pos] + random_character + s[pos:]
    
    def shuffle_random_character(s):
        chr_list=list(s)
        random.shuffle(chr_list)
        return "".join(chr_list)
    
    stack_size=np.random.randint(low=1,high=20)
    random_ops=random.choices(mutate_functions,k=stack_size)

    for op in random_ops:
        input_val=locals()[op](input_val)
      
    return input_val
    
def get_mutated_testcase(test_suite,seed_input):
    while True:
        mutated_input=[]
        for s_in in seed_input:
            searchAgain=True
        
            while(searchAgain):
                output_mutated=""
                try:
                    output_mutated=custom_mutations(s_in)
                except:
                    output_mutated=""
                    searchAgain=True
                    continue
                if(set(output_mutated).difference(printable)):
                    continue
                else:
                    searchAgain=False
                mutated_input.append(output_mutated)
                
        no_duplicate=True
        
        for tcase in test_suite:
            if all(ti in tcase[0] for ti in mutated_input):
                no_duplicate=False
                break
        if no_duplicate:
            return mutated_input

def get_no_trans_longest_strings(final_no_trans_states,inter_failing_tcases):
    longest_accepting={}

    for fn_state in final_no_trans_states:
        longest_accepting[fn_state.name]=""

    for inter_ftcase in inter_failing_tcases:
        stop_state=abs_dfa.getAcceptingFinalState(inter_ftcase)
        if(stop_state is not None):
            if stop_state in final_no_trans_states:
                if(len(longest_accepting[stop_state.name])<len(inter_ftcase)):
                    longest_accepting[stop_state.name]=inter_ftcase

    return longest_accepting

def evaluate_tcase(parser_list,test_input):
    for parser in parser_list:
        if(parser.isAccepting(test_input)):
            return False

    return True

def findReplacable(ftcase_fmins,new_fmin,multiple_inputs):
    new_fmin_freq_list=collections.Counter(new_fmin)

    if(multiple_inputs):
        del new_fmin_freq_list["_"]

    for ft_min in ftcase_fmins.keys():
        if (ftcase_fmins[ft_min][0]=="All"):
            ft_min_freq_list=collections.Counter(ft_min)

            if(multiple_inputs):
                del ft_min_freq_list["_"]

            if(list(new_fmin_freq_list.values())==list(ft_min_freq_list.values())):
                char_pos_list={}
        
                for k in new_fmin_freq_list.keys():
                    char_pos_list[k]=[i for i in range(len(new_fmin)) if new_fmin[i]==k]

                new_fmin_list=list(new_fmin)
                new_fmin_freq_key_list=list(new_fmin_freq_list.keys())
                ft_min_freq_key_list=list(ft_min_freq_list.keys())

                for i_ft_min_keys in range(len(ft_min_freq_key_list)):
                    for char_pos in char_pos_list[new_fmin_freq_key_list[i_ft_min_keys]]:
                        new_fmin_list[char_pos]=ft_min_freq_key_list[i_ft_min_keys]

                assigned_fmin="".join(new_fmin_list)

                if(assigned_fmin==ft_min):
                    return ft_min
    return None

multiple_inputs=False
parser_list=[]

c_driver=CodeflawsDriver(bug_path)
bug_dir=buggy_subject

test_cases=c_driver.get_test_cases(bug_dir)
test_case_labels=np.array([c_driver.ask_human(t[0],bug_dir) for t in test_cases])

if np.sum(test_case_labels) == test_case_labels.size:
    sys.exit("[Error:"+bug_dir+"] No failing test cases")

failing_indexes=np.nonzero(test_case_labels==False)[0]   
trainer_test_suite=[test_cases[np.random.choice(failing_indexes)]] # skipping the longer one
trainer_labels=np.array([False])
mutated_failing=[trainer_test_suite[0]]

trainer_input=""

if (len(trainer_test_suite[0][0])>1):
    multiple_inputs=True
    for i_str in trainer_test_suite[0][0]:
        trainer_input+=i_str+"_"

    trainer_input=trainer_input[:-1]
else:
    trainer_input=trainer_test_suite[0][0][0]

c_driver.set_human_labelled_zero()

ddmin=DeltaMinimize(bug_dir,c_driver,multiple_inputs)
charfuzz=CharacterFuzz(c_driver,bug_dir,multiple_inputs)
hscfuzz=HSCFuzzer(c_driver,bug_dir,multiple_inputs)

fmin,inter_passing_tcases,inter_failing_tcases=ddmin.find_minimize_input(trainer_input)
fmin_freq_list=collections.Counter(fmin)

if(multiple_inputs):
    del fmin_freq_list["_"]

F_A=[list(fmin_freq_list.keys())]

init_dfa=DFA()
init_dfa.gen_dfa(inter_failing_tcases)

abs_dfa=DFA.conv_rpni_merge(init_dfa,inter_passing_tcases,fmin)

if debug:
    print("****************Basic Level Grammar**************************")
    states_GI_parser=abs_dfa.get_state_list()
    for st_v in states_GI_parser.values():
        print(st_v.get_info())
    print("*****************************************************************")

parser=DFAparser(F_A,copy.deepcopy(abs_dfa),fmin,multiple_inputs)

if debug:
    print("\n**********************After BG*************************")
    states_BG_parser=parser.getDFAStateList()
    for st_v in states_BG_parser.values():
        print(st_v.get_info())
    print("*****************************************************************")

st_list=abs_dfa.get_state_list()
final_no_trans_states=[st for st in st_list.values() if (st.isFinal() and (st.getTransitions() is None)) ]

hscfuzz.prefix_fuzz(parser,inter_failing_tcases[0])

if(len(final_no_trans_states)>0):
    longest_accepting=get_no_trans_longest_strings(final_no_trans_states,inter_failing_tcases)
    hscfuzz.suffix_fuzz(parser,longest_accepting)

if debug:
    print("\n**********************After HCS*************************")
    states_HSC_ftparser=parser.getDFAStateList()
    for st_v in states_HSC_ftparser.values():
        print(st_v.get_info())
    print("*****************************************************************")

if fmin!=" ":
    F_A_neg=charfuzz.get_character_class(fmin)
    if F_A_neg=="All_pass":
        parser.setfmin_assignment(F_A)
    else:
        F_A="All"
        parser.setfmin_assignment(F_A)
        parser.set_negfmin_assignment(F_A_neg)
else:
    parser.setfmin_assignment(F_A)


parser_list.append(parser)
secondary_failing_tcases=[inter_failing_tcases[0]]
ftcase_fmins={fmin:[parser.getfmin_assignment(),parser.get_neg_fmin_assignment()]}

if debug:print("\nGrammar Extension\n")

for fuzz_i in range(5):
    f_tcase=random.choice(secondary_failing_tcases)

    if(multiple_inputs):
        tcase=f_tcase.split("_")
        secondary_raw_tcases=[[ft.split("_")] for ft in secondary_failing_tcases]
    else:
        tcase=[f_tcase]
        secondary_raw_tcases=[[ft] for ft in secondary_failing_tcases]

    mutated_test_input=get_mutated_testcase(secondary_raw_tcases,tcase)
    format_test_input=""
     
    for m_str in mutated_test_input:
        format_test_input+=m_str+"_" 

    format_test_input=format_test_input[:-1]    

    if(evaluate_tcase(parser_list,format_test_input)):
        mutated_test_output=c_driver.run_test(bug_dir,*copy.deepcopy(mutated_test_input))
        mutated_test_case=[mutated_test_input,mutated_test_output]
        sec_human_label=c_driver.ask_human(mutated_test_case[0],bug_dir)
        if(not sec_human_label):
            new_ft=""

            for m_str in mutated_test_input:
                new_ft+=m_str+"_"

            new_ft=new_ft[:-1]

            secondary_failing_tcases.append(new_ft)
            sec_fmin,inter_sec_passing_tcases,inter_sec_failing_tcases = ddmin.find_minimize_input(new_ft)
            sec_fmin_freq_list=collections.Counter(sec_fmin)

            if(multiple_inputs):
                del sec_fmin_freq_list["_"]

            sec_F_A=[list(sec_fmin_freq_list.keys())]

            sec_dfa=DFA()
            sec_dfa.gen_dfa(inter_sec_failing_tcases)
            sec_abs_dfa=DFA.conv_rpni_merge(sec_dfa,inter_sec_passing_tcases,sec_fmin)

            if debug:
                print("****************GE-Basic Level Grammar**************************")
                states_GI_parser=sec_abs_dfa.get_state_list()
                for st_v in states_GI_parser.values():
                    print(st_v.get_info())
                print("*****************************************************************")

            sec_parser=DFAparser(sec_F_A,copy.deepcopy(sec_abs_dfa),sec_fmin,multiple_inputs)

            if debug:
                print("\n**********************GE-After BG*************************")
                states_BG_parser=sec_parser.getDFAStateList()
                for st_v in states_BG_parser.values():
                    print(st_v.get_info())
                print("*****************************************************************")

            st_list=sec_abs_dfa.get_state_list()
            sec_final_no_trans_states=[st for st in st_list.values() if (st.isFinal() and (st.getTransitions() is None)) ]

            hscfuzz.prefix_fuzz(sec_parser,inter_sec_failing_tcases[0])

            if(len(sec_final_no_trans_states)>0):
                sec_longest_accepting=get_no_trans_longest_strings(sec_final_no_trans_states,inter_sec_failing_tcases)
                hscfuzz.suffix_fuzz(sec_parser,sec_longest_accepting)

            if debug:
                print("\n**********************GE-After HCS*************************")
                states_HSC_ftparser=sec_parser.getDFAStateList()
                for st_v in states_HSC_ftparser.values():
                    print(st_v.get_info())
                print("*****************************************************************")

            replacable_fmin=findReplacable(ftcase_fmins,sec_fmin,multiple_inputs)

            if sec_fmin in ftcase_fmins.keys():
                sec_parser.setfmin_assignment(ftcase_fmins[sec_fmin][0])
                sec_parser.set_negfmin_assignment(ftcase_fmins[sec_fmin][1])

            elif (replacable_fmin is not None):
                sec_parser.setfmin_assignment(ftcase_fmins[replacable_fmin][0])
                sec_parser.set_negfmin_assignment(ftcase_fmins[replacable_fmin][1])                    

            elif sec_fmin!=" ":
                sec_F_A_neg=charfuzz.get_character_class(sec_fmin)
                if sec_F_A_neg=="All_pass":
                    sec_parser.setfmin_assignment(sec_F_A)
                else:
                    sec_F_A="All"
                    sec_parser.setfmin_assignment(sec_F_A)
                    sec_parser.set_negfmin_assignment(sec_F_A_neg)
                ftcase_fmins[sec_fmin]=[sec_parser.getfmin_assignment(),sec_parser.get_neg_fmin_assignment()]
            else:
                sec_parser.setfmin_assignment(sec_F_A)
                ftcase_fmins[sec_fmin]=[sec_parser.getfmin_assignment(),sec_parser.get_neg_fmin_assignment()]

            parser_list.append(sec_parser)        

n_human_labelled,human_labelled_passing,human_labelled_failing=c_driver.get_human_labelled()
if debug: print("Number of human queries:"+str(n_human_labelled))
if debug: print("\nhuman labelled passing:"+str(sorted(human_labelled_passing))+"-"+str(len(human_labelled_passing)))
if debug: print("\nhuman labelled failing:"+str(sorted(human_labelled_failing))+"-"+str(len(human_labelled_failing)))
 
if debug:
    print("\nparser list grammar - After Grammar Extension")
    for parser in parser_list:
        s_ftparser=parser.getDFAStateList()
        for st_v in s_ftparser.values():
            print(st_v.get_info())
        print("*****************************************************************")            

c_driver.set_human_labelled_zero()

predicted_labels=[]

for t_case in test_cases:
    t_case_input=""

    for t_in in t_case[0]:
        t_case_input+=t_in+"_"

    t_case_input=t_case_input[:-1] 
    predicted_labels.append(evaluate_tcase(parser_list,t_case_input))

if debug: print("predicted_labels:"+str(np.array(predicted_labels)))
if debug: print("actual labels:"+str(test_case_labels))

n_fail=0
n_pass=0
n_correct=0
n_fail_correct=0
n_pass_correct=0


for i_tcase_label in range(len(test_case_labels)):
    if(test_case_labels[i_tcase_label]==False):
        n_fail+=1
    else:
        n_pass+=1

    if(test_case_labels[i_tcase_label]==predicted_labels[i_tcase_label]):
        n_correct+=1

        if(predicted_labels[i_tcase_label]==False):
            n_fail_correct+=1
        else:
            n_pass_correct+=1

print(bug_dir+","+str(iteration)+","+str(len(test_case_labels))+","+str(n_correct)+","+str(n_fail)+","+str(n_fail_correct)+","+str(n_pass)+","+str(n_pass_correct)+","+str(n_human_labelled))

#Repair test suite generation
autogen_files=glob.glob(bug_path+"/"+bug_dir+"/"+"autogen-"+str(iteration)+"-*",recursive=False)

for f in autogen_files:
    os.remove(f)

p_index=0
n_index=0

autogen_fname_prefix=bug_path+"/"+bug_dir+"/autogen-"+str(iteration)

for ptcase in human_labelled_passing:
    p_index+=1
    autogen_fname=autogen_fname_prefix+"-p"+str(p_index)
    test_case_input=ptcase[0]

    with open(autogen_fname,"w+") as autogen_file:
        autogen_file.write(test_case_input+"\n")

for ntcase in human_labelled_failing:
    n_index+=1
    autogen_fname=autogen_fname_prefix+"-n"+str(n_index)
    test_case_input=ntcase[0]

    with open(autogen_fname,"w+") as autogen_file:
        autogen_file.write(test_case_input+"\n")
