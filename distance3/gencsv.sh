#!/bin/bash

seq 1 10000 | shuf > 1-10000.csv
seq 10001 20000 | shuf > 10001-20000.csv
seq 20001 30000 | shuf > 20001-30000.csv
seq 30001 40000 | shuf > 30001-40000.csv
seq 40001 50000 | shuf > 40001-50000.csv
seq 50001 60000 | shuf > 50001-60000.csv
