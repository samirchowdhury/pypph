# function to read network data 
# my convention: function names are lowercaseUppercase, 
# variable names are lowercase_lowercase

from operator import itemgetter

class Dirnet(object):
    def __init__(self, data_file):
        # variables
        self.max_dim     = 2  # hard-coded for now
        self.max_time    = 10000 # hard-coded for now
        self.min_time    = 0 # hard-coded for now
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
        self.at_max_term = self.min_time
        self.et          = self.min_time
        self.grewlistby  = 0
        self.testy       = []
        self.testx       = []
        self.testz       = []
        self.maxindex    = []
        self.pers        = []

        # member functions
        self.readNet(data_file)
        self.makePers()
        self.getAPaths()
        self.makeSlots()
        self.markZero()

        #self.markOne()
        self.runpph()
        #self.testcb()

    def makePers(self):
        for i in range(0, self.max_dim):
            self.pers.append([str(i)+"-dim bars are ", []])

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
        zeroap_times        = [self.min_time] * int(self.num_nodes)
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
        # get the allow time of summand with maxindex
        lp               = len(path)
        at_max_term      = self.apwgts[lp-2][maxindex]
        
        return [term_idx_in_summands, max_term_in_summands, maxindex, at_max_term]


    def hasRepeats(self,path):
        lp = len(path)
        flag = False
        for idx in range(0,lp-1):
            if (path[idx] == path[idx+1]):
                flag = True
        return flag

    def computeSimpleBoundary(self,path):
        summands = []
        #lp = len(path)
        workdim = 1 # hardcode, will need to change for higher dim implem
        apset = set(self.ap[workdim])
        #self.testy = apset
        # apply boundary operator
        for idx in enumerate(path):
            bd = [s for s in path]
            del bd[idx[0]]

            # terms of type [1 1] or [2 2] are not added to summand
            if (self.hasRepeats(bd)):
                continue
            
            # unmarked terms are not added, except if they are unallowed
            # assumption: 0-paths are connected by supplied edges, 
            # so only modification is to 1-paths (for current implem)
            q = tuple(bd)
            if (len(bd)==1):
                if bd[0] in self.marked:
                    summands.append(bd[0])        
            elif (len(bd)==2 and q not in apset):   # grow arrays if needed
                summands.append(q)
                self.ap[workdim].append(q)
                self.apwgts[workdim].append(self.max_time)
                self.slots[1].append([])
                apset = apset.union([q])
                self.grewlistby = self.grewlistby + 1
                # mark that we grew the list
            else:
                if tuple(bd) in self.marked:
                    summands.append(tuple(bd))
        return summands
   
    def computeBoundary(self, path, path_dim, path_idx):
        at_path     = self.apwgts[path_dim][path_idx]
        summands    = self.computeSimpleBoundary(path)
        self.basisChange(path,summands)
        self.et     = max(at_path, self.at_max_term)
        
        
        
    
    def basisChange(self,path,summands):
        bd_ap_idx = len(path)-2
        maxindex = 0
        at_max_term = self.min_time
        # if maxidx slot has something, do cancellation (Z2 coeff here)
        while (summands):
            q = self.getMaxIndx(path,summands)
            #max_term               = q[1]
            #max_term_idx_summands   = q[0] 
            maxindex                = q[2]
            at_max_term             = q[3]

            if (self.slots[bd_ap_idx][maxindex]):
                # if there is stuff, then it has positive length
                list_el = self.slots[bd_ap_idx][maxindex][0]
                summands= [x for x in summands if x not in list_el]

                #del summands[max_term_idx_summands]
            else:
                break    
        self.summands = summands
        #self.testy    = path
        self.at_max_term = at_max_term
        self.maxindex = maxindex

    def storeOrMark(self,path,workdim,savedim,et):
        if (self.summands):
            self.slots[savedim][self.maxindex] = tuple([self.summands,et])
            # add to pers
            birth   = float(self.apwgts[savedim][self.maxindex])
            death   = float(et)
            if (birth < death):
                bar = tuple([birth,death])
                self.pers[savedim][1].append(bar)
        else:
            #self.slots[savedim][self.maxindex] = tuple([self.summands,et])
            
            self.marked.append(path)

    

    def runpph(self):
        workdim = range(1,3)
        for i in workdim:
            savedim = i-1
            j = 0
            while j < len(self.ap[i]):
                path            = self.ap[i][j]
                at_path         = self.apwgts[i][j]
                #et              = at_path
            #for path in self.ap[i]:
                self.computeBoundary(path,i,j)
                if (self.grewlistby):
                    for k in range(1,self.grewlistby+1):
                        temp_workdim    = i-1
                        temp_savedim    = i-2
                        temp_path       = self.ap[temp_workdim][0-k] #access last k elements
                        temp_path_idx   = self.ap[temp_workdim].index(temp_path) 
                        self.computeBoundary(temp_path, temp_workdim, temp_path_idx)
                        #et = max(at_path, self.at_max_term)
                        self.testy = at_path
                        self.testx = self.summands
                        self.testz = temp_path
                        self.storeOrMark(temp_path,temp_workdim,temp_savedim, self.et)
                    self.grewlistby = 0
                    j = j-1
                    
                else:
                    # et = max(at_path, self.at_max_term)
                    self.storeOrMark(path,workdim,savedim,self.et)
                j = j+1
        for i in range(0,self.max_dim):
            for idx, term in enumerate(self.ap[i]):
                if (term in self.marked and not self.slots[i][idx]):
                    birth       = float(self.apwgts[i][idx])
                    death       = float(self.max_time)
                    self.testy  = i
                    self.testx  = idx
                    self.testz  = birth
                    if (birth < death):
                        bar     = tuple([birth,death])
                        self.pers[i][1].append(bar)



            
            

