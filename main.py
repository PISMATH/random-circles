import pygame

from config import *
from distanceFunctions import *
from newObject import addNewRandomObject, addRandomCircle, addRandomLine


def renderEverything(lines: set[Line], points: set[Point], circles: set[Circle], screen):
    screen.fill(background_color)

    for circle in circles:
        center, _, r = circle
        x, y = convertGeoPointToScreenCoords(center)
        rad = r * scale
        pygame.draw.circle(screen, circle_color, (x, y), rad, circle_width)
    
    for line in lines:
        p1, p2 = line
        point1 = convertGeoPointToScreenCoords(p1)
        point2 = convertGeoPointToScreenCoords(p2)
        pygame.draw.line(screen, line_color, point1, point2, line_width)

    for point in points:
        x, y = convertGeoPointToScreenCoords(point)
        pygame.draw.circle(screen, point_color, (x, y), points_size)

    pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    running = True
    points = inital_points.copy()
    circles: set[Circle] = set()
    lines: set[Line] = set()

    stateHistory: list[tuple[set[Point], set[Circle], set[Line]]] = [(points.copy(), circles.copy(), lines.copy())]

    historyChanged = False
    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    points = inital_points.copy()
                    circles = set()
                    lines = set()

                    stateHistory = [(points.copy(), circles.copy(), lines.copy())]

                if event.key == pygame.K_l:
                    addRandomLine(points, circles, lines)
                    stateHistory.append((points.copy(), circles.copy(), lines.copy()))
                
                elif event.key == pygame.K_c:
                    addRandomCircle(points, circles, lines)
                    stateHistory.append((points.copy(), circles.copy(), lines.copy()))
                
                elif event.key == pygame.K_SPACE:
                    addNewRandomObject(points, circles, lines)
                    stateHistory.append((points.copy(), circles.copy(), lines.copy()))

                # check control+z
                elif event.key == pygame.K_z:
                    if len(stateHistory) > 0:
                        historyChanged = True
                        points, circles, lines = stateHistory.pop()
                if historyChanged:
                    historyChanged = False
                else:
                    stateHistory.append((points.copy(), circles.copy(), lines.copy()))
                
        renderEverything(lines, points, circles, screen)
        

main()
