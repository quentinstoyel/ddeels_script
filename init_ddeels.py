import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


import sys
import getopt


def main(argv):
    # defaults
    dimension = 100
    dipoles = 6000
    roundedness = 0.4
    angle = 0
    ratio = 1
    graph = False
    filename = "ag_cube"
    try:
        opts, args = getopt.getopt(argv, "hs:d:r:a:R:n:g:", [
                                   "size=", "dipole=", "roundedness=", 'angle=', "Ratio=", "filename=","graph="])
    except getopt.GetoptError:
        print 'init_ddeels.py -s <size> -d <dipole> -r <roundedness> -a <angle> -R <Ratio> -g <graph> \n \n'
        print 'This script generates the .pos, impar.dat and dx files for DDEELS and prints the actual number of dipoles in the final structure'
        print 'Make sure to input the filenames from these  into your ddeels.in file. '
        print 'Some parameters can be specified on the commmand line, to run execute: \n'
        print 'python init_ddeels.py <arguments> \n '
        print 'Defaults are:\n            dimension = 100 \n            dipoles = 6000 \n            roundedness = 0.4\n            angle = 0\n            ratio = 1\n            filename = "ag_cube"\n            graph = False'
        print
        print 'User specified options: \n-----------------------'
        print '<-s>   <--size> Length of side of cube in nm \n<-d>   <--dipole> Max number of dipoles in cube \n<-r>   <--roundedness> Defines how round the corners of the cube are, range (0,1]. 0= cube, 1 =sphere'
        print '<-a>   <--angle> Defines angle of rotation around x, relative to electron beam.  \n<-R>   <--Ratio> Defines ratio of x side to y side, to make rectangles, range [1,inf]. \n<-f>   <--filename> Defines filename of .pos file.  '
        print '<-g>   <--graph> Indicates whether or not to plot graph of dipole locations \n<-h> prints this message'
        print
        print 'END HELP'

        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'init_ddeels.py -s <size> -d <dipole> -r <roundedness> -a <angle> -R <Ratio> -g <graph> \n \n'
            print 'This script generates the .pos, impar.dat and dx files for DDEELS and prints the actual number of dipoles in the final structure'
            print 'Make sure to input the filenames from these  into your ddeels.in file. '
            print 'Some parameters can be specified on the commmand line, to run execute: \n'
            print 'python init_ddeels.py <arguments> \n '
            print 'Defaults are:\n            dimension = 100 \n            dipoles = 6000 \n            roundedness = 0.4\n            angle = 0\n            ratio = 1\n            filename = "ag_cube"\n            graph = False'
            print
            print 'User specified options: \n-----------------------'
            print '<-s>   <--size> Length of side of cube in nm \n<-d>   <--dipole> Max number of dipoles in cube \n<-r>   <--roundedness> Defines how round the corners of the cube are, range (0,1]. 0= cube, 1 =sphere'
            print '<-a>   <--angle> Defines angle of rotation around x, relative to electron beam.  \n<-R>   <--Ratio> Defines ratio of x side to y side, to make rectangles, range [1,inf]. \n<-f>   <--filename> Defines filename of .pos file.  '
            print '<-g>   <--graph> Indicates whether or not to plot graph of dipole locations \n<-h> prints this message'
            print
            print 'END HELP'


            sys.exit()
        elif opt in ("-s", "--size"):
            dimension = float(arg)
        elif opt in ("-R", "--Ratio"):
            ratio = float(arg)
            if ratio < 1:
                sys.exit("Ratio must be greater or equal to 1")
        elif opt in ("-d", "--dipole"):
            dipoles = int(arg) * ratio
        elif opt in ("-r", "--roundedness"):
            roundedness = float(arg)
        elif opt in ("-a", "--angle"):
            angle = float(arg)
        elif opt in ("-R", "--Ratio"):
            ratio = float(arg)
        elif opt in ("-n", "--filename"):
            filename = str(arg)
        elif opt in ("-g", "--graph"):
            graph = arg == 'True'
    x = Ddeels_rounded_cube(dimension, roundedness,
                            dipoles, angle, ratio, filename,graph)
    x.initialize_files_for_ddeels()



def to_precision(x,p):
    """
    returns a string representation of x formatted with a precision of p

    Based on the webkit javascript implementation taken from here:
    https://code.google.com/p/webkit-mirror/source/browse/JavaScriptCore/kjs/number_object.cpp
    """

    x = float(x)

    if x == 0.:
        return "0." + "0"*(p-1)

    out = []

    if x < 0:
        out.append("-")
        x = -x

    e = int(math.log10(x))
    tens = math.pow(10, e - p + 1)
    n = math.floor(x/tens)

    if n < math.pow(10, p - 1):
        e = e -1
        tens = math.pow(10, e - p+1)
        n = math.floor(x / tens)

    if abs((n + 1.) * tens - x) <= abs(n * tens -x):
        n = n + 1

    if n >= math.pow(10,p):
        n = n / 10.
        e = e + 1

    m = "%.*g" % (p, n)

    if e < -2 or e >= p:
        out.append(m[0])
        if p > 1:
            out.append(".")
            out.extend(m[1:p])
        out.append('e')
        if e > 0:
            out.append("+")
        out.append(str(e))
    elif e == (p -1):
        out.append(m)
    elif e >= 0:
        out.append(m[:e+1])
        if e+1 < len(m):
            out.append(".")
            out.extend(m[e+1:])
    else:
        out.append("0.")
        out.extend(["0"]*-(e+1))
        out.append(m)

    return "".join(out)




