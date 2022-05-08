FROM ubuntu:18.04

RUN apt-get -y update

RUN apt-get -y install git wget build-essential time zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev

RUN wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tar.xz

RUN tar -xf Python-3.7.2.tar.xz

RUN cd Python-3.7.2 && ./configure --enable-optimizations && make -j4 && make altinstall

RUN ln -s $(which pip3.7) /usr/bin/pip

RUN ln -s $(which python3.7) /usr/bin/python

#install numpy

RUN apt-get -y update

RUN pip install numpy

#install grammar2fix

RUN cd /root && git clone https://github.com/charakageethal/grammar2fix.git

#install benchmarks

RUN cd /root && git clone https://github.com/jkoppel/QuixBugs

RUN cd /root && git clone https://github.com/ProgramRepair/IntroClass

RUN cd /root && git clone https://github.com/codeflaws/codeflaws

RUN cd /root/codeflaws/all-script && wget http://www.comp.nus.edu.sg/~release/codeflaws/codeflaws.tar.gz

RUN cd /root/codeflaws/all-script && tar -zxf codeflaws.tar.gz

WORKDIR /root/grammar2fix

