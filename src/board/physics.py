from math import floor
from math import ceil
import networkx as nx
from vect2d import *
from copy import deepcopy

__author__ = 'Myzael'
# TODO: rewrite to use point and vector classes?
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

    maxSpeed = curSpeed + maxPosAcc
    minSpeed = curSpeed - maxNegAcc
    speedGood = minSpeed <= curSpeed <= maxSpeed

    accGood = -maxNegAcc <= curSpeed - startSpeed <= maxPosAcc
    return lenghtGood and speedGood and accGood


def calculateTakenFields(trajectory):
    taken = set()
    for point in trajectory:
        surrounding = (Vec2d(x, y) for x, y in [(floor(point.x), floor(point.y)),
                                                (floor(point.x), ceil(point.y)),
                                                (ceil(point.x), floor(point.y)),
                                                (ceil(point.x), ceil(point.y))])
        for s in surrounding:
            if s.get_dist_sqrd(point) <= 2:
                taken.add((int(s.x), int(s.y)))

    return list(taken)


def accelerationAllowed(trajectory):
    return True


def getAllowedMoves(maxSpeed, maxPosAcc=1, maxNegAcc=2):
    """
    Calculates and returns tbe list of allowed moves.
    List contains tuples of the following elements:
    """

    moves = dict()
    grid = createGrid(maxSpeed)

    vs = getStartVs(maxSpeed)
#    for startV in vs:
#        print startV
    for startV in vs:
        key = (startV[0], (startV[1].x, startV[1].y))
        if not key in moves or not moves[key]:
            moves[key] = list()
        #        print v
        # start BFS in center point
        startPoint = Vec2d(maxSpeed, maxSpeed)
        for i in nx.bfs_tree(grid, (startPoint.x, startPoint.y)):
            curPoint = Vec2d(i)
            if isInReach(curPoint, startPoint, startV[0], maxPosAcc):
                for curV in getVelocities(startV, maxSpeed, maxPosAcc, maxNegAcc):
                    p0 = startPoint
                    p1 = startPoint + startV[1]*startV[0]
                    p2 = i - curV[0]*curV[1]
                    p3 = Vec2d(i)
                    print [p0, p1, p2, p3]
                    bezier = calculateBezier([deepcopy(p0), deepcopy(p1), deepcopy(p2), deepcopy(p3)])
                    if not curVelocityReachable(bezier, startV[0], curV[0], maxPosAcc, maxNegAcc):
                        break

                    if not accelerationAllowed(bezier):
                        break

                    takenFields = calculateTakenFields(bezier)

                    moves[key].append((i, (curV[1].x, curV[1].y), takenFields))
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


def calculateBezier(points, steps=60):
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

if __name__ == "__main__":
    moves = getAllowedMoves(2)
    for key in moves.keys():
            for move in moves[key]:
                print "endP: {0}, endV: {1}, taken: {2}".format(move[0], move[1], move[2])
    print ""

