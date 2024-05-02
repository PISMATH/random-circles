from config import *
from math import sqrt

def dist(point1: Point, point2: Point) -> float:
    return sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def pointsInBoundingBox(bound1: Point, bound2: Point, points: set[Point]) -> set[Point]:
    b1x, b1y = bound1
    b2x, b2y = bound2

    minx = min(b1x, b2x)
    maxx = max(b1x, b2x)
    miny = min(b1y, b2y)
    maxy = max(b1y, b2y)
    
    pointsInBox: set[Point] = set()

    for point in points:
        px, py = point
        if minx <= px <= maxx and miny <= py <= maxy:
            pointsInBox.add(point)

    return pointsInBox

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
    
    intersects = pointsInBoundingBox((x1, y1), (x2, y2), {(intersect_x, intersect_y)})
    return pointsInBoundingBox((x3, y3), (x4, y4), intersects)

def intersectLineCircle(line: Line, circle: Circle) -> set[Point]:
    # Unpacking line points
    (x1, y1), (x2, y2) = line

    # Unpacking circle center and radius, ignoring the unused point
    (cx, cy), _, radius = circle

    # Line parametric form coefficients
    dx = x2 - x1
    dy = y2 - y1

    # Calculate quadratic equation coefficients A, B, and C
    A = dx**2 + dy**2
    B = 2 * (dx * (x1 - cx) + dy * (y1 - cy))
    C = (x1 - cx)**2 + (y1 - cy)**2 - radius**2

    # Discriminant
    D = B**2 - 4 * A * C

    # Determining the number of intersection points based on the discriminant
    if D < 0:
        return set()  # No intersection
    elif D == 0:
        t = -B / (2 * A)
        intersections = {(x1 + t * dx, y1 + t * dy)}
    else:
        sqrt_D = D**0.5
        t1 = (-B + sqrt_D) / (2 * A)
        t2 = (-B - sqrt_D) / (2 * A)
        intersections = {(x1 + t1 * dx, y1 + t1 * dy), (x1 + t2 * dx, y1 + t2 * dy)}

    return pointsInBoundingBox((x1, y1), (x2, y2), intersections)
    
def convertGeoPointToScreenCoords(point: Point):
    x = point[0] * scale + screen_width / 2
    y = point[1] * scale + screen_height / 2
    return x, y
