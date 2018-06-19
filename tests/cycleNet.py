import sys

from collections import deque

num_nodes   = int(sys.argv.pop())
file_id     = str(num_nodes)

f = open("cycleNet"+file_id+".txt","w+")
f.write(str(num_nodes)+"\n")

for i in range(0,num_nodes-1):
    for j in range(i+1,num_nodes):
        f.write(str(i) + " " + str(j) + " " + str(j-i)+"\n")


for i in range(1,num_nodes):
    for j in range(0,i):
        f.write(str(i) + " " + str(j) + " " + str(j+num_nodes-i)+"\n")

f.close()

