#!/bin/bash
sudo apt-get update
sudo apt-get install python
sudo apt-get install python-pip
sudo pip install virtualenv
sudo apt-get install python-tk
virtualenv -q -p /usr/bin/python2.7 BDM
BDM/bin/pip install -r requirements.txt
python polarity10K.py