# GRAMMAR2FIX
GRAMMAR2FIX is an active oracle learning technique for programs taking string inputs. Given a single failing input of a bug, it learns a grammar describing the pattern of all the failing inputs of the bug, interacting with a bug oracle systematically. GRAMMAR2FIX returns this grammar as a collection of Deterministic Finite Automata(DFA), and the grammar can serve as an automated test oracle for the bug. GRAMMAR2FIX also produces a test suite in grammar learning, which can be used as a repair test suite in Automated Program Repair.

GRAMMAR2FIX is implemented in Python. The following benchmarks are used in the experiments.

* <a href="https://github.com/jkoppel/QuixBugs">QuixBugs</a>
* <a href="https://github.com/ProgramRepair/IntroClass">IntroClass</a>
* <a href="https://github.com/codeflaws/codeflaws">Codeflaws</a>

GenProg (<a href="https://ieeexplore.ieee.org/document/6035728">Paper</a>, <a href="https://github.com/squaresLab/genprog-code">Tool</a>) is used as the automated program repair tool.

# How to run GRAMMAR2FIX



## Setup GenProg
```
docker pull squareslab/genprog
docker run -it squareslab/genprog /bin/bash
```
