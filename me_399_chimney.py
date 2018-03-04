import numpy as np
import pprint
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from scipy.interpolate import interp2d
# from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm


def chimney_problem():
    '''
    The chimney cross section is given. The outside material is composed of a
    fire brick with a thermal conductivity of 4.1 W/m-C. Determine the
    temperature profile of the stack using the following inside and outside
    convective conditions.

            |--------- x_outside --------|
            ______________________________ ________
            |                            |       |
     ______ |      ________________      |       |
      |     |      |              |      |       |
y_inside    |      |              |      |     y_outside
     _|____ |      |______________|      |       |
            |                            |       |
            |____________________________|_______|_
                   |-- x_inside --|

    Inside temp. T_i = 380 C
    Inside conv. coeff. h_i = 85 W/m^2-C
    Outside temp. T_o = 35 C
    Outside conv. coeff. h_o = 22.0 W/m^2-C
    '''
    node_size = 4 # Square node side length (mm)

    # Geometry
    x_outside = 180 # mm
    x_inside = 100 # mm
    y_outside = 120 # mm
    y_inside = 40 # mm

    # Error estimation and iteration limits
    c_error = 100 # Current error percentage
    er_max = 1 # Maximum error tolerance
    c_iter = 0 # Instantiate iterations
    iter_max = 1000 # Maximum iterations

    # Heat Transfer
    i_temp = 380 # Inside temp (C)
    h_in = 85 # Inside convection coefficient
    o_temp = 35 # Outside temp
    h_out = 22 # Outside convection coefficient
    k_brick = 4.1 # conduction coefficient for fire bricks

    # Using symmetry, we don't need the top half or the right half of the diagram
    # Due to python zero indexing, we need to add one 'node size' unit to
    # get the edge values to calculate
    x_max = int((x_outside/(2)) + node_size)
    y_max = int((y_outside/(2)) + node_size)
    # The inside corner point prevents the generation of points that are outside
    # the geometry and gives a reference to the location of the inside edges
    inside_corner = (x_max-(x_inside/2), y_max-(y_inside/2))
    # Create an array of possible coordinate values
    x_points = np.arange(0, x_max, node_size)
    y_points = np.arange(0, y_max, node_size)
    # generate a list of tuples based on the geometry information
    data_points = {}
    for i in x_points:
        for j in y_points:
            if i < inside_corner[0] or j < inside_corner[1]:
                data_points['({},{})'.format(i,j)] = {'x_coord' : i , 'y_coord' : j, 'temp': 0}
    print('{} points generated for calculation...\n'.format(len(data_points)))
    # pprint.pprint(data_points)
    # above = lambda in_key :
    while c_error > er_max and c_iter < iter_max:
        c_iter += 1
        point_error = 0

        for point in data_points:
            data_points[point]['old_temp'] = data_points[point]['temp']
            if point == '(0,0)':
                # Bottom Corner
                # CASE 4
                # print('Outside Corner : {} = {}'.format(point, data_points[point]['temp']))
                t_above = data_points['({},{})'.format(data_points[point]['y_coord'] + node_size ,data_points[point]['x_coord'])]['temp']
                t_right = data_points['({},{})'.format(data_points[point]['y_coord'] ,data_points[point]['x_coord'] + node_size)]['temp']

                data_points[point]['temp'] = (t_above + t_right + (2 * h_out * o_temp) / k_brick) / (2 * ((h_out * node_size/k_brick) + 1))

            elif (data_points[point]['x_coord'] == 0) ^ (data_points[point]['y_coord'] == 0):
                # Outside Edge
                # CASE 3
                # print('Outside Edge : {} = {}'.format(point, data_points[point]['temp']))
                above_ref = '({},{})'.format(data_points[point]['x_coord'], data_points[point]['y_coord'] + node_size)
                below_ref = '({},{})'.format(data_points[point]['x_coord'], data_points[point]['y_coord'] - node_size)
                left_ref = '({},{})'.format(data_points[point]['x_coord'] - node_size, data_points[point]['y_coord'])
                right_ref = '({},{})'.format(data_points[point]['x_coord'] + node_size, data_points[point]['y_coord'])

                try:
                    vertical = data_points[above_ref]['temp']
                except:
                    vertical = data_points[below_ref]['temp']
                try:
                    horiz = data_points[right_ref]['temp']
                except:
                    horiz = data_points[left_ref]['temp']

                data_points[point]['temp'] = ((2 * vertical + 2 * horiz) + (2 * node_size * h_out * o_temp / k_brick)) / (2 * ((h_out * node_size / k_brick) + 2))

            elif (data_points[point]['x_coord'] == inside_corner[0] - node_size and data_points[point]['y_coord'] > inside_corner[1] - node_size) ^ (data_points[point]['y_coord'] == inside_corner[1] - node_size and data_points[point]['x_coord'] > inside_corner[0] - node_size):
                # Inside Edge
                # print('Inside Edge : {} = {}'.format(point, data_points[point]['temp']))
                above_ref = '({},{})'.format(data_points[point]['x_coord'], data_points[point]['y_coord'] + node_size)
                below_ref = '({},{})'.format(data_points[point]['x_coord'], data_points[point]['y_coord'] - node_size)
                left_ref = '({},{})'.format(data_points[point]['x_coord'] - node_size, data_points[point]['y_coord'])
                right_ref = '({},{})'.format(data_points[point]['x_coord'] + node_size, data_points[point]['y_coord'])

                try:
                    vertical = data_points[above_ref]['temp']
                except:
                    vertical = data_points[below_ref]['temp']
                try:
                    horiz = data_points[right_ref]['temp']
                except:
                    horiz = data_points[left_ref]['temp']

                data_points[point]['temp'] = ((2 * vertical + 2 * horiz) + (2 * node_size * h_in * i_temp / k_brick)) / (2 * ((h_in * node_size / k_brick) + 2))

            elif (data_points[point]['x_coord'] == inside_corner[0] - node_size) and (data_points[point]['y_coord'] == inside_corner[1] - node_size):
                # Inside Corner
                # print('Inside Corner : {} = {}'.format(point, data_points[point]['temp']))
                above_ref = '({},{})'.format(data_points[point]['x_coord'], data_points[point]['y_coord'] + node_size)
                below_ref = '({},{})'.format(data_points[point]['x_coord'], data_points[point]['y_coord'] - node_size)
                left_ref = '({},{})'.format(data_points[point]['x_coord'] - node_size, data_points[point]['y_coord'])
                right_ref = '({},{})'.format(data_points[point]['x_coord'] + node_size, data_points[point]['y_coord'])

                above = data_points[above_ref]['temp']
                below = data_points[below_ref]['temp']
                right = data_points[right_ref]['temp']
                left = data_points[left_ref]['temp']

                data_points[point]['temp'] = (2 * (left + below) + (right + above) + (2 * h_in * node_size * i_temp / k_brick))/ (2 * (3 + h_in * node_size / k_brick))


            else:
                # Interior piece
                above_ref = '({},{})'.format(data_points[point]['x_coord'], data_points[point]['y_coord'] + node_size)
                below_ref = '({},{})'.format(data_points[point]['x_coord'], data_points[point]['y_coord'] - node_size)
                left_ref = '({},{})'.format(data_points[point]['x_coord'] - node_size, data_points[point]['y_coord'])
                right_ref = '({},{})'.format(data_points[point]['x_coord'] + node_size, data_points[point]['y_coord'])

                try:
                    above = data_points[above_ref]['temp']
                except:
                    above = data_points[below_ref]['temp']
                below = data_points[below_ref]['temp']
                try:
                    right = data_points[right_ref]['temp']
                except:
                    right = data_points[left_ref]['temp']
                left = data_points[left_ref]['temp']

                data_points[point]['temp'] = (above + below + left + right)/4
            point_error += abs((data_points[point]['temp'] - data_points[point]['old_temp']) / data_points[point]['temp']) * 100
        c_error = point_error/len(data_points)
        print(c_error)

    # pprint.pprint(data_points)
    plot_data = []
    for i in x_points:
        for j in y_points:
            ref = '({},{})'.format(i,j)
            try:
                plot_data.append((i,j,data_points[ref]['temp']))
            except:
                plot_data.append((i,j,380))
    x_list = np.array([item[0] for item in plot_data])
    y_list = np.array([item[1] for item in plot_data])
    z_list = np.array([item[2] for item in plot_data])
    plt.scatter(x_list, y_list, c=z_list, cmap=cm.inferno, marker='s', s=node_size*30)
    plt.title('Chimney Heat Distribution Map')
    plt.xlabel('X - Axis Location (mm)')
    plt.ylabel('Y - Axis Location (mm)')
    plt.xticks(np.arange(0, x_max, 10))
    plt.colorbar()
    plt.show()







chimney_problem()