from config import *
import math

from rulePlugins import circleRulesPlugin, lineRulesPlugin, pointRulesPlugin

def pointIsNew(points: set[Point], point: Point) -> bool:
    x1, y1 = point
    for point1 in points:
        x2, y2 = point1
        if (x1 - x2) ** 2 + (y1 - y2) ** 2 < point_rounding ** 2:
            return False
    return True


def circleIsNew(circles: set[Circle], circle: Circle) -> bool:
    center1, _, r1 = circle
    for circle1 in circles:
        center2, _, r2 = circle1
        if not pointIsNew({center1}, center2) and abs(r1 - r2) < circle_rounding:
            return False
    return True

def lineIsNew(lines: set[Line], line: Line) -> bool:
    p1, p2 = line
    for line1 in lines:
        p3, p4 = line1
        if not (pointIsNew({p1}, p3) or pointIsNew({p2}, p4)):
            return False
    return True

def pointIsAllowed(points: set[Point], point: Point) -> bool:
    return pointIsNew(points, point) and pointRulesPlugin(points, point)


def circleIsAllowed(circles: set[Circle], circle: Circle) -> bool:
    return circleIsNew(circles, circle) and circleRulesPlugin(circles, circle)

def lineIsAllowed(lines: set[Line], line: Line) -> bool:
    return lineIsNew(lines, line) and lineRulesPlugin(lines, line)


def addPoints(points: set[Point], new_points: set[Point]) -> None:
    for new_point in new_points:
        if pointIsAllowed(points, new_point):
            points.add(new_point)

def addCircles(circles: set[Circle], new_circles: set[Circle]) -> None:
    for new_circle in new_circles:
        if circleIsAllowed(circles, new_circle):
            circles.add(new_circle)  

def addLines(lines: set[Line], new_lines: set[Line]) -> None:
    for new_line in new_lines:
        if lineIsAllowed(lines, new_line):
            lines.add(new_line)
