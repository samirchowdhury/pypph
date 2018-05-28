import sys
from pph.pphTools import Dirnet
print(sys.argv)


def run():
    fn = sys.argv.pop()
    #readNet(fn)
    dn = Dirnet(fn)
    #dn.readNet(fn)
    print("num nodes is " + dn.num_nodes)
    print("edge weights are", dn.wgts)
    print("edges are", dn.edges)
    print("0-paths are ",dn.ap[0])
    print(dn.apwgts[0])
    print("1-paths are ", dn.ap[1])
    print(dn.apwgts[1])
    print("2-paths are", dn.ap[2])
    print(dn.apwgts[2])
    print("marked paths are", dn.marked)
    print("summands are",dn.summands)
    print("path is ", dn.testy)
    print("maxindex is ",dn.maxindex)
    print("slots are", dn.slots)
    #print("1-paths are now", dn.ap[1])
    #print(dn.apwgts[1])
    #print(dn.ap)
    #print(dn.oneap[0][0][0])

run()
