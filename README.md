# motostat-to-spritmonitor

A project for converting csv files from https://www.motostat.pl to csv files in a format compatible with https://www.spritmonitor.de

## Prerequisite

 - UNIX/Linux
 - Python3.11
 - virtualenv module 
 - pip module
 - git

## Installation

- mkdir ~/bin
- git clone https://github.com/Szumak75/motostat-to-spritmonitor.git
- ln -s `pwd`/motostat-to-spritmonitor/bin/motostat-to-spritmonitor ~/bin
- cd motostat-to-spritmonitor
- python3 -mvenv .venv
- source .venv/bin/activate
- pip install -r requirements.txt
