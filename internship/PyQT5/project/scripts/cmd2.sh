#!/bin/bash

for i in {1..10}; do
  echo Step 2 - $i
  ping -c 1 127.0.0.1 > /dev/null
  sleep 1
done
