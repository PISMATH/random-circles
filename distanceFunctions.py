from config import *
from math import sqrt

def dist(point1: Point, point2: Point) -> float:
    return sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def intersectCircles(circle1: Circle, circle2: Circle) -> set[Point]:
    center1, _, radius1 = circle1
    center2, _, radius2 = circle2

    d = dist(center1, center2)

    if d == 0 and radius1 == radius2:
        # Coincident circles do not have discrete intersection points
        return set()
    
    if d > radius1 + radius2 or d < abs(radius1 - radius2):
        # No intersection
        return set()

    # Adjust for precision issues to ensure sqrt receives a non-negative argument
    a = (radius1**2 - radius2**2 + d**2) / (2 * d)
    h_square = radius1**2 - a**2
    if h_square < 0:
        return set()  # To handle precision issues that might lead to a small negative number

    h = sqrt(h_square)
    midpoint = ((center1[0] + a * (center2[0] - center1[0]) / d),
                (center1[1] + a * (center2[1] - center1[1]) / d))

    intersection1 = ((midpoint[0] + h * (center2[1] - center1[1]) / d),
                     (midpoint[1] - h * (center2[0] - center1[0]) / d))
    intersection2 = ((midpoint[0] - h * (center2[1] - center1[1]) / d),
                     (midpoint[1] + h * (center2[0] - center1[0]) / d))

    return set([intersection1, intersection2])

def intersectLines(line1: Line, line2: Line) -> set[Point]:
    # Extract points from lines
    (x1, y1), (x2, y2) = line1
    (x3, y3), (x4, y4) = line2

    # Compute determinants for the line equations
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denom == 0:
        return set()  # Lines are parallel or identical

    # Calculate the intersection point
    intersect_x = ((x1*y2 - y1*x2)*(x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4)) / denom
    intersect_y = ((x1*y2 - y1*x2)*(y3 - y4) - (y1 - y2)*(x3*y4 - y3*x4)) / denom

    # Check if the intersection point is within both line segments
    if min(x1, x2) <= intersect_x <= max(x1, x2) and min(y1, y2) <= intersect_y <= max(y1, y2) \
       and min(x3, x4) <= intersect_x <= max(x3, x4) and min(y3, y4) <= intersect_y <= max(y3, y4):
        return {(intersect_x, intersect_y)}
    return set()

def intersectLineCircle(line: Line, circle: Circle) -> set[Point]:
    # Extract circle info
    (cx, cy), _, r = circle
    # Extract line info
    (x1, y1), (x2, y2) = line

    # Line equation coefficients
    A = y2 - y1
    B = x1 - x2
    C = A*x1 + B*y1 - (A*cx + B*cy)

    # Finding intersection points
    discriminant = r**2 * (A**2 + B**2) - C**2
    if discriminant < 0:
        return set()  # No real solutions, no intersection

    # Line intersects the circle at least at one point
    sqrt_discriminant = sqrt(discriminant)
    t1 = (-B*C - A*sqrt_discriminant) / (A**2 + B**2)
    t2 = (-B*C + A*sqrt_discriminant) / (A**2 + B**2)
    x_inter1 = cx + t1
    y_inter1 = cy + t2
    x_inter2 = cx + t1
    y_inter2 = cy + t2

    # Check if the intersection points are within the line segment
    result = set()
    if min(x1, x2) <= x_inter1 <= max(x1, x2) and min(y1, y2) <= y_inter1 <= max(y1, y2):
        result.add((x_inter1, y_inter1))
    if min(x1, x2) <= x_inter2 <= max(x1, x2) and min(y1, y2) <= y_inter2 <= max(y1, y2):
        result.add((x_inter2, y_inter2))
    return result
    
def convertGeoPointToScreenCoords(point: Point):
    x = point[0] * scale + screen_width / 2
    y = point[1] * scale + screen_height / 2
    return x, y