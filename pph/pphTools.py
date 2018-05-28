# function to read network data 
# my convention: function names are lowercaseUppercase, 
# variable names are lowercase_lowercase

from operator import itemgetter

class Dirnet(object):
    def __init__(self, data_file):
        self.max_dim     = 2  # hard-coded for now
        self.max_time    = 10000 # hard-coded for now
        self.num_nodes   = 0
        self.edges       = []
        self.wgts        = []
        #self.oneap       = [] # allowed 1-paths
        #self.twoap       = []
        self.ap          = [] # all paths
        self.apwgts      = [] # all allow times 
        self.slots       = [] # linear arrays containing slots
        self.marked      = [] # pool all marked paths
        self.summands    = []
        self.testy       = []
        self.maxindex    = []
        self.readNet(data_file)
        self.getAPaths()
        self.makeSlots()
        self.markZero()
        #self.markOne()
        self.runpph()
        #self.testcb()


    def readNet(self, data_file):
        fn                  = data_file
        f                   = open(fn)
        data                = f.read()
        f.close()
        data                = data.split()
        self.num_nodes      = data.pop(0)
        # need to pop out the number of nodes first
        self.wgts           = data[2::3]
        self.edges          = zip(data[0::3],data[1::3])


    def getAPaths(self):
        # Current implementation only handles up to 2-paths.
        # get allowed paths
        # 0-paths first
        zeroap              = [str(s) for s in range(1, int(self.num_nodes)+1)]
        #zeroap              = zip(zeroap, [0]*int(self.num_nodes))
        zeroap_times        = [0] * int(self.num_nodes)
        self.ap.append(zeroap)
        self.apwgts.append(zeroap_times)

        # 1-paths next
        oneap               = zip(self.edges,self.wgts)
        oneap               = sorted(oneap,key=itemgetter(1)) 
        # after sorting by times, split into paths and times
        oneap_times         = [s[1] for s in oneap]
        oneap               = [s[0] for s in oneap]
        self.apwgts.append(oneap_times)
        self.ap.append(oneap)
        # 1-paths done, now do 2-paths
        """ 
        This implementation uses nested for loops to construct
        2-paths. If there are Cn edges in the graph, where n
        is the number of nodes, then the 
        nested loops will take (Cn)^2 time. In contrast, using 
        npermk to precompute all possible 2-paths on n nodes 
        will cost n^3 time.
        """
        twoap       =   []
        for i_indx, i in enumerate(self.edges):
            for j_indx, j in enumerate(self.edges):
                if (j[0]==i[1]):
                    twoap_temp  = (i[0], i[1], j[1])
                    twoap_time  = max(self.wgts[i_indx], self.wgts[j_indx])
                    #temp        = zip(twoap,twoap_time)
                    twoap.append((twoap_temp,twoap_time))
                    #print("j[0] is ",j[0], "i[1] is ", i[1])
                    #print("j is ", j, "i is ", i)
        
        twoap       =   sorted(twoap,key=itemgetter(1))
        # sorted by allow times, now split
        twoap_times = [s[1] for s in twoap]
        twoap       = [s[0] for s in twoap] 
        self.ap.append(twoap)
        self.apwgts.append(twoap_times)
        # pool things together

    def makeSlots(self):
        # initialize the slots 
        for i in range(0, self.max_dim+1):
            temp = [[] for s in self.ap[i]]
            self.slots.append(temp)
        #self.slots = [[] for s in range(1,4)]


    def markZero(self):
        # for 0-paths, boundary is 0. mark and move on
        for i in range(1,int(self.num_nodes)+1):
            self.marked.append(str(i))

    def markOne(self):
        # just for testing, this should not be used in final code
        for s in self.ap[1]:
            self.marked.append(s)

    """ For getIndx:
        term is an element in the boundary of path.
        if path is del-invariant, then term will be 
        an allowed path automatically. otherwise, term
        will enter the filtration at the endtime. 
    """
    def getIndx(self, path, term):
        # get the index of a summand of a path
        # if path not allowed, append to self.ap at max_time
        lp = len(path)
        # finding element and index in list
        if (term not in self.ap[lp-2]):
            self.ap[lp-2].append(term)
            self.apwgts[lp-2].append(self.max_time)
        
        idx = self.ap[lp-2].index(term)
        return idx

        """
        if (term in self.ap[lp-2]):
            idx = self.ap[lp-2].index(term)
        else:
            # idx = -1
            self.ap[lp-2].append(term)
            idx = self.ap
        return idx
        """
    # function to return maxindex element from path and summands
    # summands refer to marked elements returned from applying del
    # operator to path
    def getMaxIndx(self, path, summands):
        term_idx_in_summands = 0
        max_term_in_summands = summands[0]
        maxindex             = self.getIndx(path, max_term_in_summands)
        for term in summands:
            if (self.getIndx(path, term) > maxindex):
                term_idx_in_summands = summands.index(term)
                max_term_in_summands = term
                maxindex             = self.getIndx(path,term)
        return [term_idx_in_summands, max_term_in_summands, maxindex]


    """ For computeBoundary:
        following can be used if we want Zp or real coeff;
        just use (-1)**idx

        for idx, term in enumerate(path):
            bd = [s for s in path if s != term]
            summands.append(bd)
    """
    def hasRepeats(self,path):
        lp = len(path)
        flag = False
        for idx in range(0,lp-1):
            if (path[idx] == path[idx+1]):
                flag = True
        return flag

    def computeSimpleBoundary(self,path):
        summands = []
        # apply boundary operator
        for idx in enumerate(path):
            bd = [s for s in path]
            del bd[idx[0]]

            # terms of type [1 1] or [2 2] are not added to summand
            if (self.hasRepeats(bd)):
                continue
            if (len(bd)==1):
                if bd[0] in self.marked:
                    summands.append(bd[0])
            else:
                if tuple(bd) in self.marked:
                    summands.append(tuple(bd))
        return summands
   
    def computeBoundary(self, path):
        summands = self.computeSimpleBoundary(path)
        self.basisChange(path,summands)
        
        
    
    def basisChange(self,path,summands):
        bd_ap_idx = len(path)-2
        maxindex = 0
        # if maxidx slot has something, remove maxidx element (Z2 coeff here)
        while (summands):
            q = self.getMaxIndx(path,summands)
            #max_term               = q[1]
            max_term_idx_summands   = q[0] 
            maxindex                = q[2]

            if (self.slots[bd_ap_idx][maxindex]):
                del summands[max_term_idx_summands]
            else:
                break    
        self.summands = summands
        self.testy    = path
        self.maxindex = maxindex


    def runpph(self):
        workdim = range(1,3)
        for i in workdim:
            savedim = i-1
            for path in self.ap[i]:
                self.computeBoundary(path)
                if (self.summands):
                    self.slots[savedim][self.maxindex] = self.summands
                else:
                    self.marked.append(path)

"""
    def testcb(self):
        for j in range(0,2):
            self.computeBoundary(self.ap[2][j])
            if (self.summands):
                self.slots[1][self.maxindex] = self.summands
"""

    






