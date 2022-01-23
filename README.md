# grammar2fix
GRAMMAR2FIX is an active oracle learning technique for programs taking string inputs. Given a single failing input of a bug, it learns a grammar describing the pattern of all the failing inputs of the bug, interacting with a bug oracle systematically. The grammar is given as a collection of Deterministic Finite Automata (DFA), which is the automated test oracle. GRAMMAR2FIX also produces a test suite in grammar learning, which can be used as a repair test suite in Automated Program Repair.
## Setup GenProg
```
docker pull squareslab/genprog
docker run -it squareslab/genprog /bin/bash
```
