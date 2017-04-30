from numpy import transpose, delete, zeros, hstack
from sklearn.cluster import DBSCAN
from Triangulate import triangulate
from Points import get_points


def gen_3d_pts(images, P):
    image_no = len(P)
    final_colors = zeros((3, 1))
    final_pts = zeros((3, 1))
    for i in range(0, image_no-1):

        j = i + 1
        if j > image_no:
            j = 0

        pt1, pt2, color = get_points(images[i], images[j])  # get matched feature points and their color
        X_est = triangulate(pt1, pt2, P[i], P[j])  # triangulate the points for 3D data

        # CLUSTERING
        Y = transpose(X_est)  # DBSCAN takes 3*n array
        Y = delete(Y, [3], axis=1)  # deleting the w component from X
        db_scan = DBSCAN(eps=0.015, min_samples=5)
        db_scan.fit(Y)
        labels = db_scan.labels_
        pt = Y[labels == 0]
        pt = transpose(pt)
        # get clustered colors
        my_colors = color[labels == 0]
        my_colors = transpose(my_colors)
        my_colors = my_colors.reshape((3, -1))

        final_pts = hstack((final_pts, pt))
        final_colors = hstack((final_colors, my_colors))

    final_pts[0][0] = final_pts[0][1]
    final_pts[1][0] = final_pts[1][1]
    final_pts[2][0] = final_pts[2][1]

    final_colors[0][0] = final_colors[0][1]
    final_colors[1][0] = final_colors[1][1]
    final_colors[2][0] = final_colors[2][1]

    return final_pts, final_colors
