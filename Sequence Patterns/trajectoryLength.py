def mine(inputfile):
    lenght = []
    f = open(inputfile)
    lines = f.readlines()
    f.close()
    for line in lines[:10]:
        traj = line.split(' ')
        print traj, len(traj)-1
        trajLen = len(traj)
        lenght.append(trajLen)

def main():
    mine('trajectories.txt')    



if __name__ == "__main__":
    main()
