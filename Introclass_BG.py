import sys
sys.path.insert(0,"DFA_Grammar")
sys.path.insert(0,"Drivers")

from DFA_Grammar.State import State
from Drivers.IntroClassDriver import IntroClassDriver
from DeltaMinimize import DeltaMinimize
from CharacterFuzz import CharacterFuzz
from DFA_Grammar.DFA import DFA
from DFA_Grammar.DFAparser import DFAparser
from HSCFuzzer import HSCFuzzer
import numpy as np
import collections
from string import printable
import argparse
from decimal import Decimal,DecimalException
import random
import subprocess
import string
import copy

parser=argparse.ArgumentParser()
parser.add_argument("-s","--subject",help="path to buggy subjects",required=True)
parser.add_argument("-i","--iteration",help="iteration",default=1,type=int)
parser.add_argument("-g","--golden_version",help="path to the golden version", required=True)
parser.add_argument("-d","--debug",help="Enable Debug",action="store_true")
args=parser.parse_args()

iteration=args.iteration
bug_dir=args.subject
debug=args.debug
path_golden=args.golden_version.rstrip('/')
test_prog_name=path_golden.split('/')[-2]

prog_name=bug_dir+"/"+test_prog_name


multiple_inputs=False
prog_name=bug_dir+"/"+test_prog_name

i_driver=IntroClassDriver(path_golden)
test_cases=i_driver.get_test_cases()

if len(test_cases)==0:
    sys.exit("[Error:"+prog_name+"No artificial test cases]")

test_case_labels=np.array([i_driver.ask_human(t[0],prog_name) for t in test_cases])

#Checking for fleaky subjects:
for i in range(5):
    fleaky_test_labels=np.array([i_driver.ask_human(t[0],prog_name) for t in test_cases])
    if(not np.array_equal(test_case_labels,fleaky_test_labels)):
        sys.exit("Removing fleaky output subject")

if np.sum(test_case_labels) == test_case_labels.size:
    sys.exit("[Error:"+prog_name+"] No failing test cases")

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
    trainer_input=trainer_test_suite[0][0][0]

i_driver.set_human_labelled_zero()

ddmin=DeltaMinimize(prog_name,i_driver,multiple_inputs)

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

n_human_labelled,human_labelled_passing,human_labelled_failing=i_driver.get_human_labelled()
if debug: print("Number of human queries:"+str(n_human_labelled))
if debug: print("\nhuman labelled passing:"+str(sorted(human_labelled_passing))+"-"+str(len(human_labelled_passing)))
if debug: print("\nhuman labelled failing:"+str(sorted(human_labelled_failing))+"-"+str(len(human_labelled_failing)))

i_driver.set_human_labelled_zero()

predicted_labels=[]

for t_case in test_cases:
    t_case_input=""

    for t_in in t_case[0]:
        t_case_input+=t_in+"_"

    t_case_input=t_case_input[:-1] 
    predicted_labels.append(not parser.isAccepting(t_case_input))

if debug: print("\npredicted_labels:"+str(np.array(predicted_labels)))
if debug: print("actual labels:"+str(test_case_labels)+"\n")

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


print(bug_dir.split('/')[-3]+","+bug_dir.split('/')[-2]+","+bug_dir.split('/')[-1]+","+str(iteration)+","+str(len(test_case_labels))+","+str(n_correct)+","+str(n_fail)+","+str(n_fail_correct)+","+str(n_pass)+","+str(n_pass_correct)+","+str(n_human_labelled))

        


