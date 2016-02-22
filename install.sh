#!/bin/bash 

sudo apt-get remove python3-pip python-pip
wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py
sudo python get-pip.py
rm get-pip.py

#pip install pytesser
pip install requests
pip install Pillow-PIL

git clone https://github.com/python-pillow/Pillow.git
cd Pillow
