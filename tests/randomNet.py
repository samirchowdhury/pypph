import sys
import numpy as np

num_nodes   = int(sys.argv.pop())
file_id     = sys.argv.pop()

A = np.multiply(np.random.rand(num_nodes,num_nodes),1 - np.identity(num_nodes))

f = open("randNet"+file_id+".txt","w+")
f.write(str(num_nodes)+"\n")

for i in range(0,num_nodes-1):
    for j in range(i+1,num_nodes):
        f.write(str(i) + " " + str(j) + " " + str(round(A[i][j],2))+"\n")


for i in range(1,num_nodes):
    for j in range(0,i):
        f.write(str(i) + " " + str(j) + " " + str(round(A[i][j],2))+"\n")


f.close()