from math import sqrt
import networkx as nx
from vect2d import *

__author__ = 'Myzael'
# TODO: rewrite to use point and vector classes?
def distance(p1, p2):
    return p1.get_distance(p2)


def isInReach(curPoint, startPoint, startV, maxPosAcc):
    # dist(curPoint-startPoint) <= |startV| * t + 1/2 * maxPosAcc * t^2
    return distance(curPoint, startPoint) <= startV[0] + 0, 5 * maxPosAcc


def getStartVs(maxSpeed):
    for startSpeed in xrange(maxSpeed + 1):
        for startVDirX in xrange(-1, 2):
            for startVDirY in xrange(-1, 2):
                yield startSpeed, Vec2d(startVDirX, startVDirY)


def getVelocities(curV, maxSpeed, maxPosAcc, maxNegAcc):
    for v in getStartVs(maxSpeed):
        if curV[0] + maxPosAcc > v[0] > curV[0] - maxNegAcc:
            yield v


def curVelocityReachable(trajectory):
    return True


def calculateTakenFields(trajectory):
    taken = None
    return taken


def accelerationAllowed(trajectory):
    return True


def getAllowedMoves(maxSpeed, maxPosAcc=1, maxNegAcc=2):
    """
    Calculates and returns tbe list of allowed moves.
    List contains tuples of the following elements:
    """

    moves = dict()
    grid = createGrid(maxSpeed)

    for v in getStartVs(maxSpeed):
        key = (v[0], (v[1].x, v[1].y))
        moves[key] = list()
#        print v
        # start BFS in center point
        startPoint = Vec2d(maxSpeed, maxSpeed)
        for i in nx.bfs_tree(grid, (startPoint.x, startPoint.y)):
            curPoint = Vec2d(i)
            if isInReach(curPoint, startPoint, v, maxPosAcc):
                for curV in getVelocities(curV=v, maxSpeed=maxSpeed, maxPosAcc=maxPosAcc, maxNegAcc=maxNegAcc):
                    p0 = startPoint
                    p1 = startPoint + v[1]
                    p2 = i - curV[1]
                    p3 = Vec2d(i)
#                    print [p0, p1, p2, p3]
                    bezier = calculateBezier([p0, p1, p2, p3])
                    if not curVelocityReachable(trajectory=bezier):
                        break

                    if not accelerationAllowed(trajectory=bezier):
                        break

                    takenFields = calculateTakenFields(trajectory=bezier)

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


def calculateBezier(points, steps=30):
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
        points.append(f)
        f += fd + fdd_per_2 + fddd_per_6
        fd += fdd + fddd_per_2
        fdd += fddd
        fdd_per_2 += fddd_per_2
    points.append(f)
    return points

if __name__ == "__main__":
    moves = getAllowedMoves(2)
    for key in moves.keys():
        print key, moves[key]
