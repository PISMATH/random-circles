import random
from config import *
from distanceFunctions import *
from isNew import addCircles, addLines, addPoints, circleIsAllowed, lineIsAllowed

def addCircle(points: set[Point], circles: set[Circle], lines: set[Line], center: Point, secondpoint: Point):
    new_circle: Circle = (center, secondpoint, dist(center, secondpoint))
    
    if not circleIsAllowed(circles, new_circle):
        return

    for circle in circles:
        point_intersects = intersectCircles(circle, new_circle)
        if DebugMode:
            print(f"In random circle, points {point_intersects} were added to the list. These points are from circles {new_circle}, {circle}")
        addPoints(points, point_intersects)

    for line in lines:
        point_intersects = intersectLineCircle(line, new_circle)
        if DebugMode:
            print(f"In random circle, points {point_intersects} were added to the list. These points are from circle {new_circle} and line {line}")
        addPoints(points, point_intersects)

    addCircles(circles, {new_circle})

def addLine(points: set[Point], circles: set[Circle], lines: set[Line], point1: Point, point2: Point):
    new_line: Line = (point1, point2)

    if not lineIsAllowed(lines, new_line):
        return

    for circle in circles:
        point_intersects = intersectLineCircle(new_line, circle)
        addPoints(points, point_intersects)

    for line in lines:
        point_intersects = intersectLines(line, new_line)
        addPoints(points, point_intersects)

    addLines(lines, {new_line})

def addRandomCircle(points: set[Point], circles: set[Circle], lines: set[Line]):
    center = random.choice(list(points))

    points.remove(center)
    secondpoint = random.choice(list(points))
    points.add(center)
    addCircle(points, circles, lines, center, secondpoint)

def addRandomLine(points: set[Point], circles: set[Circle], lines: set[Line]):
    point1 = random.choice(list(points))

    points.remove(point1)
    point2 = random.choice(list(points))
    points.add(point1)
    addLine(points, circles, lines, point1, point2)
    
def addNewRandomObject(points: set[Point], circles: set[Circle], lines: set[Line]):
    if random.random() < circle_odds:
        addRandomCircle(points, circles, lines)

    else:
        addRandomLine(points, circles, lines)

def executeNeuralNetAction(points: set[Point], circles: set[Circle], lines: set[Line], neuralOutputs):
    circlePreference, linePreference, p1x, p1y, p2x, p2y = neuralOutputs
    p1 = nearestPoint(points, (p1x, p1y))
    p2 = nearestPoint(points, (p2x, p2y))
    if p1 != p2:
        if circlePreference > linePreference:
            addCircle(points, circles, lines, p1, p2)
        
        else:
            addLine(points, circles, lines, p1, p2)