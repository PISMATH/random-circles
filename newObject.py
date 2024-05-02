import random
from config import *
from distanceFunctions import *

def addRandomCircle(points: set[Point], circles: set[Circle], lines: set[Line]):
    center = random.choice(list(points))

    points.remove(center)
    secondpoint = random.choice(list(points))
    points.add(center)

    new_circle: Circle = (center, secondpoint, dist(center, secondpoint))
    
    for circle in circles:
        point_intersects = intersectCircles(circle, new_circle)
        points.update(point_intersects)

    for line in lines:
        point_intersects = intersectLineCircle(line, new_circle)
        points.update(point_intersects)

    circles.add(new_circle)

def addRandomLine(points: set[Point], circles: set[Circle], lines: set[Line]):
    point1 = random.choice(list(points))

    points.remove(point1)
    point2 = random.choice(list(points))
    points.add(point1)

    new_line: Line = (point1, point2)
    
    for circle in circles:
        point_intersects = intersectLineCircle(new_line, circle)
        points.update(point_intersects)

    for line in lines:
        point_intersects = intersectLines(line, new_line)
        points.update(point_intersects)

    lines.add(new_line)

def addNewRandomObject(points: set[Point], circles: set[Circle], lines: set[Line]):
    if random.random() < circle_odds:
        addRandomCircle(points, circles, lines)

    else:
        addRandomLine(points, circles, lines)

