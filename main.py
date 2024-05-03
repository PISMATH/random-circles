import pygame

from config import *
from distanceFunctions import *
from newObject import addNewRandomObject, addRandomCircle, addRandomLine
from isNew import addPoints

def renderEverything(lines: set[Line], points: set[Point], circles: set[Circle], scale, screen):
    screen.fill(background_color)

    for circle in circles:
        center, _, r = circle
        x, y = convertGeoPointToScreenCoords(center, scale)
        rad = r * scale
        pygame.draw.circle(screen, circle_color, (x, y), rad, circle_width)
    
    for line in lines:
        p1, p2 = line
        point1 = convertGeoPointToScreenCoords(p1, scale)
        point2 = convertGeoPointToScreenCoords(p2, scale)
        pygame.draw.line(screen, line_color, point1, point2, line_width)

    for point in points:
        x, y = convertGeoPointToScreenCoords(point, scale)
        pygame.draw.circle(screen, point_color, (x, y), points_size)

    pygame.display.flip()

def main():
    screen_scale = scale
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    running = True
    points = inital_points.copy()
    circles: set[Circle] = set()
    lines: set[Line] = set()

    stateHistory: list[tuple[set[Point], set[Circle], set[Line]]] = [(points.copy(), circles.copy(), lines.copy())]

    historyChanged = False
    clickMode = 0 # 0 is new point, 1 is delete nearest point
    
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
            
                elif event.key == pygame.K_l:
                    addRandomLine(points, circles, lines)
                    stateHistory.append((points.copy(), circles.copy(), lines.copy()))
                
                elif event.key == pygame.K_c:
                    addRandomCircle(points, circles, lines)
                    stateHistory.append((points.copy(), circles.copy(), lines.copy()))
                
                elif event.key == pygame.K_SPACE:
                    addNewRandomObject(points, circles, lines)
                    stateHistory.append((points.copy(), circles.copy(), lines.copy()))

                
                elif event.key == pygame.K_z:
                    if len(stateHistory) > 0:
                        historyChanged = True
                        points, circles, lines = stateHistory.pop()
                
                elif event.key == pygame.K_0:
                    clickMode = 0
                
                elif event.key == pygame.K_1:
                    clickMode = 1
                
                elif event.key == pygame.K_EQUALS:
                    screen_scale += 10

                elif event.key == pygame.K_MINUS:
                    if screen_scale > 10:
                        screen_scale -= 10
                # check control+z
                if historyChanged:
                    historyChanged = False
                else:
                    stateHistory.append((points.copy(), circles.copy(), lines.copy()))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if clickMode == 0:
                    clickPos = convertScreenCoordsToGeoPoint(pygame.mouse.get_pos(), screen_scale)
                    if DebugMode:
                        print(f"click at {clickPos} and mode 0")
                    addPoints(points, {clickPos})
                    stateHistory.append((points.copy(), circles.copy(), lines.copy()))
                
                if clickMode == 1:

                    clickPos = convertScreenCoordsToGeoPoint(pygame.mouse.get_pos(), screen_scale)
                    if DebugMode:
                        print(f"click at {clickPos} and mode 1")
                    nearest_point = nearestPoint(points, clickPos)
                    if nearest_point != None:
                        points.remove(nearest_point)
                        stateHistory.append((points.copy(), circles.copy(), lines.copy()))
                
                  
        renderEverything(lines, points, circles, screen_scale, screen)
        

main()
