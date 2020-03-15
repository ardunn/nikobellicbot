#!/bin/bash

shopt -s expand_aliases
source ~/.bashrc

cenv
python main.py > bot.log 2> bot.err &
disown -h %1
