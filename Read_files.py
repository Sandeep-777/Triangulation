from os import listdir
from os.path import isfile, join, dirname
from numpy import empty, transpose, size, loadtxt, s_, delete
from cv2 import imread, cvtColor, COLOR_BGR2GRAY
from scipy.io import loadmat
import vtk
from numpy import zeros


def read_file(folder_name):
    my_path = join(dirname(__file__), folder_name)
    only_files = [f for f in listdir(my_path) if isfile(join(my_path, f))]
    only_files = sorted(only_files)
    images = empty(len(only_files), dtype=object)
    for n in range(0, len(only_files)):
        images[n] = imread(join(my_path, only_files[n]))
    return images


def convert_to_gray(images):
    length = size(images)
    img = empty(length, dtype=object)
    for i in range(0, length):
        img[i] = cvtColor(images[i], COLOR_BGR2GRAY)
    return img


def mat_to_np_arr(filename):
    data = list()
    mat = loadmat(filename)
    m = mat["P"]
    m = transpose(m)
    for i in range(0, 36):
        data.append(m[i][0])
    return data


def read_vtk2arr(filename):
    reader = vtk.vtkDataSetReader()
    reader.SetFileName(filename)
    reader.ReadAllScalarsOn()         # Activate the reading of all scalars
    reader.Update()

    data = reader.GetOutput()
    vt = data.GetPolys()
    no_of_poly = data.GetNumberOfPolys()
    poly = zeros((no_of_poly, 4), dtype=int)
    count = int(0)

    for i in range(0, vt.GetSize(), 4):
        poly[count][0] = vt.GetData().GetValue(i)
        poly[count][1] = vt.GetData().GetValue(i+1)
        poly[count][2] = vt.GetData().GetValue(i+2)
        poly[count][3] = vt.GetData().GetValue(i+3)
        count += 1

    return poly


def read_normals_from_pcd(filename):
    data = loadtxt(filename, skiprows=11)
    data = delete(data, s_[0:3], 1)
    data = delete(data, 3, 1)
    return data
