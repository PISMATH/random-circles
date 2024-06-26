from config import *
 
from rule_plugins import circle_rules_plugin, line_rules_plugin, point_rules_plugin
 
def point_is_new(points: set[Point], point: Point) -> bool:
    x1, y1 = point
    for point1 in points:
        x2, y2 = point1
        if (x1 - x2) ** 2 + (y1 - y2) ** 2 < point_rounding ** 2:
            return False
    return True
 
 
def circle_is_new(circles: set[Circle], circle: Circle) -> bool:
    center1, _, r1 = circle
    for circle1 in circles:
        center2, _, r2 = circle1
        if not point_is_new({center1}, center2) and abs(r1 - r2) < circle_rounding:
            return False
    return True
 
def line_is_new(lines: set[Line], line: Line) -> bool:
    p1, p2 = line
    for line1 in lines:
        p3, p4 = line1
        if not (point_is_new({p1}, p3) or point_is_new({p2}, p4)):
            return False
    return True
 
def point_is_allowed(points: set[Point], point: Point) -> bool:
    return point_is_new(points, point) and point_rules_plugin(points, point)
 
 
def circle_is_allowed(circles: set[Circle], circle: Circle) -> bool:
    return circle_is_new(circles, circle) and circle_rules_plugin(circles, circle)
 
def line_is_allowed(lines: set[Line], line: Line) -> bool:
    return line_is_new(lines, line) and line_rules_plugin(lines, line)
 
 
def add_points(points: set[Point], new_points: set[Point]) -> None:
    for new_point in new_points:
        if point_is_allowed(points, new_point):
            points.add(new_point)
 
def add_circles(circles: set[Circle], new_circles: set[Circle]) -> None:
    for new_circle in new_circles:
        if circle_is_allowed(circles, new_circle):
            circles.add(new_circle)
 
def add_lines(lines: set[Line], new_lines: set[Line]) -> None:
    for new_line in new_lines:
        if line_is_allowed(lines, new_line):
            lines.add(new_line)
