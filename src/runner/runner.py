import sys
import time

sys.path.append('../')
from communication.robot import Robot
from board.board import Board
from communication.client import get_move
from time import sleep
from optparse import OptionParser


def read_command_line_args():
    parser = OptionParser()
    parser.add_option("-v", "--visualize", action="store_true",
        dest="visualize", help="visualize simulation")
    parser.add_option("-s", "--save", action="store_true",
        dest="save", help="save history to file")
    parser.add_option("-c", "--config", action="store",
        dest="configPath", help="path to config file", type="string")
    (options, args) = parser.parse_args()
    return options.visualize, options.save, options.configPath

def readRobot(args):
    '''
    constructs a Robot object from a line from config file
    '''
    robot = Robot()
    robot.setId(args[0])
    robot.setOwnPosition(eval(args[1]))
    robot.destination = eval(args[2])
    return robot


def shouldContinue(robots):
    """
    returns false if all robots have reached their destinations
    """
    return filter(lambda (r, u): r.getOwnPosition() not in r.destination, robots)

if __name__ == "__main__":
    visualize, save, configPath = read_command_line_args()
    config = open(configPath)
    board = Board(config.readline().strip('\n'), visualize)
    robots = []
    for line in config.read().splitlines():
        args = line.split()
        robot = readRobot(args)
        robots.append((robot, args[3]))
        board.addRobot(robot.position, args[0])
    while shouldContinue(robots):
        print map(lambda t: t[0].position, robots)
        for robot, url in robots:
            robot.robots = map(lambda r: r[0].position, robots)
            robot.allowedMoves = board.getAllowedMoves(robot.position)
            newPosition = get_move(url, robot)
            board.moveRobot(robot.position, newPosition)
            robot.setOwnPosition(newPosition)
        if visualize:
            sleep(1)
            board.refreshBoard()
    if save:
        filename = 'history/' + str(time.time())
        print filename
        board.dumpHistory(filename)

