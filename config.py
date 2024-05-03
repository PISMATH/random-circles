screen_width = 2400
screen_height = 1200
fps = 15
scale = 100

background_color = (255, 255, 255)

points_size = 4
point_color = (0, 0, 0)
point_rounding = 1e-10 # How close points are before they are the same

circle_color = (255, 0, 0)
circle_width = 2
circle_odds = 0.5
circle_rounding = 1e-10 # How close circles are before they are the same

line_color = (0, 0, 255)
line_width = 1

Point = tuple[float, float]
Circle = tuple[Point, Point, float]
Line = tuple[Point, Point]

DebugMode = False

inital_points = {(-1, 0), (1, 0)}
