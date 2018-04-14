def prob_1():
    '''
    An electronics package was evaluated for survival to abnormal drop environments.
    A capacitive displacement sensor with signal conditioning calculated the
    deflections (D) as a result of the hard impact. From the data in drop1.csv,
    determine the velocity at impact, the height of freefal, and the macimum G's
    imparted on the electronics module.
    '''
    import numpy as np
    import matplotlib.pyplot as plt
    import os
    degree_fit = 5 # Degree of polynomial fit

    if 'drop1.csv' in os.listdir('.'):
        x, y = np.loadtxt(open('drop1.csv'),delimiter=',',unpack=True,skiprows=2)
        stdev = np.std(y)
        regress = np.polyfit(x,y,deg=degree_fit)

        def dxdt(val,eqn=regress):
            ans = []
            for index, coef in enumerate(eqn):
                if (len(eqn)-(index+2)) >= 0:
                    ans.append((len(eqn)-(index+1))*coef*val**(len(eqn)-(index+2)))
            return sum(ans)

        def d2xdt2(val, eqn=regress):
            ans = []
            for index, coef in enumerate(eqn):
                if (len(eqn)-(index+3)) >= 0:
                    ans.append(((len(eqn)-(index+2))*(len(eqn)-(index+1))*coef*val**(len(eqn)-(index+3))))
            return sum(ans)

        # Anonymous function - input value and vector of polynomial coefficients and returns function output
        ret_poly = lambda val, eqn : sum([coef*val**(len(eqn)-(index+1)) for index, coef in enumerate(eqn)])
        # List comprehensions for computing displacement
        y_vals = np.array([ret_poly(i, regress) for i in x])
        min_d_index, min_d_val = min(enumerate(y), key=lambda p: p[1])
        # print('Maximum Deflection: {:.4f} in. at Time : {:.6f} s'.format(min_d_val, x[min_d_index]))
        # Compute velocity
        y_vel = np.array([dxdt(i, regress) for i in x])
        vel_zero_x = bisection(dxdt, x[1], x[-1])
        # print('Zero Velocity at t = {:.6f} seconds.'.format(vel_zero_x))
        # Compute acceleration
        accel = np.array([d2xdt2(i, regress) for i in x])
        accel_zero_1x = bisection(d2xdt2, x[1], vel_zero_x)
        # print('Zero Acceleration 1 at t = {:.6f} seconds.'.format(accel_zero_1x))
        accel_zero_2x = bisection(d2xdt2, vel_zero_x, x[-1])
        # print('Zero Acceleration 2 at t = {:.6f} seconds.'.format(accel_zero_2x))
        # Residuals for goodness of fit
        err = (1 - sum([(((y[i] - y_vals[i])/stdev)**2) for i, _ in enumerate(x)]))**(0.5)
        g = 9.81*(3.28084)*(12) # convert gravity to inches/second^2
        height = (dxdt(accel_zero_1x)**2)/(2*g)
        max_accel = d2xdt2(vel_zero_x)
        max_g = (max_accel/g)
        print('Maximum Velocity of {} in/s at t = {}'.format(dxdt(accel_zero_1x),accel_zero_1x))
        print('Freefall Height = {} feet'.format(height/12))
        print('Maximum G Force = {} Gs'.format(max_g))

        plt.plot(x,y,label='Data Points')
        plt.plot(x,y_vals,linestyle='--',color='red',label='${}^t$$^h$ - Degree Poly-fit $R^2$ : {:.4f}'.format(degree_fit,err))
        plt.scatter(x[min_d_index], min_d_val,label='Maximum Deflection: {:.4f} in. at Time : {:.6f} s'.format(min_d_val, x[min_d_index]))
        plt.xlabel('Time (s)')
        plt.ylabel('Displacement (x)')
        plt.title('Impact and Displacement')
        plt.subplots_adjust(left=.15, right=0.90, bottom=.1, top=.9)
        plt.legend(loc="upper left")
        plt.savefig('me352_p1_displacement.png', bbox_inches='tight')
        plt.show()

        plt.plot(x, y_vel, label='Velocity')
        plt.scatter(vel_zero_x, dxdt(vel_zero_x),label='Zero Velocity at {:.6f} seconds.'.format(vel_zero_x),color='red')
        plt.scatter(accel_zero_1x, dxdt(accel_zero_1x),label='Min Velocity of {:.6f} at {:.6f} seconds.'.format(dxdt(accel_zero_1x),accel_zero_1x), color='red')
        plt.scatter(accel_zero_2x, dxdt(accel_zero_2x),label='Max Velocity of {:.6f} at {:.6f} seconds.'.format(dxdt(accel_zero_2x),accel_zero_2x), color='red')
        plt.xlabel('Time (s)')
        plt.ylabel('Velocity (in/s)')
        plt.title('Impact and Velocity')
        plt.legend(loc="upper left")
        plt.savefig('me352_p1_velocity.png', bbox_inches='tight')
        plt.show()

        plt.plot(x, accel, label='Acceleration')
        plt.scatter(accel_zero_1x, d2xdt2(accel_zero_1x),label='Zero Accel 1 at {:.6f} seconds.'.format(accel_zero_1x), color='red')
        plt.scatter(accel_zero_2x, d2xdt2(accel_zero_2x),label='Zero Accel 2 at {:.6f} seconds.'.format(accel_zero_2x), color='red')
        plt.scatter(vel_zero_x, d2xdt2(vel_zero_x),label='Max. Accel of {:.6f} at {:.6f} seconds.'.format(d2xdt2(vel_zero_x),vel_zero_x), color='red')
        plt.xlabel('Time (s)')
        plt.ylabel('Acceleration (in/$s^2$)')
        plt.title('Impact and Acceleration')
        plt.subplots_adjust(left=.2, right=0.95, bottom=.1, top=.9)
        plt.legend(loc="lower left")
        plt.savefig('me352_p1_accel.png', bbox_inches='tight')
        plt.show()

