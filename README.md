# GRAMMAR2FIX
GRAMMAR2FIX is an active oracle learning technique for programs taking string inputs. Given a single failing input of a bug, it learns a grammar describing the pattern of all the failing inputs of the bug, interacting with a bug oracle systematically. GRAMMAR2FIX returns this grammar as a collection of Deterministic Finite Automata(DFA), and the grammar can serve as an automated test oracle for the bug. GRAMMAR2FIX also produces a test suite in grammar learning, which can be used as a repair test suite in Automated Program Repair.

GRAMMAR2FIX is implemented in Python. The following benchmarks are used in the experiments.

* [QuixBugs](https://github.com/jkoppel/QuixBugs "QuixBugs")
* [IntroClass](https://github.com/ProgramRepair/IntroClass "IntroClass")
* [Codeflaws](https://github.com/codeflaws/codeflaws "Codeflaws")

GenProg (<a href="https://ieeexplore.ieee.org/document/6035728">Paper</a>, <a href="https://github.com/squaresLab/genprog-code">Tool</a>) is used as the automated program repair tool.

We conducted our experiments in Ubutu 18.04.6 LTS with 32 logical cores. 

# <a id="getting_started"/> Getting Started 

## Step 1- Install Supporting Components

GRAMMAR2FIX needs Python 3.7.2 or greater. Also, "git", "numpy" and "wget" are necessary. If these are not available, use the following commands to install it in linux.

```
apt-get update
apt-get -y install git wget build-essential time zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev

#Install Python 3.7
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

# install numpy
pip install numpy

```
## Step 2- Install benckmarks

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
## Step 3- Install GRAMMAR2FIX
Clone GRAMMAR2FIX github repository 
```
git clone https://github.com/charakageethal/grammar2fix.git
```

# Reproduce Experimental Results
## <a id="basic_expr"/>Running the experiments to measure oracle accuracy and labelling effort of GRAMMAR2FIX.

To repat the experiments related to oracle accuracy and labelling effort, GRAMMAR2FIX contains _"quixbugs_experiments.sh"_ for QuixBugs, _"introclass_experiments.sh"_ for IntroClass and _"codeflaws_experiments.sh"_ for Codeflaws.

### <a id="expr_runs"/> Step 1- Run GRAMMAR2FIX on the benchmarks
```
cd grammar2fix
./quixbugs_experiments.sh <<path to QuixBugs>>
./introclass_experiments.sh <<path to IntroClass>>
./codeflaws_experiments.sh <<path to Codeflaws>>
```
The .csv files are copied to the grammar2fix/results folder
### Step 2-Reproduce the results
We use [R](https://www.r-project.org/) to generate the graphs. Follow [these instructions](https://computingforgeeks.com/how-to-install-r-and-rstudio-on-ubuntu-debian-mint/) to install R and Rstudio. 
After that, go to the **results** folder and run _"overall_accuracy_benchmarks.R"_ and _"grammar_gen_wise_plots.R"_. 

## Running Program Repair experiments with codeflaws.
We use [GenProg docker](https://github.com/squaresLab/genprog-code) to run the program repair experiments. 

### Step 1- Setup GenProg docker
Setup a docker container for GenProg repair tool
```
docker pull squareslab/genprog
docker run -it squareslab/genprog /bin/bash
```
### Step 2- Setup GRAMMAR2FIX and benchmarks

Repeat the steps in [Getting Started](#getting_started) to setup GRAMMAR2FIX and Codeflaws in the docker container. Download GRAMMAR2FIX repository to the "/root" directory of the docker container.

### Step 3 - Run GRAMMAR2FIX on Codeflaws
Run the script _"codeflaws_repair_experiments.sh"_ as follows.
```
cd grammar2fix
./codeflaws_repair_experiments.sh <<path to codeflaws>>
```
### Step 4 - Reproduce program repair results
Go to grammar2fix/results/codeflaws_repair and run _"codeflaws_repair.R"_

## Running experiments through Dockerfile
We have provided a Dockerfile to run the experiments realated to oracle accuracy and labelling effort of GRAMMAR2FIX ([See Above](#basic_expr)). Use the following command to build the docker container from the Dockerfile
```
sudo docker build -t <<docker_container_name>> .
```
Use the following command to run the docker container.
```
sudo docker run -it <<docker_container_name>> /bin/bash
```
The Dockerfile downloads the benchmarks to the following locations.
* QuixBugs : /root/QuixBugs
* IntroClass : /root/IntroClass
* Codeflaws : /root/codeflaws/all-script/codelfaws

After that run the experiment scripts as previously ([See Above](#expr_runs))

