from numpy import float32, vstack, ones, zeros
from cv2 import SURF, FlannBasedMatcher, cvtColor, COLOR_BGR2GRAY


def get_points(c_img1, c_img2):

    # convert to gray
    img1 = cvtColor(c_img1, COLOR_BGR2GRAY)
    img2 = cvtColor(c_img2, COLOR_BGR2GRAY)
    surf = SURF()                       # Initiate SURF detector
    # find the key points and descriptors with SURF
    kp1, des1 = surf.detectAndCompute(img1,  None)
    kp2, des2 = surf.detectAndCompute(img2,  None)

    my_flan_index_tree = 0
    index_params = dict(algorithm=my_flan_index_tree,   trees=6)
    search_params = dict(checks=50)

    my_flan = FlannBasedMatcher(index_params, search_params)
    matches = my_flan.knnMatch(des1,  des2,   k=2)

    # store all the good matches as per Lowe's ratio test.
    good = []
    pts2 = []
    pts1 = []

    for m, n in matches:
        if m.distance < 0.9*n.distance:
            good.append(m)
        pts1 = float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        pts2 = float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

    # get color of key points
    lengths = len(pts1) - 1
    color1 = zeros((len(pts1), 1, 3))
    color2 = zeros((len(pts1), 1, 3))
    color = zeros((len(pts1), 1, 3), dtype=int)

    for i in range(1, lengths):
        color1[i] = c_img1[int(pts1[i][0][1]), int(pts1[i][0][0])]
        color2[i] = c_img2[int(pts2[i][0][1]), int(pts2[i][0][0])]
        color[i] = (color1[i] + color2[i])/2                        # avg of colors

    # convert the 2D features into homogeneous coordinates into array of 3x51 dimension
    pt1 = pts1.reshape((pts1.shape[0], 2)).T
    pt1 = vstack((pt1, ones(pt1.shape[1])))

    pt2 = pts2.reshape((pts2.shape[0], 2)).T
    pt2 = vstack((pt2, ones(pt2.shape[1])))

    return pt1, pt2, color
