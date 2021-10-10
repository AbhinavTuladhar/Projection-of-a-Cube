import pygame
import numpy as np
from math import sin, cos, pi

# Screen size and Colours
WIDTH, HEIGHT = 1280, 680
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Setting up pygame
pygame.init()
pygame.display.set_caption("3D Projection")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# All the constants used in the program.
clock = pygame.time.Clock()
FPS = 60
distance = 5                                    # Change this to change initial position
z_change = 0.015                                # Used while zooming in and out
z_offset = 0
scale = 600                                     # Change the size of the cube
angle = 0
index = 0
speed = 0.02                                    # Change the rotation speed
cube_position = [WIDTH // 2, HEIGHT // 2]
font = pygame.font.SysFont("helvetica", 20, bold = True)

flags = [0 for _ in range(3)]                   # Check whether the cube is rotating around an axis

rotation_dict = {
    0 : 'x-axis',
    1 : 'y-axis',
    2 : 'z-axis'
}

# Points of the cube
points = []
points.append(np.array([-1, -1, 1]))
points.append(np.array([1, -1, 1]))
points.append(np.array([1,  1, 1]))
points.append(np.array([-1, 1, 1]))
points.append(np.array([-1, -1, -1]))
points.append(np.array([1, -1, -1]))
points.append(np.array([1, 1, -1]))
points.append(np.array([-1, 1, -1]))

# Used to store the projection points
projected_points = [x for x in range(len(points))]

# Function to connect the projected points
def connect_points(i, j, k):
    a = k[i]
    b = k[j]
    pygame.draw.line(screen, WHITE, (a[0], a[1]), (b[0], b[1]), 2)

running = True
while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            # For rotation purposes
            if event.key == pygame.K_x:
                flags[0] = (flags[0] + 1) % 2
            if event.key == pygame.K_y:
                flags[1] = (flags[1] + 1) % 2
            if event.key == pygame.K_z:
                flags[2] = (flags[2] + 1) % 2
            # For zooming purposes
            if event.key == pygame.K_UP:
                z_offset += z_change
            if event.key == pygame.K_DOWN:
                z_offset -= z_change

    # Apply update to angle only if at least one rotation
    # matrix is active
    if all(flag == 0 for flag in flags):
        angle = 0
    else:
        angle += speed

    # Create a list to store the rotation matrices
    rotation_matrices = []

    rotation_x = np.array([
        [1, 0, 0],
        [0, cos(angle), -sin(angle)],
        [0, sin(angle), cos(angle)]
    ])

    rotation_y = np.array([
        [cos(angle), 0, -sin(angle)],
        [0, 1, 0],
        [sin(angle), 0, cos(angle)]
    ])

    rotation_z = np.array([
        [cos(angle), -sin(angle), 0],
        [sin(angle), cos(angle), 0],
        [0, 0, 1]
    ])

    rotation_matrices.extend([rotation_x, rotation_y, rotation_z])

    index = 0
    for point in points:
        rotated_2d = np.dot(np.identity(3), point.reshape((3, 1)))

        # Multiply with rotation matrix if corresponding flag is set
        for flag, matrix in zip(flags, rotation_matrices):
            if flag:
                rotated_2d = np.dot(matrix, rotated_2d)

        # For perspective projection
        z = 1 / (distance - rotated_2d[2][0]) + z_offset
        projection_matrix = np.array([
            [z, 0, 0],
            [0, z, 0],
        ])

        # Project the 3D object to the 2D screen
        projected = np.dot(projection_matrix, rotated_2d)
        # For scaling and proper positioning
        x = int(projected[0][0] * scale) + cube_position[0]
        y = int(projected[1][0] * scale) + cube_position[1]

        projected_points[index] = [x, y]
        index += 1

        # Draw a circle at the projected point
        pygame.draw.circle(screen, WHITE, (x, y), 5)

    # Connecting the points
    for p in range(4):
        connect_points(p, (p + 1) % 4, projected_points)
        connect_points(p + 4, ((p + 1) % 4) + 4, projected_points)
        connect_points(p, (p + 4), projected_points)

    # For text purposes
    expression = "Active rotation matrices: "
    for count, flag in enumerate(flags):
        if flag:
            expression += rotation_dict[count] + " "
    label = font.render(expression, 2, WHITE)
    screen.blit(label, (0, 0))

    pygame.display.update()
    clock.tick(FPS)

print(projected.shape)
pygame.quit()