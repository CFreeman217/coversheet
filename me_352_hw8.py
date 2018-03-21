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

    def dxdt(val,eqn):
        ans = []
        for index, coef in enumerate(eqn):
            if (len(eqn)-(index+2)) >= 0:
                ans.append((len(eqn)-(index+1))*coef*val**(len(eqn)-(index+2)))
        return sum(ans)

    def d2xdt2(val, eqn):
        ans = []
        for index, coef in enumerate(eqn):
            if (len(eqn)-(index+3)) >= 0:
                ans.append(((len(eqn)-(index+2))*(len(eqn)-(index+1))*coef*val**(len(eqn)-(index+3))))
        return sum(ans)

    if 'drop1.csv' in os.listdir('.'):
        x, y = np.loadtxt(open('drop1.csv'),delimiter=',',unpack=True,skiprows=2)
        stdev = np.std(y)
        regress = np.polyfit(x,y,deg=degree_fit)
        # Anonymous function - input value and vector of polynomial coefficients and returns function output
        ret_poly = lambda val, eqn : sum([coef*val**(len(eqn)-(index+1)) for index, coef in enumerate(eqn)])
        # List comprehensions for computing displacement
        y_vals = np.array([ret_poly(i, regress) for i in x])
        min_index, min_val = min(enumerate(y), key=lambda p: p[1])

        print('Maximum Deflection: {:.4f} in. at Time : {:.6f} s'.format(min_val, x[min_index]))
        # Compute velocity
        y_vel = np.array([dxdt(i, regress) for i in x])
        # Compute acceleration
        accel = np.array([d2xdt2(i, regress) for i in x])
        # Residuals for goodness of fit
        err = 1 - sum([(((y[i] - y_vals[i])/stdev)**2) for i, _ in enumerate(x)])
        print(err)

        plt.plot(x,y,label='Data Points')
        plt.plot(x,y_vals,linestyle='--',color='red',label='${}^t$$^h$ - Degree Poly-fit $R^2$ : {:.4f}'.format(degree_fit,err))
        plt.scatter(x[min_index], min_val,label='Maximum Deflection: {:.4f} in. at Time : {:.6f} s'.format(min_val, x[min_index]))
        plt.xlabel('Time (s)')
        plt.ylabel('Displacement (x)')
        plt.title('Impact and Displacement')
        plt.subplots_adjust(left=.15, right=0.90, bottom=.1, top=.9)
        plt.legend()
        plt.show()

        plt.plot(x, y_vel, label='Velocity')
        plt.xlabel('Time (s)')
        plt.ylabel('Velocity (in/s)')
        plt.title('Impact and Velocity')
        plt.legend()
        plt.show()

        plt.plot(x, accel, label='Acceleration')
        plt.xlabel('Time (s)')
        plt.ylabel('Acceleration (in/$s^2$)')
        plt.title('Impact and Acceleration')
        plt.subplots_adjust(left=.2, right=0.95, bottom=.1, top=.9)
        plt.legend()
        plt.show()






prob_1()