class Ddeels_rounded_cube:

    def __init__(self, dimension, roundedness, max_number_of_dipoles, angle, ratio, filename, graph):
        self.rotation_angle = angle #initializing everything to the class
        self.exp_factor = 2.0 / roundedness #centers the cube at origin
        self.max_value = dimension / 2.0
        self.ratio = ratio
        self.step_size = dimension / (float(max_number_of_dipoles)**(1.0 / 3))
        self.filename = filename
        self.graph = graph
        self.x_values = np.arange(-self.max_value,
                                  self.max_value, self.step_size / self.ratio)
        self.y_values = np.arange(-self.max_value,
                                  self.max_value, self.step_size)
        self.z_values = np.arange(-self.max_value,
                                  self.max_value, self.step_size)

    def function_3d_shape(self, x, y, z):
        # given coordinates of dipole, returns True/False if dipole is inside/outside thing
        coordinate_value = np.abs((x * self.ratio))**self.exp_factor + np.abs(y)**self.exp_factor + \
            np.abs(z)**self.exp_factor - \
            np.abs((self.max_value))**self.exp_factor
        if coordinate_value > 0:
            return False
        elif coordinate_value <= 0:
            return True

    def make_rotation_matrix(self, angle):
        angle = angle
        # define rotation matrix around x axis, in degrees:
        theta = (angle / 180.) * np.pi
        self.rotation_matrix = np.matrix([[np.cos(theta), np.sin(theta)],
                                          [-np.sin(theta),  np.cos(theta)]])
        return

    def write_cube(self):
        # file to write the positions to, whilst waiting to figure out header
        storage_file = open('cube_storage.pos', 'w')
        dipole_count = 0  # counter to make sure we know how many dipoles we have
        self.make_rotation_matrix(self.rotation_angle)  # if tilting
        if self.graph is True: #does this output a graph?
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
        for x in self.x_values:
            for y in self.y_values:
                for z in self.z_values:
                    # if the point x,y,z is in the shape
                    if self.function_3d_shape(x, y, z) == True:
                        final_y, final_z = np.array(
                            np.matmul(self.rotation_matrix, [y, z]))[0]  # rotate around x
                        data_row = "   " + str(to_precision(x, 8)) + "        " + str(to_precision(
                            final_y, 8)) + "         " + str(to_precision(final_z, 8)) + "       1           1 \n" #what to write to file
                        storage_file.write(data_row)
                        dipole_count += 1
                        if self.graph is True:
                            ax.scatter(x, final_y, final_z, c='b')
        if self.graph is True:
            plt.show()
        storage_file.close()
        storage_file = open('cube_storage.pos', 'r')
        print dipole_count
        cube_file = open(self.filename + "_" +
                         str(self.rotation_angle) + '.pos', 'w') #writes the header with the right number of dipoles
        cube_file.write('#' + str(dipole_count) + '\n')
        cube_file.write("#" + str(dipole_count) +
                        " dipole ag rounded cube from nicoletti paper \n")
        cube_file.write(
            "#     x(i)           y(i)                     z(i)     DxType(i)   DFType(i) \n")
        cube_file.write(storage_file.read())
        storage_file.close()
        cube_file.close()
        return

    def write_impar_file(self):
        #sticks impar on midpoint of side and on corner of shape, based of max values
        impar_file = open("impar.dat", 'w')
        impar_file.write(
            '# 2 \n # comment: in [Ang]\n#       x(i)        y(i)\n')
        impar_file.write('        ' + str(self.max_value + 2) +
                         '        ' + str(self.max_value + 2) + '\n')
        impar_file.write('        0.0        ' +
                         str(self.max_value + 2) + '\n')
        impar_file.close()

    def write_dx_file(self):
        dx_file = open("dxtype.dat", 'w')
        dx_file.write(
            "# 1 \n #comment: in [Ang] \n #      dx(i)         dy(i)        dz(i) \n")
        dx_file.write("      " + str(to_precision(self.step_size, 6)) + "       " + str(
            to_precision(self.step_size, 6)) + "      " + str(to_precision(self.step_size, 6) + "\n"))
        dx_file.close()

    def initialize_files_for_ddeels(self):
        #runs everything in the right order
        self.write_impar_file()
        self.write_cube()
        self.write_dx_file()


if __name__ == "__main__":
    main(sys.argv[1:])
