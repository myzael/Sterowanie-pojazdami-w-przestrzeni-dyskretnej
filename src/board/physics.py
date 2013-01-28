from math import floor
from math import ceil
from matplotlib import patches
from matplotlib.path import Path
import networkx as nx
from src.board.convexHull import convex_hull
from vect2d import *
from copy import deepcopy
from numpy import *
import pylab


def distance(p1, p2):
    return p1.get_distance(p2)


def isInReach(curPoint, startPoint, startSpeed, maxPosAcc):
    dist = distance(curPoint, startPoint)
    maxi = startSpeed + 0.5 * maxPosAcc
    return dist <= maxi


def getStartVs(maxSpeed):
    for startSpeed in xrange(maxSpeed + 1):
        for startVDirX in xrange(-1, 2):
            for startVDirY in xrange(-1, 2):
                if startVDirX != 0 or startVDirY != 0:
                    yield startSpeed, Vec2d(startVDirX, startVDirY)


def getVelocities(curV, maxSpeed, maxPosAcc, maxNegAcc):
    for v in getStartVs(maxSpeed):
        if curV[0] + maxPosAcc > v[0] > curV[0] - maxNegAcc:
            yield v


def calculateBezierLength(trajectory):
    distance = 0.0
    curPoint = trajectory[0]
    for point in trajectory:
        distance = distance + point.get_distance(curPoint)
        curPoint = point
    return distance


def curVelocityReachable(trajectory, startSpeed, curSpeed, maxPosAcc, maxNegAcc):
    lenght = calculateBezierLength(trajectory)
    lenghtGood = startSpeed - 0.5 * maxNegAcc <= lenght <= startSpeed + 0.5 * maxPosAcc
    first = trajectory[0]
    last = trajectory[-1]

    maxSpeed = curSpeed + maxPosAcc
    minSpeed = curSpeed - maxNegAcc
    speedGood = minSpeed <= curSpeed <= maxSpeed

    accGood = -maxNegAcc <= curSpeed - startSpeed <= maxPosAcc
    return lenghtGood and speedGood and accGood


def calculateTakenFields(trajectory):
    taken = set()
    taken.add((0, 0))
    for point in trajectory:
        surrounding = (Vec2d(x, y) for x, y in [(floor(point.x), floor(point.y)),
                                                (floor(point.x), ceil(point.y)),
                                                (ceil(point.x), floor(point.y)),
                                                (ceil(point.x), ceil(point.y))])
        for s in surrounding:
            if s.get_dist_sqrd(point) < 2:
                taken.add((int(s.x), int(s.y)))

    return list(taken)


def accelerationAllowed(trajectory):
    return True


def fixVelocity(v):
    if v[0] == 0:
        return (0.5, v[1])
    else:
        return v

def unfixVelocity(v):
    if v[0] == 0.5:
        return (0, v[1])
    else:
        return v


def getAllowedMoves(maxSpeed, maxPosAcc=1, maxNegAcc=2, vis=False):
    """
    Calculates and returns tbe list of allowed moves.
    List contains tuples of the following elements:
    """

    moves = dict()
    grid = createGrid(maxSpeed)

    vs = getStartVs(maxSpeed)
    #for startV in vs:
    #   print startV
    for startV in vs:
        key = (startV[0], (startV[1].x, startV[1].y))
        if not key in moves or not moves[key]:
            moves[key] = list()
            #        print v
        # start BFS in center point
        startPoint = Vec2d(0, 0)
        for i in nx.bfs_tree(grid, (startPoint.x, startPoint.y)):
            curPoint = Vec2d(i)
            if isInReach(curPoint, startPoint, startV[0], maxPosAcc):
                for curV in getVelocities(startV, maxSpeed, maxPosAcc, maxNegAcc):
                    startV = fixVelocity(startV)
                    curV = fixVelocity(curV)
                    p0 = startPoint
                    p1 = startPoint + startV[1] * startV[0]
                    p2 = i - curV[0] * curV[1]
                    p3 = Vec2d(i)
#                    print [p0, p1, p2, p3]
#                    print [startPoint, startV, i, curV]
                    bezier = calculateBezier([deepcopy(p0), deepcopy(p1), deepcopy(p2), deepcopy(p3)])
                    startV = unfixVelocity(startV)
                    curV = unfixVelocity(curV)
#                    print i
                    if not curVelocityReachable(bezier, startV[0], curV[0], maxPosAcc, maxNegAcc):
                        break

                    if not accelerationAllowed(bezier):
                        break

                    takenFields = calculateTakenFields(bezier)

                    if vis:
                        moves[key].append((i, (curV[0], (curV[1].x, curV[1].y)), takenFields, bezier))
                    else:
                        moves[key].append((i, (curV[0], (curV[1].x, curV[1].y)), takenFields))
    return moves


