import numpy as np
import pprint
import matplotlib.pyplot as plt
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

    This program can take a variable node size, geometry, temperatures and material constants to
    generate a heat plot of cross section for the chimney. To reduce computation time, the program
    uses symmetry to break the plot into quarters and then rebuilds the full chimney size once the
    mean error threshold has been met.
    '''
    node_size = 10 # Square node side length (mm)

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

    # POINT MATRIX GENERATION
    # Using symmetry, we don't need the top half or the right half of the diagram
    # Due to python zero indexing, we need to add one 'node size' unit to
    # get the edge values to calculate
    x_max = int((x_outside/(2)) + node_size)
    y_max = int((y_outside/(2)) + node_size)
    # Convert the node length to meters
    delta_x = node_size/1000
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
                # Each entry in the data points dictionary contains a nested dictionary with keys referencing
                # position and temperature information. This dictionary will also hold old temp data for calculating
                # error across iterations
                data_points['({},{})'.format(i,j)] = {'x_coord' : i , 'y_coord' : j, 'temp': o_temp}
    print('{} points generated for calculation...\n'.format(len(data_points)))

    # CALCULATIONS
    # Generate temperature data and iterate through the points while the current estimated error is outside the
    # set limit
    while c_error > er_max and c_iter < iter_max:
        # Cycle the iterator
        c_iter += 1
        # Instantiate a variable to hold the error
        point_error = 0
        # Run through each point in the generated array
        for point in data_points:
            # Store the previous value for error estimation
            data_points[point]['old_temp'] = data_points[point]['temp']
            if point == '(0,0)':
                # Bottom Corner
                # CASE 4
                # print('Outside Corner : {} = {}'.format(point, data_points[point]['temp']))
                t_above = data_points['({},{})'.format(data_points[point]['y_coord'] + node_size ,data_points[point]['x_coord'])]['temp']
                t_right = data_points['({},{})'.format(data_points[point]['y_coord'] ,data_points[point]['x_coord'] + node_size)]['temp']
                # This calculation is straighforwward and only relies on the nodes above or below. The rest of the examples need more geometry
                data_points[point]['temp'] = (t_above + t_right + ((2 * h_out * o_temp * delta_x) / k_brick)) / (2 * ((h_out * delta_x/k_brick) + 1))

            elif (data_points[point]['x_coord'] == 0) ^ (data_points[point]['y_coord'] == 0) and (data_points[point]['y_coord'] != data_points[point]['x_coord']):
                # Outside Edge
                # CASE 3
                # print('Outside Edge : {} = {}'.format(point, data_points[point]['temp']))
                # For this area, we needed to generate strings to be used as keys that can access information from a neighboring point in the array
                # I copied and pasted this because it throws an error in case 1 and it was slightly faster to do this than write and debug
                # an internal function to do this.
                above_ref = '({},{})'.format(data_points[point]['x_coord'], data_points[point]['y_coord'] + node_size)
                below_ref = '({},{})'.format(data_points[point]['x_coord'], data_points[point]['y_coord'] - node_size)
                left_ref = '({},{})'.format(data_points[point]['x_coord'] - node_size, data_points[point]['y_coord'])
                right_ref = '({},{})'.format(data_points[point]['x_coord'] + node_size, data_points[point]['y_coord'])
                # Here is where we try to gather the temperature information for the node above the current node
                try:
                    above = data_points[above_ref]['temp']
                except:
                    # If we have made it to this part of the code, then the program must be computing the edge piece
                    # in the upper left edge of the section we are calculating. It turns out that by symmetry in the
                    # formula, we can just count the value for the node below as the same as the node above.
                    above = data_points[below_ref]['temp']
                # All of these points should have below points for calculating the bottom left corner of the chimney profile
                try:
                    below = data_points[below_ref]['temp']
                except:
                    below = 0
                try:
                    # Here we are doing the same thing for the horizontal points
                    right = data_points[right_ref]['temp']
                except:
                    # See the previous comment in the except statement above
                    right = data_points[left_ref]['temp']
                # All of these points should have left points for calculating the bottom left corner of the chimney profile
                try:
                    left = data_points[left_ref]['temp']
                except:
                    left = 0
                if (data_points[point]['x_coord'] == 0):
                    data_points[point]['temp'] = (((2 * right) + above + below) + (2 * h_out * delta_x * o_temp / k_brick)) / (2 * ((h_out * delta_x / k_brick) + 2))
                else:
                    data_points[point]['temp'] = (((2 * above) + left + right) + (2 * h_out * delta_x * o_temp / k_brick)) / (2 * ((h_out * delta_x / k_brick) + 2))

            elif (data_points[point]['x_coord'] == inside_corner[0] - node_size and data_points[point]['y_coord'] > inside_corner[1] - node_size) ^ (data_points[point]['y_coord'] == inside_corner[1] - node_size and data_points[point]['x_coord'] > inside_corner[0] - node_size):
                # Inside Edge
                # CASE 3
                # print('Inside Edge : {} = {}'.format(point, data_points[point]['temp']))
                # For this area, we needed to generate strings to be used as keys that can access information from a neighboring point in the array
                # I copied and pasted this because it throws an error in case 1 and it was slightly faster to do this than write and debug
                # an internal function to do this.
                above_ref = '({},{})'.format(data_points[point]['x_coord'], data_points[point]['y_coord'] + node_size)
                below_ref = '({},{})'.format(data_points[point]['x_coord'], data_points[point]['y_coord'] - node_size)
                left_ref = '({},{})'.format(data_points[point]['x_coord'] - node_size, data_points[point]['y_coord'])
                right_ref = '({},{})'.format(data_points[point]['x_coord'] + node_size, data_points[point]['y_coord'])
                # Here is where we try to gather the temperature information for the node above the current node
                try:
                    above = data_points[above_ref]['temp']
                except:
                    # If we have made it to this part of the code, then the program must be computing the edge piece
                    # in the upper left edge of the section we are calculating. It turns out that by symmetry in the
                    # formula, we can just count the value for the node below as the same as the node above.
                    above = data_points[below_ref]['temp']
                # All of these points should have below points for calculating the bottom left corner of the chimney profile
                below = data_points[below_ref]['temp']
                try:
                    # Here we are doing the same thing for the horizontal points
                    right = data_points[right_ref]['temp']
                except:
                    # See the previous comment in the except statement above
                    right = data_points[left_ref]['temp']
                # All of these points should have left points for calculating the bottom left corner of the chimney profile
                left = data_points[left_ref]['temp']
                if (data_points[point]['x_coord'] == inside_corner[0] - node_size and data_points[point]['y_coord'] > inside_corner[1] - node_size):
                    data_points[point]['temp'] = (((2 * left) + above + below) + (2 * h_in * delta_x * i_temp / k_brick)) / (2 * ((h_in * delta_x / k_brick) + 2))
                else:
                    data_points[point]['temp'] = (((2 * below) + left + right) + (2 * h_in * delta_x * i_temp / k_brick)) / (2 * ((h_in * delta_x / k_brick) + 2))
            elif (data_points[point]['x_coord'] == inside_corner[0] - node_size) and (data_points[point]['y_coord'] == inside_corner[1] - node_size):
                # Inside Corner
                # print('Inside Corner : {} = {}'.format(point, data_points[point]['temp']))
                # For this area, we needed to generate strings to be used as keys that can access information from a neighboring point in the array
                # I copied and pasted this because it throws an error in case 1 and it was slightly faster to do this than write and debug
                # an internal function to do this.
                above_ref = '({},{})'.format(data_points[point]['x_coord'], data_points[point]['y_coord'] + node_size)
                below_ref = '({},{})'.format(data_points[point]['x_coord'], data_points[point]['y_coord'] - node_size)
                left_ref = '({},{})'.format(data_points[point]['x_coord'] - node_size, data_points[point]['y_coord'])
                right_ref = '({},{})'.format(data_points[point]['x_coord'] + node_size, data_points[point]['y_coord'])
                # For this particular point, we know that it is guaranteed to have 4 neighbors so we don't need to fool
                # around with that try and except business
                above = data_points[above_ref]['temp']
                below = data_points[below_ref]['temp']
                right = data_points[right_ref]['temp']
                left = data_points[left_ref]['temp']
                # Perform the calculation and store the data point temperature in this node
                data_points[point]['temp'] = (2 * (left + below) + (right + above) + (2 * h_in * delta_x * i_temp / k_brick))/ (2 * (3 + h_in * delta_x / k_brick))

            else:
                # Interior piece
                # For this area, we needed to generate strings to be used as keys that can access information from a neighboring point in the array
                # I copied and pasted this because it throws an error in case 1 and it was slightly faster to do this than write and debug
                # an internal function to do this.
                above_ref = '({},{})'.format(data_points[point]['x_coord'], data_points[point]['y_coord'] + node_size)
                below_ref = '({},{})'.format(data_points[point]['x_coord'], data_points[point]['y_coord'] - node_size)
                left_ref = '({},{})'.format(data_points[point]['x_coord'] - node_size, data_points[point]['y_coord'])
                right_ref = '({},{})'.format(data_points[point]['x_coord'] + node_size, data_points[point]['y_coord'])
                # Here is where we try to gather the temperature information for the node above the current node
                try:
                    above = data_points[above_ref]['temp']
                except:
                    # If we have made it to this part of the code, then the program must be computing the edge piece
                    # in the upper left edge of the section we are calculating. It turns out that by symmetry in the
                    # formula, we can just count the value for the node below as the same as the node above.
                    above = data_points[below_ref]['temp']
                # All of these points should have below points for calculating the bottom left corner of the chimney profile
                below = data_points[below_ref]['temp']
                try:
                    # Here we are doing the same thing for the horizontal points
                    right = data_points[right_ref]['temp']
                except:
                    # See the previous comment in the except statement above
                    right = data_points[left_ref]['temp']
                # All of these points should have left points for calculating the bottom left corner of the chimney profile
                left = data_points[left_ref]['temp']
                # Perform the calculation and store the data point temperature in this node
                data_points[point]['temp'] = (above + below + left + right)/4
            # Now that a new temperature value has been generated, find the estimated error by using the movement from the last iteration
            # Add this value to the sum of the rest of point errors for this iteration
            point_error += abs((data_points[point]['temp'] - data_points[point]['old_temp']) / data_points[point]['temp']) * 100
        # I decided to use the mean error among all of the data points individually to determine when the error threshold has been met.
        # c_error contains the current error for this iteration
        c_error = point_error/len(data_points)
        print(c_error)
    pprint.pprint(data_points)
    # PLOTTING
    # First we need to generate a list of all of the data points. Since we only calculated a quarter
    # of the chimney space, the rest of the point matrix needs to be rebuilt from the quarter size
    # data set. The end result will be a list of tuples (x, y, temp) for all of the points in the
    # specified geometry
    plot_data = []
    for i in x_points:
        for j in y_points:
            # generate a string to access the elements in the data point dictionary
            ref = '({},{})'.format(i,j)
            try:
                # If the reference point is within the geometry of the points we calculated,
                # then generate data for the three other points that will be the same as this
                # point by symmetry.
                plot_data.append((i,j,data_points[ref]['temp']))
                plot_data.append((x_outside - i,j,data_points[ref]['temp']))
                plot_data.append((i,y_outside - j,data_points[ref]['temp']))
                plot_data.append((x_outside - i, y_outside - j,data_points[ref]['temp']))
            except:
                # If the program gets to this portion of the code, then i and j point to coordinates
                # that are within the inside of the chimney, so this can be set to the internal air temperature
                # These points still need their corresponding symmetrical points filled in for it to
                # look cool
                plot_data.append((i,j,i_temp))
                plot_data.append((x_outside - i,j,i_temp))
                plot_data.append((x_outside - i, y_outside - j,i_temp))
                plot_data.append((i, y_outside - j,i_temp))
    # These list comprehensions store the data in vertical slices to be fed into the scatter plot function
    x_list = np.array([item[0] for item in plot_data])
    y_list = np.array([item[1] for item in plot_data])
    z_list = np.array([item[2] for item in plot_data])
    # Plot points and jack with settings until it looks good
    plt.scatter(x_list, y_list, c=z_list, cmap=cm.inferno, marker='s', s=node_size**2.5)
    # Add labels ant titles I guess
    plt.title('Chimney Heat Distribution Map', y=1.05)
    plt.xlabel('X - Axis Location (mm)')
    plt.ylabel('Y - Axis Location (mm)')
    plt.xticks(np.arange(0, x_outside + 10, 10),rotation='45')
    plt.yticks(np.arange(0, y_outside + 10, 10))
    # Dicking with settings until I get the plot area to show up the way I want to.
    # I am not sure that all of these are even doing anything at this point but it
    # prints a pretty graph so I am done messing with it.
    plt.colorbar(shrink=0.75,label='Temperature (C)')
    plt.grid(True, linestyle='dotted')
    plt.axes().set_aspect('equal','datalim')
    # I think that this is the most important setting in deciding the plot area and shape of the
    # axes. Sets padding for the plot. Pyplot is still easier to use than excel.
    plt.subplots_adjust(left=.15, right=0.99, bottom=.2, top=.85)
    # SAVE IT AND YOU ARE DONE! YAY
    plt.savefig('ME_399_chimney_diagram.png', bbox_inches='tight')
    # By default the plot collapses after the show command, so this line must be the last one to execute
    plt.show()

chimney_problem()
