
import pygame
from pygame.draw import line

from config import *
from distanceFunctions import *
from newObject import addNewRandomObject, addRandomCircle, addRandomLine

points: set[Point] = {(-1, 0), (1, 0)}
circles: set[Circle] = set()
lines: set[Line] = set()

def renderEverything(points: set[Point], circles: set[Circle], screen):
    screen.fill('BLACK')

    for circle in circles:
        center, _, r = circle
        x, y = convertGeoPointToScreenCoords(center)
        rad = r * scale
        pygame.draw.circle(screen, circle_color, (x, y), rad, circle_width)
    
    for line in lines:
        p1, p2 = line
        point1 = convertGeoPointToScreenCoords(p1)
        point2 = convertGeoPointToScreenCoords(p2)
        pygame.draw.line(screen, circle_color, point1, point2, line_width)
    for point in points:
        x, y = convertGeoPointToScreenCoords(point)
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
                if event.key == pygame.K_l:
                    addRandomLine(points, circles, lines)
                
                elif event.key == pygame.K_c:
                    addRandomCircle(points, circles, lines)
                
                elif event.key == pygame.K_SPACE:
                    addNewRandomObject(points, circles, lines)
                
        renderEverything(points, circles, screen)
        

main()