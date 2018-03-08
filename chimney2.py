import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import pprint
def chimney():
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
    node_size = 5 # Square node side length (mm)

    # Geometry
    x_outside = 180 # mm
    x_inside = 100 # mm
    y_outside = 120 # mm
    y_inside = 40 # mm

    # Error estimation and iteration limits
    c_error = 100 # Current error percentage
    er_max = .5 # Maximum error tolerance
    c_iter = 0 # Instantiate iterations
    iter_max = 1000 # Maximum iterations
    init_temp = 0 # Initial temp to start the iterator
    delta_x = node_size/1000 # Physical size of the node in meters

    # Heat Transfer
    in_temp = 380 # Inside temp (C)
    h_in = 85 # Inside convection coefficient
    out_temp = 35 # Outside temp
    h_out = 22 # Outside convection coefficient
    k_brick = 4.1 # conduction coefficient for fire bricks

    # Chop the diagram and generate points
    cols_x = int((x_outside / (2 * node_size)) + 1)
    rows_y = int((y_outside / (2 * node_size)) + 1)
    # find the inner edges
    ineg_x = int((cols_x - (x_inside/(2*node_size)) - 1))
    ineg_y = int((rows_y - (y_inside/(2*node_size)) - 1))
    # Generate an array of dictionaries to hold the values we need
    node_matrix = np.array([[{'temp':init_temp, 'oldtemp' : 0, 'OB' : False} for i in range(cols_x)] for j in range(rows_y)])
    # While we are under the iteration limit and outside the error threshold...
    while c_error > er_max and c_iter < iter_max:
        # cycle the iterator
        c_iter += 1
        # Set the current error
        tot_er = 0
        # instantiate min and max temp. assumes the object is being heated from the inside
        max_temp = out_temp
        min_temp = in_temp
        # Break the node array into an indexed list
        for y_index, row in enumerate(node_matrix):
            # break the rows into an indexed list. Each instance of col is an instance of the dictionary
            for x_index, col in enumerate(row):
                # Store the old value
                col['oldtemp'] = col['temp']
                # BEGIN CRAZY ZONE
                # nested if statements suck because they are hard to understand
                if x_index == 0:
                    # left side
                    if y_index == 0:
                        # Lower Left Corner
                        above = node_matrix[y_index + 1][x_index]['temp']
                        right = node_matrix[y_index][x_index + 1]['temp']
                        # special calculation for this corner only
                        col['temp'] = (above + right + (2 * h_out * delta_x * out_temp / k_brick)) / (2 * ((h_out * delta_x / k_brick) + 1))
                    else:
                        # Left Column
                        if y_index == rows_y - 1:
                            # Top Outside Left Edge
                            above = node_matrix[y_index - 1][x_index]['temp']
                        else:
                            # Outside Left Edge
                            above = node_matrix[y_index + 1][x_index]['temp']
                        below = node_matrix[y_index - 1][x_index]['temp']
                        right = node_matrix[y_index][x_index + 1]['temp']
                        # similar to 3 other regions but this way seems to work better.
                        col['temp'] = (2 * right + above + below + (2 * h_out * delta_x * out_temp / k_brick)) / (2 * ((h_out * delta_x / k_brick) + 2))

                elif x_index > 0 and y_index == 0:
                    # Bottom Edge
                    if x_index == cols_x - 1:
                        # Outside Bottom Right Edge
                        right = node_matrix[y_index][x_index - 1]['temp']
                    else:
                        # Outside Bottom Edge
                        right = node_matrix[y_index][x_index + 1]['temp']
                    above = node_matrix[y_index + 1][x_index]['temp']
                    left = node_matrix[y_index][x_index - 1]['temp']
                    # see above column temp line
                    col['temp'] = (2 * above + right + left + (2 * h_out * delta_x * out_temp / k_brick)) / (2 * ((h_out * delta_x / k_brick) + 2))

                elif x_index == ineg_x and y_index >= ineg_y:
                    if y_index == ineg_y:
                        # Inside Corner
                        left = node_matrix[y_index][x_index - 1]['temp']
                        right = node_matrix[y_index][x_index + 1]['temp']
                        above = node_matrix[y_index + 1][x_index]['temp']
                        below = node_matrix[y_index - 1][x_index]['temp']
                        # this is a long equation
                        col['temp'] = (2 * (left + below) + above + right + (2 * h_in * delta_x * in_temp / k_brick)) / (2 * (3 + (h_in * delta_x / k_brick)))
                    else:
                        # Inside Edge
                        if y_index == rows_y - 1:
                            # Top Inside Left Edge
                            above = node_matrix[y_index - 1][x_index]['temp']
                        else:
                            # Inside Left Edge
                            above = node_matrix[y_index + 1][x_index]['temp']
                        left = node_matrix[y_index][x_index - 1]['temp']
                        below = node_matrix[y_index - 1][x_index]['temp']
                        col['temp'] = (2 * left + above + below + (2 * h_in * delta_x * in_temp / k_brick)) / (2 * ((h_in * delta_x / k_brick) + 2))
                elif x_index > ineg_x and y_index == ineg_y:
                    # Bottom edge chimney side
                    if x_index == cols_x - 1:
                        # Inside Bottom Right Edge
                        right = node_matrix[y_index][x_index - 1]['temp']
                    else:
                        # Inside Bottom Edge
                        right = node_matrix[y_index][x_index + 1]['temp']
                    left = node_matrix[y_index][x_index - 1]['temp']
                    below = node_matrix[y_index - 1][x_index]['temp']
                    col['temp'] = (2 * below + left + right + (2 * h_in * delta_x * in_temp / k_brick)) / (2 * ((h_in * delta_x / k_brick) + 2))
                elif x_index > ineg_x and y_index > ineg_y:
                    # Out of bounds - these points are inside the chimney
                    col['temp'] = in_temp
                    # do not count these points as part of the error total or min/max range.
                    col['OB'] = True
                else:
                    # Filling pieces
                    if y_index == rows_y - 1:
                        # Inside Top Edge
                        above = node_matrix[y_index - 1][x_index]['temp']
                    else:
                        # this is a core piece
                        above = node_matrix[y_index + 1][x_index]['temp']
                    if x_index == cols_x - 1:
                        # Inside Right Edge
                        right = node_matrix[y_index][x_index - 1]['temp']
                    else:
                        # Core piece
                        right = node_matrix[y_index][x_index + 1]['temp']

                    left = node_matrix[y_index][x_index - 1]['temp']
                    below = node_matrix[y_index - 1][x_index]['temp']
                    col['temp'] = (above + below + left + right) / 4
                # estimated error since last iteration
                this_error = abs((col['temp'] - col['oldtemp'])/col['temp'])*100
                if col['OB'] == False:
                    # if this point is within the geometry of the chimney then count the error
                    tot_er += this_error
                    # finding the minimum temp is easiest here because this dictionary is nested too far
                    if col['temp'] < min_temp:
                        min_temp = col['temp']
                        min_index = [x_index, y_index]
                    if col['temp'] > max_temp:
                        max_temp = col['temp']
                        max_index = [x_index, y_index]
        # set the current error
        c_error = tot_er
    print('Leaving calculation loop with an estimated error of {:.2f} {} after {} iterations.'.format(c_error, '%', c_iter))
    plot_data = []
    # This is a wonky way to do this but i wanted to put a border of outside air around the plot
    for i in range(cols_x + 1):
        # the x-coordinates on the plot are generated from the node size
        x_coord = (i - 1) * node_size
        for j in range(rows_y + 1):
            # store the y-coordinate from the node number and size
            y_coord = (j - 1) * node_size
            # if the coordinate is on the outside, create a point that is equal to exterior air
            if (i == 0) or (j == 0):
                this_temp = out_temp
            else:
                # store the quarter cut matrix value in the temp variable for this run
                this_temp = node_matrix[j-1][i-1]['temp']
            # All of this nonsense is to avoid chopping off or duplicating the edge piece when
            # putting the full size plot back together. Each section is fed in as a tuple so the values stay together.
            # this ends up getting passed as (x, y, temp)
            if (x_coord == (cols_x - 1) * node_size) and (y_coord != (rows_y - 1) * node_size):
                plot_data.append((x_coord, y_coord, this_temp))
                plot_data.append((x_coord, y_outside-y_coord, this_temp))
            if (y_coord == (rows_y - 1) * node_size) and (x_coord != (cols_x - 1) * node_size):
                plot_data.append((x_coord, y_coord, this_temp))
                plot_data.append((x_coord, y_outside-y_coord, this_temp))
            if (y_coord == (rows_y - 1) * node_size) and (x_coord == (cols_x - 1) * node_size):
                plot_data.append((x_coord, y_coord, this_temp))
            else:
                plot_data.append((x_coord, y_coord, this_temp))
                plot_data.append((x_outside - x_coord, y_outside - y_coord, this_temp))
                plot_data.append((x_outside - x_coord, y_coord, this_temp))
                plot_data.append((x_coord, y_outside - y_coord, this_temp))

    # These list comprehensions store the data in vertical slices to be fed into the scatter plot function
    x_list = np.array([item[0] for item in plot_data])
    y_list = np.array([item[1] for item in plot_data])
    z_list = np.array([item[2] for item in plot_data])
    # Plot points and jack with settings until it looks good
    plt.scatter(x_list, y_list, c=z_list, cmap=cm.tab20b, marker='s', s=node_size * 10)

    plt.plot(max_index[0] * node_size, max_index[1] * node_size, 'ro', label='Max. Temp = %.0f $^\circ$C' % max_temp)
    plt.plot(min_index[0] * node_size, min_index[1] * node_size, 'bo', label='Min. Temp = %.0f $^\circ$C' % min_temp)
    plt.legend()
    # Add labels ant titles I guess
    plt.title('Chimney Heat Distribution Map', y=1.05, x=0.33)
    plt.xlabel('X - Axis Location (mm)')
    plt.ylabel('Y - Axis Location (mm)')
    plt.xticks(np.arange(-10, x_outside + 20, 10),rotation='45')
    plt.yticks(np.arange(-10, y_outside + 20, 10))
    # Dicking with settings until I get the plot area to show up the way I want to.
    # I am not sure that all of these are even doing anything at this point but it
    # prints a pretty graph so I am done messing with it.
    plt.colorbar(shrink=0.75,label='Temperature ($^\circ$C)')
    plt.grid(True, linestyle='dotted')
    plt.axes().set_aspect('equal','datalim')
    # I think that this is the most important setting in deciding the plot area and shape of the
    # axes. Sets padding for the plot. Pyplot is still easier to use than excel.
    plt.subplots_adjust(left=.15, right=0.99, bottom=.2, top=.85)
    # SAVE IT AND YOU ARE DONE! YAY
    plt.savefig('ME_399_chimney_diagram.png', bbox_inches='tight')
    # By default the plot collapses after the show command, so this line must be the last one to execute
    plt.show()
chimney()