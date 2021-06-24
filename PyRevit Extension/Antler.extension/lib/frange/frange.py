import numpy as _np

class frange():
    """
    Return an object can be used to generate a generator or an array 
    of floats from start (inclusive) to stop (exclusive) by step. 
    This object stores the start, stop, step and length of
    the data. Uses less memory than storing a large array.

    Example
    -------
    An example of how to use this class to generate some data is
    as follows for some time data between 0 and 2 in steps of
    1e-3 (0.001)::

        you can create an frange object like so
        $ time = frange(0, 2, 1e-3)

        you can print the length of the array it will generate
        $ printlen(time) # prints length of frange, just like an array or list

        you can create a generator
        $ generator = time.get_generator() # gets a generator instance
        $ for i in generator: # iterates through printing each element
        $     print(i)

        you can create a numpy array
        $ array = time.get_array() # gets an array instance
        $ newarray = 5 * array # multiplies array by 5

        you can also get the start, stop and step by accessing the slice parameters
        $ start = time.slice.start
        $ stop = time.slice.stop
        $ step = time.slice.step

    """
    def __init__(self, start, stop, step):
        """
        Intialises frange class instance. Sets start, top, step and 
        len properties.

        Parameters
        ----------
        start : float
            starting point
        stop : float
            stopping point 
        step : float
           stepping interval
        """
        self.slice = slice(start, stop, step)
        self.len = self.get_array().size
        return None

    def get_generator(self):
        """
        Returns a generator for the frange object instance.

        Returns
        -------
        gen : generator
            A generator that yields successive samples from start (inclusive)
            to stop (exclusive) in step steps.
        """
        s = self.slice
        gen = drange(s.start, s.stop, s.step) # intialises the generator
        return gen
    
    def get_array(self):
        """
        Returns an numpy array containing the values from start (inclusive)
        to stop (exclusive) in step steps.

        Returns
        -------
        array : ndarray
            Array of values from start (inclusive)
            to stop (exclusive) in step steps.
        """
        s = self.slice        
        array = _np.arange(s.start, s.stop, s.step)
        return array

#    def __array__(self): # supposedly allows numpy to treat object itself as an array but it doesn't work?
#        array = self.get_array()
#        return array
    
    def __len__(self):
        return self.len


def drange(start, stop, step):
    """
    A generator that yields successive samples from start (inclusive)
    to stop (exclusive) in step intervals.

    Parameters
    ----------
    start : float
        starting point
    stop : float
        stopping point 
    step : float
        stepping interval

    Yields
    ------
    x : float
        next sample
    """
    x = start
    if step > 0:
        while x + step <= stop: # produces same behaviour as numpy.arange
            yield x
            x += step
    elif step < 0:
        while x + step >= stop: # produces same behaviour as numpy.arange
            yield x
            x += step
    else:
        raise ZeroDivisionError("Step must be non-zero")
    
