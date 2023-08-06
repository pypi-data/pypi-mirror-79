import numbers
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class Functions:
    def __version__():
        return "1.0"
    
    def __init__(self):
        pass
    
    def AssertNumber(x):
        if isinstance(x, numbers.Number)==False:
            raise Exception("Sorry, you must use just numbers!")

    def trimf(x, a, b, c):
        """Triangular Pertinence Function (trimf).
        The triangular curve is a function of 'x', and depends on three scalar parameters [a b c].
        The parameters 'a' and 'c' correspond to the values of X located at the vertices at the base of the triangle, 
        which have a pertinence equal to zero. The 'b' parameter is the value of X located at the vertex with relevance equal to 1.
        """
        AssertNumber(x)
        AssertNumber(a)
        AssertNumber(b)
        AssertNumber(c)        
        return max( min( (x-a)/(b-a), (c-x)/(c-b) ), 0 )

    def GenerateRangeX(start,end,unit):
        """Returns a vector within range a and b. The unit defines the amount to be used. 
        Example 1: vector between 1 and 10, with unit 1 will return 1,2,3,4,5 ...
        Example 2: vector between 1 and 10, unit 0.1 will return 1, 1.1, 1.2,1.3, etc.
        """
        return np.arange(start,end,unit)

    def TriangFuzzification(x, fuzzy_sets):
        """ The process of fuzzification.
        Parameters:
        x (numeric): required value of x, deterministic value.
        fuzzy_sets (dictionary): the defined fuzzy sets with values.
        Example: 
        temperature={
            'Low':[-1,0,10],
            'Middle':[11,20,25],
            'High':[26,35,40]
        }

        Returns:
        Pandas Dataframe. The index is the fuzzy sets and columns variable X
        """
        return pd.DataFrame(list(map(lambda y:trimf(x, *fuzzy_sets[y]), fuzzy_sets.keys())),
                            index=list(fuzzy_sets.keys()),
                           columns=["X"])

    def TriangFuzzificationVector(X, fuzzy_sets):
        """ The process of fuzzification.
        Parameters:
        x (vector): required values of x, deterministic value as a vector.
        Example
        fuzzy_sets (dictionary): the defined fuzzy sets with values.
        Example: array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        temperature={
            'Low':[-1,0,10],
            'Middle':[11,20,25],
            'High':[26,35,40]
        }

        Returns:
        Pandas DataFrame:The index is the vector X and columns are the fuzzy sets.
        """
        return pd.DataFrame([list(map(lambda y:trimf(x,*fuzzy_sets[y]), fuzzy_sets.keys())) for x in X],
                           index=X,
                           columns=list(fuzzy_sets.keys()))

    def DefuzzimetricArc(df,T):
        """ The defuzzimetric arc function.
        Parameters:
        df: dataframe. The index is the X vector and the columns are the y variable.
        T: Factor T (mutation)
        Example
        Returns:
        Pandas DataFrame:The index is the vector X and columns are the fuzzy sets.
        """
        AssertNumber(T)
        return pd.DataFrame([[np.abs((2*df.iloc[x,y]/np.pi)*np.arcsin(np.sin((2*np.pi*df.index[x])/(T)))) for y in range(df.shape[1])] for x in range(df.shape[0])])

    def TNormDefuzzification(df):
        """ The process of defuzzification, using TNorm.
        Parameters:
        df: dataframe. The index is the X vector and the columns are the y variable.
        Example
        Returns:
        Pandas DataFrame:The index is the vector X and columns are the fuzzy sets.
        """
        return pd.DataFrame([[np.abs((2/np.pi*np.arcsin(np.sin(df.index[x]*np.pi/2)*np.sin(df.iloc[x,y]*np.pi/2)))) for y in range(df.shape[1])] for x in range(df.shape[0])])
