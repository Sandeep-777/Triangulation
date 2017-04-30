import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from numpy import transpose, delete, size, zeros
from sklearn.cluster import DBSCAN
from Triangulate import triangulate
from PCD_WRITE import make_obj_file
from Points import get_points
from Read_files import read_file, mat_to_np_arr, read_vtk2arr, read_normals_from_pcd


image = read_file('images')             # load images
P = mat_to_np_arr('projective.mat')          # load projection matrices

pt1, pt2, color = get_points(image[0], image[1])       # get matched feature points and their color
X_est = triangulate(pt1, pt2, P[0], P[1])       # triangulate the points for 3D data

# CLUSTERING
Y = transpose(X_est)             # DBSCAN takes 3*n array
Y = delete(Y, [3], axis=1)       # deleting the w component from X
db_scan = DBSCAN(eps=0.015, min_samples=15)
db_scan.fit(Y)
labels = db_scan.labels_
PTS = Y[labels == 0]
vertices = PTS.tolist()
# get clustered colors
colors = color[labels == 0]
colors = transpose(colors)
colors = colors.reshape((3, -1))
my_color = zeros(colors.shape, dtype=float)
for i in range(1, size(my_color, 1)):
    my_color[0][i] = float(colors[0][i]) / 255
    my_color[1][i] = float(colors[1][i]) / 255
    my_color[2][i] = float(colors[2][i]) / 255
color = transpose(my_color).tolist()

poly = read_vtk2arr('color.vtk')
poly = poly.tolist()
normal = read_normals_from_pcd('m.pcd')
normal = normal.tolist()


def cube():
    glBegin(GL_TRIANGLE_STRIP)
    for surface in poly:
        x = 0
        for vertex in surface:
            x += 1
            glColor3fv(color[x])
            glVertex3fv(vertices[vertex])
    glEnd()
    # glBegin(GL_LINES)
    # for edge in edges:
    #     for vertex in edge:
    #         glVertex3fv(vertices[vertex])
    # glEnd()


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.01, 100.0)
    glTranslatef(0.0, 0.0, -5)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:
                    glTranslatef(-0.5, 0, 0)
                if event.key == pygame.K_l:
                    glTranslatef(0.5, 0, 0)
                if event.key == pygame.K_i:
                    glTranslatef(0, 1, 0)
                if event.key == pygame.K_k:
                    glTranslatef(0, -1, 0)
                if event.key == pygame.K_a:
                    glRotatef(-3, 1, 0, 0)
                if event.key == pygame.K_d:
                    glRotatef(3, 1, 0, 0)
                if event.key == pygame.K_w:
                    glRotatef(-3, 0, 0, 1)
                if event.key == pygame.K_s:
                    glRotatef(3, 0, 0, 1)
                if event.key == pygame.K_q:
                    glRotatef(-3, 0, 1, 0)
                if event.key == pygame.K_e:
                    glRotatef(3, 0, 1, 0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    glTranslatef(0, 0, 1.0)

                if event.button == 5:
                    glTranslatef(0, 0, -1.0)
        # glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        cube()
        pygame.display.flip()
        pygame.time.wait(10)


main()
