FROM ubuntu:18.04

RUN apt-get -y update

RUN apt-get -y install git wget build-essential time zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev

RUN cd /tmp

RUN wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tar.xz

RUN tar -xf Python-3.7.2.tar.xz

RUN cd Python-3.7.2 && ./configure --enable-optimizations && make -j4 && make altinstall

RUN ln -s $(which pip3.7) /usr/bin/pip

RUN ln -s $(which python3.7) /usr/bin/python

RUN cd /root


#install grammar2fix

RUN git clone https://github.com/charakageethal/grammar2fix.git

#install benchmarks

RUN git clone https://github.com/jkoppel/QuixBugs

RUN git clone https://github.com/ProgramRepair/IntroClass

RUN git clone https://github.com/codeflaws/codeflaws

RUN cd codeflaws/all-script

RUN wget http://www.comp.nus.edu.sg/~release/codeflaws/codeflaws.tar.gz

RUN tar -zxf codeflaws.tar.gz

RUN cd ~

WORKDIR grammar2fix
