from numpy import transpose, delete, size
from sklearn.cluster import DBSCAN
from Triangulate import triangulate
from PCD_WRITE import make_ply_file
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
PTS = transpose(PTS)
# get clustered colors
colors = color[labels == 0]
colors = transpose(colors)
colors = colors.reshape((3, -1))

poly = read_vtk2arr('color.vtk')
normal = read_normals_from_pcd('m.pcd')
normal = transpose(normal)

# making ply file

make_ply_file('surface.ply', PTS, colors, poly)

print 'PTS'
print PTS.shape
print '\ncolors'
print colors.shape
print '\nnormal'
print normal.shape
print '\npoly'
print poly.shape