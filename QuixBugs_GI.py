import sys
sys.path.insert(0,"DFA_Grammar")
sys.path.insert(0,"Drivers")

from DFA_Grammar.State import State
from Drivers.QuixbugsDriver import QuixbugsDriver
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
parser.add_argument("-s","--subject",help="Buggy Subject",required=True)
parser.add_argument("-p","--path",help="path to QuixBugs",required=True)
parser.add_argument("-i","--iteration",help="iteration",default=1,type=int)
parser.add_argument("-d","--debug",help="Enable Debug",action="store_true")
args=parser.parse_args()

iteration=args.iteration
bug_path=args.path
debug=args.debug
buggy_subject=args.subject

multiple_inputs=False

q_driver=QuixbugsDriver(bug_path)
prog_name=buggy_subject

test_cases=q_driver.get_test_cases(prog_name)
test_case_labels=np.array([q_driver.ask_human(t[0],prog_name) for t in test_cases])

if np.sum(test_case_labels) == test_case_labels.size:
    sys.exit("[Error:"+prog_name+"] No failing test cases")

failing_indexes=np.nonzero(test_case_labels==False)[0]   
trainer_test_suite=[test_cases[np.random.choice(failing_indexes)]] 
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

q_driver.set_human_labelled_zero()

ddmin=DeltaMinimize(prog_name,q_driver,multiple_inputs)

fmin,inter_passing_tcases,inter_failing_tcases=ddmin.find_minimize_input(trainer_input)

init_dfa=DFA()
init_dfa.gen_dfa(inter_failing_tcases)

parser=DFA.conv_rpni_merge(init_dfa,inter_passing_tcases,fmin)

if debug:
    print("****************Basic Level Grammar**************************")
    states_GI_parser=parser.get_state_list()
    for st_v in states_GI_parser.values():
        print(st_v.get_info())
    print("*****************************************************************")

n_human_labelled,human_labelled_passing,human_labelled_failing=q_driver.get_human_labelled()
if debug: print("Number of human queries:"+str(n_human_labelled))
if debug: print("\nhuman labelled passing:"+str(sorted(human_labelled_passing))+"-"+str(len(human_labelled_passing)))
if debug: print("\nhuman labelled failing:"+str(sorted(human_labelled_failing))+"-"+str(len(human_labelled_failing)))

q_driver.set_human_labelled_zero()

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

print(prog_name+","+str(iteration)+","+str(len(test_case_labels))+","+str(n_correct)+","+str(n_fail)+","+str(n_fail_correct)+","+str(n_pass)+","+str(n_pass_correct)+","+str(n_human_labelled))
