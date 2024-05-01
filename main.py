import random
import pygame

from math import sqrt
from config import *

Point = tuple[float, float]
Circle = tuple[Point, Point, float]

points: set[Point] = {(-1, 0), (1, 0)}
circles: set[Circle] = set()

def dist(point1: Point, point2: Point) -> float:
    return sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def intersectCircle(circle1: Circle, circle2: Circle) -> set[Point]:
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

def drawRandomCircle(points: set[Point], circles: set[Circle]):
    center = random.choice(list(points))

    points.remove(center)
    secondpoint = random.choice(list(points))
    points.add(center)

    new_circle: Circle = (center, secondpoint, dist(center, secondpoint))
    
    for circle in circles:
        point_intersects = intersectCircle(circle, new_circle)
        points.update(point_intersects)

    circles.add(new_circle)

def convertGeoPointToScreenCoords(point: Point):
    x = point[0] * scale + screen_width / 2
    y = point[1] * scale + screen_height / 2
    return x, y

def renderEverything(points: set[Point], circles: set[Circle], screen):
    screen.fill('BLACK')

    for circle in circles:
        center, _, r = circle
        x, y = convertGeoPointToScreenCoords(center)
        rad = r * scale
        pygame.draw.circle(screen, circle_color, (x, y), rad, circle_width)

    for point in points:
        x, y = convertGeoPointToScreenCoords(point)
        print(x, y)
        pygame.draw.circle(screen, point_color, (x, y), points_size)

    pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                drawRandomCircle(points, circles)
        renderEverything(points, circles, screen)
        

main()