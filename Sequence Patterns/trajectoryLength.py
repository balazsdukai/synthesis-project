import matplotlib.pyplot as plt
import numpy as np

def mine(inputfile):
    length = []
    f = open(inputfile)
    lines = f.readlines()
    f.close()
    for line in lines:
        traj = line.split(' ')
        trajLen = len(traj)-1
        if trajLen < 20:
            length.append(trajLen)
    print np.mean(length)

    histogram(length)


def histogram(data):
    bins = [2,3,4,5,6,7,8]
    # the histogram of the data with histtype='step'
    n, bins, patches = plt.hist(data, bins, histtype='bar', rwidth=1.0)
    
    #plt.hist(data)
    plt.title("Lenght of trajectory")
    plt.xlabel("Lenght")
    plt.ylabel("Frequency")
    #plt.axis([2, 10, 0, 1000000])
    
    plt.show()


def main():
    mine('trajectories.txt')    



if __name__ == "__main__":
    main()
