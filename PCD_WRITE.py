from numpy import transpose
from Read_files import read_vtk2arr


def pcd_write(data, length, filename):
    my_file = open(filename, 'w')
    ptx = data[0]
    pty = data[1]
    ptz = data[2]
    comment = '# .PCD v.5 - Point Cloud Data file format\n'
    header = 'VERSION .5\n' + 'FIELDS x y z\n' + 'SIZE 4 4 4\n' + 'TYPE F F F\n' + 'COUNT 1 1 1\n' + \
             'WIDTH ' + str(length) + '\nHEIGHT 1\n' + 'POINTS ' + str(length) + '\nDATA ascii\n'
    my_file.write(comment)
    my_file.write(header)
    for j in range(length):
        if j != length:
            my_file.write('' + str(ptx[j]) + ' ' + str(pty[j]) + ' ' + str(ptz[j]) + '\n')
        else:
            my_file.write('' + str(ptx[j]) + ' ' + str(pty[j]) + ' ' + str(ptz[j]))
    my_file.close()


def pcd_write_color(data, color, length, filename):
    my_file = open(filename, 'w')
    ptx = data[0]
    pty = data[1]
    ptz = data[2]
    blue = color[0]
    green = color[1]
    red = color[2]
    comment = '# .PCD v.7 - Point Cloud Data file format\n'
    header = 'VERSION .7\n' + 'FIELDS x y z rgb\n' + 'SIZE 4 4 4 4\n' + 'TYPE F F F F\n' + 'COUNT 1 1 1 1\n' + \
             'WIDTH ' + str(length) + '\nHEIGHT 1\n' 'VIEWPOINT 0 0 0 1 0 0 0\n' + 'POINTS ' + str(length) + \
             '\nDATA ascii\n'
    my_file.write(comment)
    my_file.write(header)
    for j in range(length):

        rgb = rgb2float(int(red[j]), int(green[j]), int(blue[j]))
        if j != length:
            my_file.write('' + str(ptx[j]) + ' ' + str(pty[j]) + ' ' + str(ptz[j]) + ' ' + str(rgb) + '\n')
        else:
            my_file.write('' + str(ptx[j]) + ' ' + str(pty[j]) + ' ' + str(ptz[j]) + ' ' + str(rgb))
    my_file.close()


def rgb2float(r, g, b, a=0):
    return float(a << 24 | r << 16 | g << 8 | b)


def make_ply_file(filename, vertex, color, poly):
    my_file = open(filename, 'w')

    ptx = vertex[0]
    pty = vertex[1]
    ptz = vertex[2]

    clr = color[2]
    clg = color[1]
    clb = color[0]

    pt_no = len(transpose(color))
    poly_no = len(poly)

    header = 'ply\n' + 'format ascii 1.0\n' + 'comment author: Sandy\n' + 'comment object: 3D surface\n' + \
             'element vertex ' + str(len(transpose(color))) + '\n' + 'property float x\nproperty float y\nproperty float z\n' + \
             'property uchar red\nproperty uchar green\nproperty uchar blue\n' + 'element face ' + str(len(poly)) + \
             '\nproperty list uchar int vertex_indices\n' + 'end_header\n'

    my_file.write(header)
    for j in range(pt_no):
        my_file.write(str(ptx[j]) + ' ' + str(pty[j]) + ' ' + str(ptz[j]) + ' ' + str(clr[j]) + ' ' +
                      str(clg[j]) + ' ' + str(clb[j]) + '\n')
    for j in range(poly_no):
        if j != poly_no:
            my_file.write(str(poly[j][0]) + ' ' + str(poly[j][1]) + ' ' + str(poly[j][2]) + ' ' + str(poly[j][3]) +
                          '\n')
    my_file.close()


def make_obj_file(filename, vertex, color, normal, poly):
    my_file = open(filename, 'w')

    clr = color[2]
    clg = color[1]
    clb = color[0]

    pt_no = len(transpose(vertex)) - 1
    poly_no = len(poly) - 1

    for j in range(pt_no):
        color_r = float(clr[j])
        color_g = float(clg[j])
        color_b = float(clb[j])
        color_r /= 255
        color_g /= 255
        color_b /= 255
        my_file.write('vn ' + "{0:.6f}".format(normal[0][j]) + ' ' + "{0:.6f}".format(normal[1][j]) + ' ' + "{0:.6f}".format(normal[2][j]) + '\nv ' +
                      "{0:.6f}".format(vertex[0][j]) + ' ' + "{0:.6f}".format(vertex[1][j]) + ' ' + "{0:.6f}".format(vertex[2][j]) + ' ' + "{0:.6f}".format(color_r) +
                      ' ' + "{0:.6f}".format(color_g) + ' ' + "{0:.6f}".format(color_b) + '\n')
    for j in range(poly_no):
        if j != poly_no:
            my_file.write('f ' + str(poly[j][1]) + '//' + str(poly[j][1]) + ' ' + str(poly[j][2]) + '//' +
                          str(poly[j][2]) + ' ' + str(poly[j][3]) + '//' + str(poly[j][3]) + '\n')
        else:
            my_file.write(str(poly[j][0]) + ' ' + str(poly[j][1]) + ' ' + str(poly[j][2]) + ' ' + str(poly[j][3]))
    my_file.close()


def make_obj_point(filename, vertex, color):
    my_file = open(filename, 'w')

    clr = color[2]
    clg = color[1]
    clb = color[0]

    pt_no = len(transpose(vertex)) - 1

    for j in range(pt_no):
        color_r = float(clr[j])
        color_g = float(clg[j])
        color_b = float(clb[j])
        color_r /= 255
        color_g /= 255
        color_b /= 255
        my_file.write('v ' + "{0:.6f}".format(vertex[0][j]) + ' ' + "{0:.6f}".format(vertex[1][j]) + ' ' +
                      "{0:.6f}".format(vertex[2][j]) + ' ' + "{0:.6f}".format(color_r) +
                      ' ' + "{0:.6f}".format(color_g) + ' ' + "{0:.6f}".format(color_b) + '\n')
    my_file.close()

poly = read_vtk2arr('color.vtk')

