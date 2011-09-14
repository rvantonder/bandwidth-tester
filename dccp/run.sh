#!/bin/bash

if [ ! -n "$3" ]
then
  echo "Usage: ./`basename $0` <ip> <port> <num_clients>"
  exit
fi  

for i in $(seq "$3"); do
  python dccpclient.py "$1" "$2" &
done


