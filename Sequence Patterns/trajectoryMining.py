
def mine(inputfile):
    subSeq = []
    distinctSeq = []
    f = open(inputfile)
    lines = f.readlines()
    f.close()
    for line in lines:
        split = line.split('],')
        seq, support = split[0].strip('(['), split[1]
        support = int((support[:-2]))
        seq = seq.split(', ')
        seq = map( int,seq )
        subSeq.append( (seq,support) )
    for seq,sup in subSeq:
        if len(seq) > 4 and sup > 300:
            seen=set()
            for i in seq:
                if i not in seen:
                    seen.add(i)
            if len(seen) > 3:
                distinctSeq.append((seq,sup))
                
    for seq in distinctSeq:
        print seq
                    
                        
                    
    """    
        if len( seq ) > 3 and support > 2000:
            write( seq,support )
        distinctSeq()


    


def write(seq,sup):
    with open('testMining.txt', 'a') as f:
        f.write(str(seq)+' '+str(sup)+'\n')
"""       

def main():
    mine('testSupport.txt')    



if __name__ == "__main__":
    main()
