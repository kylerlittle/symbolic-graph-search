#!/bin/bash

# Get script directory absolute path. This way script always runs as if from within 'scripts/' dir.
scriptDir=$(dirname -- "$(readlink -f -- "$BASH_SOURCE")")
cd "$scriptDir"

# Install Python3
sudo apt-get install libssl-dev openssl
wget https://www.python.org/ftp/python/3.5.0/Python-3.5.0.tgz
tar xzvf Python-3.5.0.tgz
cd Python-3.5.0
./configure
make
sudo make install

# Clean-up
cd ..
rm Python-3.5.0.tgz
sudo rm -rf Python-3.5.0/

# Install pip
sudo apt-get install python3-pip

# Install virtualenv
sudo pip3 install virtualenv

# Setup virtual env in home directory of project.
cd ..
virtualenv --python=python3.5 venv

# Install graphviz
git clone https://gitlab.com/graphviz/graphviz.git
cd graphviz
./autogen.sh
./configure
make
sudo make install
cd ..
