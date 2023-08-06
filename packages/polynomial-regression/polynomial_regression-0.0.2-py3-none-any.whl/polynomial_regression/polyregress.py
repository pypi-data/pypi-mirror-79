try:
    import numpy as np
except ModuleNotFoundError:
    raise ModuleNotFoundError("Numpy must be installed for polynomial_regression to work")

class polynomial_regression:
    def regress(x,y,n=1):
        '''
        x is the set of x-coordinates of points to be fit. A 1-D list is required. Pass a np.ndarray to reduce time.
        y is the set of y-coordinates of points to be fit. A 1-D list is required. Pass a np.ndarray to reduce time.
        n is the degree of the polynomial to fit.

        May Raise Singular Matrix Error iff n>number of points.

        Returns c such that c[i] is the coefficient of x^i in the polynomial.
        Precision to at least 8 digits after decimal points is achieved.  
        '''
        
        x=np.asarray(x)
        y=np.asarray(y)
        if(x.shape!=y.shape):
            raise ValueError("Shape of both x and y must be same, and greater than n")

        X=np.zeros((n+1, n+1))
        for i in range(n+1):
            for j in range(i,n+1):
                X[i][j]=np.sum(x**(i+j))
                X[j][i]=X[i][j]
    
        Y=np.zeros((n+1))
        
        for i in range(n+1):
            Y[i]=np.sum(np.multiply(y, x**(i)))
        
        c=np.linalg.solve(X, Y)
        
        return c