def bisection(funct, lowerguess, upperguess, er_limit=0.00001, max_iter=100):
    '''
    Numerical Methods - Roots of Functions
    Bisection Method:
    + As a bracketing method, this will always converge
    - Requires 2 initial conditions that bracket the root
    - Can be slow to converge
    - Does not find multiple or complex roots.
    Select two x-values that yield function outputs of opposite sign and
    this function performs bisection to find the root.
    funct : Function to evaluate the root
    lowerguess : Initial lower guess for x
    upperguess : Initial upper guess for x
    er_limit : Desired approximate error
    max_iter : Maximum number of iterations allowed
    '''
    # Find the point information from the function
    x_lower = lowerguess
    y_lower = funct(lowerguess)
    x_upper = upperguess
    y_upper = funct(upperguess)
    # Initialize an x guess
    x_guess = x_lower
    # While current error is outside the desired estimate and we are
    # within the iteration limit
    for iter_no in range(max_iter):
    # while c_error > er_limit and i_count < max_iter:
        # Store the previous value
        old_guess = x_guess
        # Generate a new guess for an x-value
        x_guess = (x_lower + x_upper) / 2
        # Create the corresponding y-value from the input function
        y_guess = funct(x_guess)
        # If the output from the guess and the lower bound are on the
        # same side of the x-axis.
        if y_guess * y_lower > 0:
            # The lower bound needs to be adjusted to the new guess
            x_lower = x_guess
            y_lower = y_guess
        elif y_guess * y_upper > 0:
            # Otherwise the other boundary needs to be adjusted
            x_upper = x_guess
            y_upper = y_guess
        else:
            # A true zero has been found
            break
        # Calculate the current Error for this iteration
        c_error = abs((x_guess - old_guess) / x_guess)
        if c_error < er_limit:
            # print('Bisection Method Error threshold reached')
            break
    # Print the output
    # print('Bisection Method Results : \n')
    # print('Approximated Value : {}'.format(x_guess))
    # print('Function Output : {}'.format(y_guess))
    # print('Estimated Error : {}'.format(c_error))
    # print('Iteration Count : {}'.format(iter_no + 1))
    # Returns the coordinates of the most recent guess
    return x_guess

def lin_fit(x_list, y_list):
    '''
    Generates linear regression best fit line for list of x-values and y-values passed in the form of a list
    Returns coefficients for the form y = a * x + b
    a, b, r_squared, std_er, er_max = lin_fit(x_list, y_list)
    a : a-coefficient
    b : intercept offset
    r_squared : correlation coefficient
    std_er : standard error
    er_max : maximum error
    '''
    n = len(x_list)
    if n != len(y_list):
        print('Lists must be of equal length.')
    s_xi = sum(x_list)
    s_yi = sum(y_list)
    y_mean = s_yi/n
    s_xi2 = sum([i**2 for i in x_list])
    s_yi2 = sum([i**2 for i in y_list])
    s_xy = sum([x_list[i]*y_list[i] for i in range(n)])
    # Calculate coefficients
    coef_a = ((n * s_xy) - (s_xi * s_yi)) / ((n * s_xi2) - (s_xi**2))
    coef_b = ((s_xi2 * s_yi) - (s_xi * s_xy)) / ((n*s_xi2) - (s_xi**2))
    # Break numerator and denominator calculations down for R-Square calculation
    r2_num = sum([((coef_a * x_list[i] + coef_b - y_list[i])**2) for i in range(n)])
    # Find maximum error deviation from the best fit line
    er_max = max([abs(coef_a * x_list[i] + coef_b - y_list[i]) for i in range(n)])
    r2_den = sum([(y_list[i] - y_mean)**2 for i in range(n)])
    # R-Squared Value - coefficient of determination
    r_sq = 1 - (r2_num / r2_den)
    # Standard error
    std_er = (r2_num/(n-2))**(0.5)
    return coef_a, coef_b, r_sq, std_er, er_max
    

def prob_3():
    deflect = [0.00, 1.25, 2.50, 3.75, 5.00]
    v_out = [0.10, 0.65, 1.32, 1.95, 2.70]
    m, b, r2, se, me= lin_fit(deflect, v_out)
    print('Linear Best Fit: y = {:.4f} * x + {:.4f}'.format(m,b))
    print('R-Squared, Calibration Constant = {:.4f}'.format(r2))
    print('Standard Error = {:.4f}'.format(se))
    print('Maximum Error = {:.4f}'.format(me))
    



prob_1()
# prob_3()