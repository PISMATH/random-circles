import random
from config import *
from distance_functions import *
from is_new import add_circles, add_lines, add_points, circle_is_allowed, line_is_allowed
 
def add_circle(points: set[Point], circles: set[Circle], lines: set[Line], center: Point, secondpoint: Point):
    new_circle: Circle = (center, secondpoint, dist(center, secondpoint))
     
    if not circle_is_allowed(circles, new_circle):
        return
 
    for circle in circles:
        point_intersects = intersect_circles(circle, new_circle)
        if DebugMode:
            print(f"In random circle, points {point_intersects} were added to the list. These points are from circles {new_circle}, {circle}")
        add_points(points, point_intersects)
 
    for line in lines:
        point_intersects = intersect_line_circle(line, new_circle)
        if DebugMode:
            print(f"In random circle, points {point_intersects} were added to the list. These points are from circle {new_circle} and line {line}")
        add_points(points, point_intersects)
 
    add_circles(circles, {new_circle})
 
def add_line(points: set[Point], circles: set[Circle], lines: set[Line], point1: Point, point2: Point):
    new_line: Line = (point1, point2)
 
    if not line_is_allowed(lines, new_line):
        return
 
    for circle in circles:
        point_intersects = intersect_line_circle(new_line, circle)
        add_points(points, point_intersects)
 
    for line in lines:
        point_intersects = intersect_lines(line, new_line)
        add_points(points, point_intersects)
 
    add_lines(lines, {new_line})
 
def add_random_circle(points: set[Point], circles: set[Circle], lines: set[Line]):
    center = random.choice(list(points))
 
    points.remove(center)
    secondpoint = random.choice(list(points))
    points.add(center)
    add_circle(points, circles, lines, center, secondpoint)
 
def add_random_line(points: set[Point], circles: set[Circle], lines: set[Line]):
    point1 = random.choice(list(points))
 
    points.remove(point1)
    point2 = random.choice(list(points))
    points.add(point1)
    add_line(points, circles, lines, point1, point2)
     
def add_new_random_object(points: set[Point], circles: set[Circle], lines: set[Line]):
    if random.random() < circle_odds:
        add_random_circle(points, circles, lines)
 
    else:
        add_random_line(points, circles, lines)
 
def execute_neural_net_action(points: set[Point], circles: set[Circle], lines: set[Line], neural_outputs):
    circle_preference, line_preference, p1x, p1y, p2x, p2y = neural_outputs
    p1 = nearest_point(points, (p1x, p1y))
    p2 = nearest_point(points, (p2x, p2y))
    if p1 != p2:
        if circle_preference > line_preference:
            add_circle(points, circles, lines, p1, p2)
         
        else:
            add_line(points, circles, lines, p1, p2)
