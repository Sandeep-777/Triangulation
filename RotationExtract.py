import numpy as np
from math import atan2
from math import degrees
from math import sqrt
from math import sin
from math import cos
import os


def builder(angles):
    # Reverse
    alpha = angles[1]
    beta = angles[2]
    gama = angles[3]
    r_x = [1, 0, 0, 0, cos(gama), -sin(gama), 0, sin(gama), cos(gama)]
    r_xmat = np.array(r_x).reshape(3, 3)
    r_y = [cos(beta), 0, sin(beta), 0, 1, 0, -sin(beta), 0, cos(beta)]
    r_ymat = np.array(r_y).reshape(3, 3)
    r_z = [cos(alpha), -sin(alpha), 0, sin(alpha), cos(alpha), 0, 0, 0, 1]
    r_zmat = np.array(r_z).reshape(3, 3)
    r_mat_1 = np.dot(r_zmat, r_ymat)
    r_mat = np.dot(r_mat_1, r_xmat)
    return r_mat


def worker():
    my_paths = os.listdir('/home/sandeep/Desktop/MajorProject/Images')
    main_list = []
    rot_max = []
    for item in my_paths:
        name = item[:-4]
        first_list = name.split(';')
        first_np_list = np.array(first_list, dtype=float)
        main_list.append(first_np_list)
    main_array = np.array(main_list)
    for array in main_array:
        retval = builder(array)
        extra = np.zeros((3, 1))
        retval1 = np.hstack((retval, extra))
        rot_max.append(retval1)
    rot_final = np.array(rot_max)
    return rot_final


def mapper(ds1, ds2):
    alpha_1 = atan2(ds1[1][0], ds1[0][0])
    beta_1 = atan2(-(ds1[2][0]), sqrt((ds1[2][1] ** 2) + (ds1[2][2] ** 2)))
    gama_1 = atan2(ds1[2][1], ds1[2][2])
    alpha_2 = atan2(ds2[1][0], ds2[0][0])
    beta_2 = atan2(-(ds2[2][0]), sqrt((ds2[2][1] ** 2) + (ds2[2][2] ** 2)))
    gama_2 = atan2(ds2[2][1], ds2[2][2])
    del_alpha = alpha_1 - alpha_2
    del_beta = beta_1 - beta_2
    del_gama = gama_1 - gama_2
    print del_alpha, del_beta, del_gama
    r_x1 = [1, 0, 0, 0, cos(del_gama), -sin(del_gama), 0, sin(del_gama), cos(del_gama)]
    r_xmat1 = np.array(r_x1).reshape(3, 3)
    r_y1 = [cos(del_beta), 0, sin(del_beta), 0, 1, 0, -sin(del_beta), 0, cos(del_beta)]
    r_ymat1 = np.array(r_y1).reshape(3, 3)
    r_z1 = [cos(del_alpha), -sin(del_alpha), 0, sin(del_alpha), cos(del_alpha), 0, 0, 0, 1]
    r_zmat1 = np.array(r_z1).reshape(3, 3)
    r_mat_1_1 = np.dot(r_zmat1, r_ymat1)
    r_mat_send = np.dot(r_mat_1_1, r_xmat1)
    return r_mat_send


def changeRelation(ds0, ds1, ds2):
    alpha_0 = atan2(ds0[1][0], ds0[0][0])
    beta_0 = atan2(-(ds0[2][0]), sqrt((ds0[2][1] ** 2) + (ds0[2][2] ** 2)))
    gama_0 = atan2(ds0[2][1], ds0[2][2])

    alpha_1 = atan2(ds1[1][0], ds1[0][0])
    beta_1 = atan2(-(ds1[2][0]), sqrt((ds1[2][1] ** 2) + (ds1[2][2] ** 2)))
    gama_1 = atan2(ds1[2][1], ds1[2][2])

    alpha_2 = atan2(ds2[1][0], ds2[0][0])
    beta_2 = atan2(-(ds2[2][0]), sqrt((ds2[2][1] ** 2) + (ds2[2][2] ** 2)))
    gama_2 = atan2(ds2[2][1], ds2[2][2])

    del_alpha1 = alpha_1 - alpha_0
    del_beta1 = beta_1 - beta_0
    del_gama1 = gama_1 - gama_0
    dx1 = ds1[0][3]
    dy1 = ds1[1][3]
    dz1 = ds1[1][3]

    del_alpha2 = alpha_2 - alpha_0
    del_beta2 = beta_2 - beta_0
    del_gama2 = gama_2 - gama_0
    dx2 = ds2[0][3] - ds0[0][3]
    dy2 = ds2[1][3] - ds0[1][3]
    dz2 = ds2[1][3] - ds0[2][3]

    del_alpha = del_alpha2 - del_alpha1
    del_beta = del_beta2 - del_beta1
    del_gama = del_gama2 - del_gama1
    dx = dx2 - dx1
    dy = dy2 - dy1
    dz = dz2 - dz1

    T = np.array([[dx1], [dy1], [dz1]])

    r_x1 = [1, 0, 0, 0, cos(del_gama), -sin(del_gama), 0, sin(del_gama), cos(del_gama)]
    r_xmat1 = np.array(r_x1).reshape(3, 3)
    r_y1 = [cos(del_beta), 0, sin(del_beta), 0, 1, 0, -sin(del_beta), 0, cos(del_beta)]
    r_ymat1 = np.array(r_y1).reshape(3, 3)
    r_z1 = [cos(del_alpha), -sin(del_alpha), 0, sin(del_alpha), cos(del_alpha), 0, 0, 0, 1]
    r_zmat1 = np.array(r_z1).reshape(3, 3)
    r_mat_1_1 = np.dot(r_zmat1, r_ymat1)
    r_mat_send = np.dot(r_mat_1_1, r_xmat1)
    retval1 = np.hstack((r_mat_send, T))

    return retval1