def createGrid(maxSpeed):
    """
    Creates full Moore neighborhood grid graph
    """
    diameter = 2 * maxSpeed + 1
    graph = nx.grid_2d_graph(diameter, diameter)
    for i in xrange(diameter):
        for j in xrange(diameter):
            if i > 0 and j > 0:
                graph.add_edge((i, j), (i - 1, j - 1))
            if i < diameter - 1 and j > 0:
                graph.add_edge((i, j), (i + 1, j - 1))
            if i > 0 and j < diameter - 1:
                graph.add_edge((i, j), (i - 1, j + 1))
            if i < diameter - 1 and j < diameter - 1:
                graph.add_edge((i, j), (i + 1, j + 1))
    return graph


def calculateBezier(points, steps=40):
    """
    Calculate a bezier curve from 4 control points and return a
    list of the resulting points.

    The function uses the forward differencing algorithm described here:
    http://www.niksula.cs.hut.fi/~hkankaan/Homepages/bezierfast.html
    """

    t = 1.0 / steps
    temp = t * t

    f = points[0]
    fd = 3 * (points[1] - points[0]) * t
    fdd_per_2 = 3 * (points[0] - 2 * points[1] + points[2]) * temp
    fddd_per_2 = 3 * (3 * (points[1] - points[2]) + points[3] - points[0]) * temp * t

    fddd = 2 * fddd_per_2
    fdd = 2 * fdd_per_2
    fddd_per_6 = fddd_per_2 / 3.0

    points = []
    for x in xrange(steps):
        points.append(deepcopy(f))
        f += fd + fdd_per_2 + fddd_per_6
        fd += fdd + fddd_per_2
        fdd += fddd
        fdd_per_2 += fddd_per_2
    points.append(deepcopy(f))
    return points


def point(x, y):
    pylab.plot([[x], [y]])


def qq(x, y):
    if (x + y) % 2 == 0: return 1
    else: return sqrt(2)


def arrow(start=(0, 0), vel=(0, (0, 0)), color='b'):
    if vel == (0, (0, 0)):
        xr, yr = 0.1, 0.1
    else:
        if vel[0] == 0:
            sp = 0.1
        else:
            sp = vel[0]
        x = vel[1][0]
        y = vel[1][1]
        xr = sp * x * qq(x, y)
        yr = sp * y * qq(x, y)
    pylab.arrow(start[0], start[1], xr, yr, head_width=0.05, head_length=0.1, color=color)


def get_fig(moves, key):
    global colors, arg
    # draw init speed


    # draw end point
    for i, move in enumerate(moves[key]):
        ax = make_axes()
        arrow(vel=key, color='r')
        endP = move[0]
        endV = move[1]
        arrow(start=endP, vel=endV, color='g')
        taken = move[2]
        bezier = move[3]

        s = "key: {0}\nendP: {1}\nendV: {2}\ntaken: {3}\n".format(key, endP, endV, taken)
#        s = str(endP)
        print s
        pylab.text(-3.3 * arg, 3.3 * arg, s)

        pylab.scatter(zip(*bezier)[0], zip(*bezier)[1], c='g', alpha=.25, edgecolors='none')

        pylab.scatter(zip(*taken)[0], zip(*taken)[1], c='r', s=20, alpha=.75, edgecolors='none')

        pylab.draw()
        pylab.pause(0.0001)
        pylab.clf()


def make_axes():
    ax = pylab.axes([0.025, 0.025, 0.95, 0.95])
    ax.set_xlim(-4 * arg, 4 * arg)
    ax.set_ylim(-4 * arg, 4 * arg)
    ax.xaxis.set_major_locator(pylab.MultipleLocator(1.0))
    ax.xaxis.set_minor_locator(pylab.MultipleLocator(0.1))
    ax.yaxis.set_major_locator(pylab.MultipleLocator(1.0))
    ax.yaxis.set_minor_locator(pylab.MultipleLocator(0.1))
    ax.grid(which='major', axis='x', linewidth=0.75, linestyle='-', color='0.75')
    ax.grid(which='minor', axis='x', linewidth=0.25, linestyle='-', color='0.75')
    ax.grid(which='major', axis='y', linewidth=0.75, linestyle='-', color='0.75')
    ax.grid(which='minor', axis='y', linewidth=0.25, linestyle='-', color='0.75')
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    return ax

if __name__ == "__main__":
    arg = 2
    moves = getAllowedMoves(arg,2,4,True)
    colors = ['aqua', 'black', 'blue', 'fuchsia', 'gray', 'green', 'lime', 'maroon', 'navy', 'olive', 'purple', 'red',
              'silver', 'teal', 'yellow']

    pylab.ion()
    pylab.get_current_fig_manager().window.wm_geometry("1000x1000+0+0")
    pylab.show()

    for key in moves.keys():
        get_fig(moves, key)
