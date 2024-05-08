import pygame
 
from config import *
from distance_functions import *
from new_object import add_new_random_object, add_random_circle, add_random_line
from is_new import add_points
 
def render_everything(lines: set[Line], points: set[Point], circles: set[Circle], scale, screen):
    screen.fill(background_color)
 
    for circle in circles:
        center, _, r = circle
        x, y = convert_geo_point_to_screen_coords(center, scale)
        rad = r * scale
        pygame.draw.circle(screen, circle_color, (x, y), rad, circle_width)
     
    for line in lines:
        p1, p2 = line
        point1 = convert_geo_point_to_screen_coords(p1, scale)
        point2 = convert_geo_point_to_screen_coords(p2, scale)
        pygame.draw.line(screen, line_color, point1, point2, line_width)
 
    for point in points:
        x, y = convert_geo_point_to_screen_coords(point, scale)
        pygame.draw.circle(screen, point_color, (x, y), points_size)
 
    pygame.display.flip()
 
def tokenize_state(points: set[Point], circles: set[Circle], lines: set[Line]):
    if len(points) > 50 or len(circles) > 50 or len(lines) > 50:
        return False
     
    state_list = []
     
    for point in points:
        state_list.extend(point)
     
    for _ in range(50 - len(points)):
        state_list.extend([0] * 2)
     
    for circle in circles:
        p1, _, r = circle
        state_list.extend(p1)
        state_list.append(r)
 
    for _ in range(50 - len(circles)):
        state_list.extend([0] * 3)
 
    for line in lines:
        p1, p2 = line
        state_list.extend(p1)
        state_list.extend(p2)
 
    for _ in range(50 - len(lines)):
        state_list.extend([0] * 4)
     
    return state_list
 
def neural_net_loss_funtion(points: set[Point], circles: set[Circle], lines: set[Line], system_outputs):
    pass
 
def main():
    screen_scale = scale
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    running = True
    points = inital_points.copy()
    circles: set[Circle] = set()
    lines: set[Line] = set()
 
    state_history: list[tuple[set[Point], set[Circle], set[Line]]] = [(points.copy(), circles.copy(), lines.copy())]
 
    history_changed = False
    click_mode = 0 # 0 is new point, 1 is delete nearest point
     
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
 
                    state_history = [(points.copy(), circles.copy(), lines.copy())]
             
                elif event.key == pygame.K_l:
                    add_random_line(points, circles, lines)
                    state_history.append((points.copy(), circles.copy(), lines.copy()))
                 
                elif event.key == pygame.K_c:
                    add_random_circle(points, circles, lines)
                    state_history.append((points.copy(), circles.copy(), lines.copy()))
                 
                elif event.key == pygame.K_SPACE:
                    add_new_random_object(points, circles, lines)
                    state_history.append((points.copy(), circles.copy(), lines.copy()))
 
                 
                elif event.key == pygame.K_z:
                    if len(state_history) > 0:
                        history_changed = True
                        points, circles, lines = state_history.pop()
                 
                elif event.key == pygame.K_0:
                    click_mode = 0
                 
                elif event.key == pygame.K_1:
                    click_mode = 1
                 
                elif event.key == pygame.K_EQUALS:
                    screen_scale += 10
 
                elif event.key == pygame.K_MINUS:
                    if screen_scale > 10:
                        screen_scale -= 10
                # check control+z
                if history_changed:
                    history_changed = False
                else:
                    state_history.append((points.copy(), circles.copy(), lines.copy()))
 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if click_mode == 0:
                    click_pos = convert_screen_coords_to_geo_point(pygame.mouse.get_pos(), screen_scale)
                    if DebugMode:
                        print(f"click at {click_pos} and mode 0")
                    add_points(points, {click_pos})
                    state_history.append((points.copy(), circles.copy(), lines.copy()))
                 
                if click_mode == 1:
 
                    click_pos = convert_screen_coords_to_geo_point(pygame.mouse.get_pos(), screen_scale)
                    if DebugMode:
                        print(f"click at {click_pos} and mode 1")
                    nearest_point = nearest_point(points, click_pos)
                    if nearest_point != None:
                        points.remove(nearest_point)
                        state_history.append((points.copy(), circles.copy(), lines.copy()))
                 
                   
        render_everything(lines, points, circles, screen_scale, screen)
        print(tokenize_state(points, circles, lines))
 
main()
