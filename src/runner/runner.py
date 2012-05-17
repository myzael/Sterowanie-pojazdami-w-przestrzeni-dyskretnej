import sys

sys.path.append('../')
from communication.robot import Robot
from board.board import Board
from communication.client import get_move

if __name__ == "__main__":
    config = open('config')
    board = Board(config.readline().strip('\n'))
    robots = []
    for line in config.read().splitlines():
        args = line.split()
        robot = Robot()
        robot.setId(args[0])
        robot.setOwnPosition(eval(args[1]))
        robot.destination = eval(args[2])
        robots.append((robot, args[3]))
        board.addRobot(robot.position, args[0])
    while filter(lambda (r, u): r.getOwnPosition() not in r.destination, robots):
        raw_input("Press Enter to continue")
        print map(lambda t: t[0].position, robots)
        for robot, url in robots:
            robot.robots = map(lambda r: r[0].position, robots)
            robot.allowedMoves = board.getAllowedMoves(robot.position)
            position = get_move(url, robot)
            board.moveRobot(robot.position, position)
            robot.setOwnPosition(position)
        board.refreshBoard()

