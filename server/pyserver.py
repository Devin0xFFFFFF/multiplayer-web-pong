#!/usr/bin/python
from sys import stdout
from time import sleep

# Count from 1 to 10 with a sleep
for count in range(0, 1000):
  msg = "{\"HEAD\": \"CMD\", \"BODY\": {\"targetID\":\"ball\", \"action\": \"move\", \"args\": [10]}}"
  print(msg)
  stdout.flush()
  sleep(0.015)