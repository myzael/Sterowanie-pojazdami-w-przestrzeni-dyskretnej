import sys
from threading import Thread
from matplotlib import pylab

sys.path.append("C:\Kuba\Coding\Studies\Agenty\Sterowanie-pojazdami-w-przestrzeni-dyskretnej")

import httplib
import sys
import time
from src.board.physicsBoard import PhysicsBoard
from src.communication.client import get_move
from src.communication.robot import Robot

sys.path.append('../')
from time import sleep
from optparse import OptionParser
from networkx import shortest_path_length

EXPONENT = 7


def read_command_line_args():
    parser = OptionParser()
    parser.add_option("-v", "--visualize", action="store_true",
                      dest="visualize", help="visualize simulation")
    parser.add_option("-s", "--save", action="store_true",
                      dest="save", help="save history to file")
    parser.add_option("-c", "--config", action="store",
                      dest="configPath", help="path to config file", type="string")
    parser.add_option("-r", "--regenerate", action="store_true",
                      dest="regenerate", help="regenerate physics")
    (options, args) = parser.parse_args()
    return options.visualize, options.save, options.configPath, options.regenerate


def readRobot(args):
    '''
    constructs a Robot object from a line from config file
    '''
    robot = Robot()
    robot.setId(args[0])
    init = eval(args[1])
    robot.setOwnPosition(init[0])
    robot.destination = eval(args[2])
    robot.setSpeed(init[1])
    robot.setVelocity(init[2])
    return robot


def shouldContinue(robots):
    """
    returns false if all robots have reached their destinations
    """
    return filter(lambda (r, u): r.getOwnPosition() not in r.destination, robots)


def calculate_shortest_path_length(robots, board):
    lengths = dict()
    for robot in robots:
        lengths[robot.id] = min(
            map(lambda dest: shortest_path_length(board.graph, robot.position, dest), robot.destination))
    return lengths


def parse_config(board, config):
    robots = []
    for line in config.read().splitlines():
        args = line.split()
        robot = readRobot(args)
        robots.append((robot, args[3]))
        direction = eval(args[1])[2]
        speed = eval(args[1])[1]
        board.addRobot(robot.position, args[0], direction, speed)
    return robots


def move(board, robot, robots, statistics, url):
    robot.robots = map(lambda r: r[0].position, robots)
    robot.allowedMoves = board.getAllowedMoves(robot.position)
    newPosition, newSpeed, newVelocity = get_move(url, robot)
    board.moveRobot(robot.position, newPosition, newSpeed, newVelocity)
    if robot.position != newPosition or robot.position not in robot.destination:
        statistics[robot.id] = statistics.get(robot.id, 0) + 1
    robot.setOwnPosition(newPosition)
    robot.setVelocity(newVelocity)
    robot.setSpeed(newSpeed)


def save_history(board):
    filename = 'history/' + str(time.time())
    print filename
    board.dumpHistory(filename)


def calculate__metric(shortest_paths, statistics):
    metric = sum(map(lambda id: (statistics[id] - shortest_paths[id]) ** EXPONENT, shortest_paths.keys()))
    return metric


def initialize(board, robots):
    for robot, url in robots:
        robot.robots = map(lambda r: r[0].position, robots)
        robot.allowedMoves = board.getAllowedMoves(robot.position)
        try:
            get_move(url, robot)
        except ValueError:
            pass
        except httplib.BadStatusLine:
            pass


def ask_robot_async(threads, robot, url):
    thread = Thread(target=ask_robot, args=(robot, url))
    threads.append(thread)
    thread.start()


def ask_robot(robot, url):
    robot.robots = map(lambda r: r[0].position, robots)
    robot.allowedMoves = board.getAllowedMoves(robot.position)
    newPosition, newSpeed, newVelocity = get_move(url, robot)
    moves.append((robot, newPosition, newSpeed, newVelocity))


if __name__ == "__main__":
    visualize, save, configPath, regenerate = read_command_line_args()
    config = open(configPath)
    board = PhysicsBoard(config.readline().strip('\n'), '../../board', 4, 4, 6, visualize)
    pylab.get_current_fig_manager().window.wm_geometry("1000x1000+0+0")
    statistics = dict()
    robots = parse_config(board, config)
    shortest_paths = calculate_shortest_path_length(map(lambda r: r[0], robots), board)
    initialize(board, robots)
    print "initialized"
    while shouldContinue(robots):
        moves = []
        for robot, url in robots:
            threads = []
            ask_robot_async(threads, robot, url)
        for t in threads: t.join()
        for robot, newPosition, newSpeed, newVelocity in moves:
            board.moveRobot(robot.position, newPosition, newSpeed, newVelocity)
            if robot.position != newPosition or robot.position not in robot.destination:
                statistics[robot.id] = statistics.get(robot.id, 0) + 1
            robot.setOwnPosition(newPosition)
            robot.setVelocity(newVelocity)
            robot.setSpeed(newSpeed)
        if visualize:
            sleep(0.1)
            board.refreshBoard()
    print shortest_paths
    print statistics
    print calculate__metric(shortest_paths, statistics)
    if save:
        save_history(board)
    raw_input("press enter to exit")

