#!/bin/bash

echo "I'm lazy so I'm just going to run this on the fastest single threaded"
echo "EC2 instance rather than refactoring my recursion to parallelise in"
echo "python or (the right way) finding the efficient closed-form solution."
echo

system=$(uname -a)
if [[ $system != *"Ubuntu"* ]]; then
	echo "This script is only for Ubuntu!"
	exit 1
fi

echo "Installing dependencies..."
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install -y git
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update -y
sudo apt install python3.12 -y
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.12
echo "alias python=python3.12" >>~/.bashrc
echo 'PATH=/home/ubuntu/.local/bin:$PATH' >>~/.bashrc
source ~/.bashrc
pip install poetry
git clone https://www.github.com/oliverlambson/advent-of-code-2023.git

echo "Remember to run 'source ~/.bashrc'"
