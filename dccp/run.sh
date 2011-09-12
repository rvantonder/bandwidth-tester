#!/bin/bash

A="1 2 3 4 5 6 7 8 "

for i in $(seq 100); do
 python dccpclient.py 146.232.49.44 3002 & #los die ampersand in!
done
