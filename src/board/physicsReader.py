def readPhysics(physicsfilename):
    with open(physicsfilename, 'r') as f:
        moves = dict()
        key = True
        currentKey = None
        for line in f:
            if key:
                currentKey = eval(line)
                moves[currentKey] = []
                key = False
            elif line.startswith('#'):
                key = True
            else:
                moves[currentKey].append(eval(line))

        return moves