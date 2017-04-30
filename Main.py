from numpy import size
from matplotlib import pyplot as plt
from PCD_WRITE import pcd_write, pcd_write_color, make_ply_file, make_obj_point
from Read_files import read_file, mat_to_np_arr, read_vtk2arr
from mpl_toolkits.mplot3d import axes3d
from Total import gen_3d_pts


image = read_file('images')             # load images
P = mat_to_np_arr('projective.mat')          # load projection matrices

PTS, colors = gen_3d_pts(image, P)             # generate 3D vertices with colors

# exporting file
length = size(PTS[0])

pcd_write_color(PTS, colors, length, 'points_3D_color.pcd')
make_obj_point('point_cloud.obj', PTS, colors)


# plotting figure
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot(PTS[0], PTS[1], PTS[2], 'ko')
plt.axis('equal')
plt.show()
