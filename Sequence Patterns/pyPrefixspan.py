# All rights reserved.
# http://datamininginsight.blogspot.com

class Prefixspan:
    def __init__(self, db = []):
        self.db = db
        self.genSdb()
        
    def genSdb(self):
        '''
        Generate mutual converting tables between db and sdb 
        '''
        self.db2sdb = dict()
        self.sdb2db = list()
        count = 0
        self.sdb = list()
        for seq in self.db:
            newseq = list()
            for item in seq:
                if self.db2sdb.has_key(item):
                    pass
                else:
                    self.db2sdb[item] = count
                    self.sdb2db.append(item)
                    count += 1
                newseq.append( self.db2sdb[item] )
            self.sdb.append( newseq )
        self.itemCount = count
    
    def run(self, min_sup = 3):
        '''
        mine patterns with min_sup as the min support threshold
        '''
        self.min_sup = min_sup
        L1Patterns = self.genL1Patterns()
        patterns = self.genPatterns( L1Patterns )
        self.sdbpatterns = L1Patterns + patterns

    def getPatterns(self):
        '''
        returns the set of the patterns, which is a list of
        tuples (sequence, support)
        '''
        oriPatterns = list()
        for (pattern, sup, pdb) in self.sdbpatterns:
            oriPattern = list()
            for item in pattern:
                oriPattern.append(self.sdb2db[item])
            oriPatterns.append( (oriPattern, sup) )
        return oriPatterns
        
    def genL1Patterns(self):
        '''
        generate length-1 patterns
        '''
        pattern = []
        sup = len(self.sdb)
        pdb = [(i,0) for i in range(len(self.sdb))]
        L1Prefixes = self.span( (pattern, sup, pdb) )
        return L1Prefixes
    
    def genPatterns(self, prefixes):
        '''
        generate length-(l+1) patterns from
        length-l patterns
        '''
        results = []
        for prefix in prefixes:
            result = self.span(prefix)
            results += result
        if results != []:
            results += self.genPatterns( results )
        return results
    
    def span(self, prefix):
        '''
        span current length-l prefix pattern set
        to length-(l+1) prefix pattern set.
        prefix is a tuple (pattern, sup, pdb):
        pattern is an list representation of the pattern,
        sup is the absolute support of the pattern,
        pdb is the projection database of the pattern, 
        which is a list of tuples in the form of (sid,pos).
        '''
        (pattern, sup, pdb) = prefix
        itemSups = [0] * self.itemCount
        for (sid, pid) in pdb:
            itemAppear = [0] * self.itemCount
            for item in self.sdb[sid][pid:]:
                itemAppear[item] = 1
            itemSups = map(lambda x,y: x+y, itemSups, itemAppear)
        prefixes = list()
        for i in range(len(itemSups)):
            if itemSups[i] >= self.min_sup:
                newPattern = pattern + [i]
                newSup = itemSups[i]
                newPdb = list()
                for (sid, pid) in pdb:
                    for j in range(pid, len(self.sdb[sid])):
                        item = self.sdb[sid][j]
                        if item == i:
                            newPdb.append( (sid, j+1) )
                            break
                prefixes.append( (newPattern, newSup, newPdb) )
                #self.span( (newPattern, newSup, newPdb) )
        return prefixes
         
def mine(inputfile, outputfile, support):
    f = open(inputfile)
    lines = f.readlines()
    f.close()
    sdb = []
    for line in lines:
        seq = line.split(' ')
        sdb.append( seq[0:-2] )
    span = Prefixspan(sdb)
    span.run(support)
    patterns = span.getPatterns()
    patterns.sort(key=lambda x: x[1])
    f = open(outputfile, 'w')
    for pattern in patterns:
        f.write( str(pattern) + '\n' )
    f.close()
        
def test():
    db = [[0,1,2,3,4], [0,1,2,3],[3,2,1,2,1,2],[1,2,3,2,3,1],[1,2,3,1,0,1]]
    span = Prefixspan(db)
    span.run(3)
    print span.getPatterns()
    
def displayUsage():
    print '''
    Usage:
    1. needs an input file (.txt) with sequences
    This can be specified in the main()
    2. 
    python pyPrefixspan.py input_file_name output_file_name support_threshold
    
    All rights reserved.
    http://datamininginsight.blogspot.com
    '''
    
def main():
    from sys import argv
    displayUsage()
    
    mine('trajectories.txt','allTrajectorySupport.txt',100)

    

if __name__ == "__main__":
    main()
    
