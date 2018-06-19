import sys
from pph.pphTools import Dirnet

""" for generating log files
old_stdout = sys.stdout
log_file = open("message.log","w")
sys.stdout = log_file
"""

print(sys.argv)


def run():
    fn = sys.argv.pop()
    #readNet(fn)
    dn = Dirnet(fn)
    #dn.readNet(fn)
    #print("num nodes is " + dn.num_nodes)
    #print("edge weights are", dn.wgts)
    #print("edges are", dn.edges)
    #print("0-paths are ",dn.ap[0])
    #print(dn.apwgts[0])
    #print("1-paths are ", dn.ap[1])
    #print(dn.apwgts[1])
    #print("2-paths are", dn.ap[2])
    #print("num 2-paths", len(dn.ap[2]))
    #print(dn.apwgts[2])
    #print("num marked", len(dn.marked))
    #print("marked paths are", dn.marked)
    #print("summands are",dn.summands)
    #print("testx is ", dn.testx)
    #print("testy is ", dn.testy)
    #print("testz is ", dn.testz)
    #print("lenbd is ", dn.lenbd)
    #print("bd is ", dn.bd)
    #print("tupbd is ", dn.tupbd)
    #print("tubpd inside", dn.tupbdset)
    #print("maxindex is ",dn.maxindex)
    #print("slots are", dn.slots)
    
    #print("test value is ", dn.testx)
    #print("test value is ", dn.testy)
    #print("test value is ", dn.testz)
    print("pers bars are", dn.pers)
    #print("1-paths are now", dn.ap[1])
    #print(dn.apwgts[1])
    #print(dn.ap)
    #print(dn.oneap[0][0][0])

run()

"""
sys.stdout = old_stdout
log_file.close()
"""