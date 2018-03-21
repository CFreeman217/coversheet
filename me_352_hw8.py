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
    degree_fit = 4 # Degree of polynomial fit



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
        print('Maximum Deflection: {:.4f} in. at Time : {:.6f} s'.format(min_d_val, x[min_d_index]))
        # Compute velocity
        y_vel = np.array([dxdt(i, regress) for i in x])
        vel_zero_x = bisection(dxdt, x[1], x[-1])
        print('Zero Velocity at t = {:.6f} seconds.'.format(vel_zero_x))
        # Compute acceleration
        accel = np.array([d2xdt2(i, regress) for i in x])
        accel_zero_1x = bisection(d2xdt2, x[1], vel_zero_x)
        print('Zero Acceleration 1 at t = {:.6f} seconds.'.format(accel_zero_1x))
        accel_zero_2x = bisection(d2xdt2, vel_zero_x, x[-1])
        print('Zero Acceleration 2 at t = {:.6f} seconds.'.format(accel_zero_2x))
        # Residuals for goodness of fit
        err = 1 - sum([(((y[i] - y_vals[i])/stdev)**2) for i, _ in enumerate(x)])
        print(err)


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
        plt.scatter(accel_zero_1x, d2xdt2(accel_zero_1x),label='Zero Accel 1 of {:.6f} at {:.6f} seconds.'.format(d2xdt2(accel_zero_1x),accel_zero_1x), color='red')
        plt.scatter(accel_zero_2x, d2xdt2(accel_zero_2x),label='Zero Accel 2 of {:.6f} at {:.6f} seconds.'.format(d2xdt2(accel_zero_1x),accel_zero_1x), color='red')
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
            print('Bisection Method Error threshold reached')
            break
    # Print the output
    # print('Bisection Method Results : \n')
    # print('Approximated Value : {}'.format(x_guess))
    # print('Function Output : {}'.format(y_guess))
    # print('Estimated Error : {}'.format(c_error))
    # print('Iteration Count : {}'.format(iter_no + 1))
    # Returns the coordinates of the most recent guess
    return x_guess

prob_1()