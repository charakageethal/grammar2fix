# GRAMMAR2FIX
GRAMMAR2FIX is an active oracle learning technique for programs taking string inputs. Given a single failing input of a bug, it learns a grammar describing the pattern of all the failing inputs of the bug, interacting with a bug oracle systematically. GRAMMAR2FIX returns this grammar as a collection of Deterministic Finite Automata(DFA), and the grammar can serve as an automated test oracle for the bug. GRAMMAR2FIX also produces a test suite in grammar learning, which can be used as a repair test suite in Automated Program Repair.

GRAMMAR2FIX is implemented in Python. The following benchmarks are used in the experiments.

* [QuixBugs](https://github.com/jkoppel/QuixBugs "QuixBugs")
* [IntroClass](https://github.com/ProgramRepair/IntroClass "IntroClass")
* [Codeflaws](https://github.com/codeflaws/codeflaws "Codeflaws")

GenProg (<a href="https://ieeexplore.ieee.org/document/6035728">Paper</a>, <a href="https://github.com/squaresLab/genprog-code">Tool</a>) is used as the automated program repair tool.

We conducted our experiments in Ubutu 18.04.6 LTS with 32 logical cores.

# How to run GRAMMAR2FIX
## Running the experiments to measure oracle accuracy and labelling effort of GRAMMAR2FIX.

To repat the experiments related to oracle accuracy and labelling effort, GRAMMAR2FIX needs Python 3.7.2 or greater. Also, "git" and "wget" are necessary. If these are not available, use the following commands to install it in linux.

```
apt-get update
apt-get -y install git wget build-essential
pushd /tmp
wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tar.xz
tar -xf Python-3.7.2.tar.xz
cd Python-3.7.2
./configure --enable-optimizations
make -j4
make altinstall
ln -s $(which pip3.7) /usr/bin/pip
mv /usr/bin/python /usr/bin/python.old
ln -s $(which python3.7) /usr/bin/python
popd
```
### Step 1- Install benckmarks
Download and install benchmarks as follows. 
```
# Install QuixBugs
git clone https://github.com/jkoppel/QuixBugs

# Install IntroClass
git clone https://github.com/ProgramRepair/IntroClass
cd IntroClass
make
cd ~

# Install Codeflaws
git clone https://github.com/codeflaws/codeflaws
cd codeflaws/all-script
wget http://www.comp.nus.edu.sg/~release/codeflaws/codeflaws.tar.gz
tar -zxf codeflaws.tar.gz
cd ~
```
### Step 2- Run GRAMMAR2FIX on the benchmarks
Copy the GRAMMAR2FIX repository to the machine and execute the following scripts.
```
cd grammar2fix
./quixbugs_experiments.sh <<path to QuixBugs>>
./introclass_experiments.sh <<path to IntroClass>>
./codeflaws_experiments.sh <<path to Codeflaws>>
```
The .csv files are copied to the grammar2fix/results folder
### Step 3-Reproduce the results
Go to the grammar2fix results folder and run "overall_accuracy_benchmarks.R" and "grammar_gen_wise_plots.R". 

## Running Program Repair experiments with codeflaws.
### Step 1-Install Codeflaws with GenProg
Setup a docker container for GenProg repair tool
```
docker pull squareslab/genprog
docker run -it squareslab/genprog /bin/bash
```
Download and setup any dependencies

```
apt-get update
apt-get -y install git time build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget z3 bc

# Install python
pushd /tmp
wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tar.xz
tar -xf Python-3.7.2.tar.xz
cd Python-3.7.2
./configure --enable-optimizations
make -j4
make altinstall
ln -s $(which pip3.7) /usr/bin/pip
mv /usr/bin/python /usr/bin/python.old
ln -s $(which python3.7) /usr/bin/python
popd

# Set the path for cilly compiler
export PATH=/root/.opam/system/bin/:$PATH
```
Download and set up the Codeflaws benchmark inside the container

```
cd /root
git clone https://github.com/codeflaws/codeflaws
cd codeflaws/all-script
wget http://www.comp.nus.edu.sg/~release/codeflaws/codeflaws.tar.gz
tar -zxf codeflaws.tar.gz
```
### Step 2 - Run GRAMMAR2FIX on Codeflaws
Download GRAMMAR2FIX repository to the /root directory of the container. Run the following scripts
```
cd grammar2fix
./codeflaws_repair_experiments.sh <<path to codeflaws>>
# Default path: /root/codeflaws/all-script/codeflaws
```
### Step 3 - Reproduce program repair results
Go to grammar2fix/results/codeflaws_repair and run "codeflaws_repair.R"


