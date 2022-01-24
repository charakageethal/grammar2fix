# grammar2fix
GRAMMAR2FIX is an active oracle learning technique for programs taking string inputs. Given a single failing input of a bug, it learns a grammar describing the pattern of all the failing inputs of the bug, interacting with a bug oracle systematically. GRAMMAR2FIX returns this grammar as a collection of Deterministic Finite Automata(DFA), and the grammar can serve as an automated test oracle for the bug. GRAMMAR2FIX also produces a test suite in grammar learning, which can be used as a repair test suite in Automated Program Repair.

GRAMMAR2FIX is implemented in Python. The following projects are used in our experiments.

## Setup GenProg
```
docker pull squareslab/genprog
docker run -it squareslab/genprog /bin/bash
```
