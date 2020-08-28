#pi estimation with python
import random #import random number generator module
import numpy #to handle numpy calls in test_input.py
import numpy as np #importing numpy module with alias np
import matplotlib.pyplot as plt #importing the plotting functionality of matplotlib
import time #importing time function to test time efficiency of code
import traceback #error tracking
import arcpy #esri geoprocessing module
#all code is in python 2.7

class Error_EmptyArray(Exception):
    pass #handle empty array error
class Error_ArraySizeDifferent(Exception):
    pass #handle different size array error

def estimate_pi_python(samples):
    #estimate pi using python code only
    num_darts_in_circle = 0.0 #counrter for points inside the circle
    for x in range(samples): #iterae through number of samples and generate random points
        random_val = random.random() #generate random number between 0 and 1
        random_val -= 0.5 #reduce random number by half the range
        X = random_val #assign the random value to the X variable
        random_val = random.random() 
        random_val -= 0.5
        Y = random_val
        distance = (X**2 + Y**2)**0.5 #square-root of sum of squares
        if distance <= 0.5: #count values inside teh radius of the circle
            num_darts_in_circle +=1
    return (num_darts_in_circle/samples)*4 #return the pi value which is a multiplied by 4 to capture all the quads of the darts.

def estimate_pi_numpy(samples):
    X = np.random.random_sample((samples,)) - 0.5
    Y = np.random.random_sample((samples,)) - 0.5
    distance_array = np.sqrt(X**2 + Y**2)
    distance_boolean = distance_array <= 0.5
    num_darts_in_circle = float(sum(distance_boolean))
    return (num_darts_in_circle/samples)*4

def plot_darts(samples):
    X = np.random.random_sample((samples,)) - 0.5
    Y = np.random.random_sample((samples,)) - 0.5
    distance_array = np.sqrt(X**2 + Y**2)
    distance_boolean = distance_array <= 0.5
    dart_color_array = distance_boolean.astype(np.int)
    color_map = np.array(['r','g'])
    plt.scatter(X, Y, c=color_map[dart_color_array])
    plt.show()
def estimate_pi_anotherway(samples):
    #https://www.pythonlikeyoumeanit.com/Module3_IntroducingNumpy/Problems/Approximating_pi.html
    M = samples
    N = 1
    dart_positions = np.random.rand(M, N, 2) * 2 - 1               # shape-(M, N, 2) array of positions
    dist_from_origin = np.sqrt((dart_positions**2).sum(axis=2))    # shape-(M, N) array of distances
    is_in_circle = dist_from_origin <= 1                           # shape-(M, N) boolean array
    num_thrown = np.arange(1, N+1)  # 1, 2, ..., N, shape=(N,)
    num_in_circle = np.cumsum(is_in_circle, axis=1)  # shape-(M, N)
    # broadcast-divide to produce approximations of pi across all
    # M trials
    running_estimate = 4 * num_in_circle / num_thrown
    return np.average(running_estimate)
try:
    # Test Input
    print "***Part I***"
    n_samples = 1000000
    actual = numpy.pi
    start = time.clock()
    pi_est = estimate_pi_python(n_samples)
    python_runtime = time.clock() - start
    print 'Estimated value (Python):', pi_est
    print 'Percent (%) error (Python):', numpy.abs(pi_est - actual) / actual * 100
    print 'Total CPU time (sec) to run (Python):', python_runtime
    start = time.clock()
    pi_est = estimate_pi_numpy(n_samples)
    numpy_runtime = time.clock() - start
    print 'Estimated value (NumPy):', pi_est
    print 'Percent (%) error (NumPy):', numpy.abs(pi_est - actual) / actual * 100
    print 'Total CPU time (sec) to run (NumPy):', numpy_runtime
    print 'Using NumPy is',python_runtime / numpy_runtime, 'times faster than standard Python!'

    start = time.clock()
    pi_est = estimate_pi_anotherway(n_samples)
    numpy2_runtime = time.clock() - start
    print 'Estimated value (Numpy2):', pi_est
    print 'Total CPU time (sec) to run (Numpy2):', numpy_runtime
    print 'Percent (%) error (Numpy2):', numpy.abs(pi_est - actual) / actual * 100
    print 'Using NumPy is',python_runtime / numpy2_runtime, 'times faster than standard Python!'
    
    n_samples = 5000
    plot_darts(n_samples)
    
except Error_EmptyArray:
  print("Error: One of your input arrays is empty!")
except Error_ArraySizeDifferent:
  print("Error: Your input arrays are not the same length!")

except Exception as e:
    print(traceback.format_exc()) #error unsuppression for debugging
    print "Error: " + str(e) # Prints Python-related errors


#sources:
# sources for estimation of pi using Monte Carlo Simulation
#   estimation pi using python with random module only:
#   http://www.stealthcopter.com/blog/2009/09/python-calculating-pi-using-random-numbers/
#   https://towardsdatascience.com/how-to-make-pi-part-1-d0b41a03111f
#   https://gist.github.com/louismullie/3769218
#   https://www.geeksforgeeks.org/estimating-value-pi-using-monte-carlo/
#   https://stackoverflow.com/questions/46751718/calculate-pi-using-random-numbers  
#  using numpy module:
#   https://www.youtube.com/watch?v=X5kdy29rX1U
#   https://galeascience.wordpress.com/2016/03/02/approximating-pi-with-monte-carlo-simulations/
#   https://glowingpython.blogspot.com/2012/01/monte-carlo-estimate-for-pi-with-numpy.html
#   https://www.kaggle.com/nickgould/monte-carlo-tutorial-calculating-pi
#   https://idrack.org/blog/2018/02/03/python-monte-carlo-simulation-calculate-pi/ 
# source for plotting pi estimatition using matplotlin module pyplot functionality:
#   https://www.machinelearningplus.com/plots/matplotlib-tutorial-complete-guide-python-plot-examples/
#   https://www.tutorialspoint.com/matplotlib/matplotlib_tutorial.pdf
#   https://python4astronomers.github.io/plotting/matplotlib.html
#   https://matplotlib.org/api/pyplot_api.html
#   https://www.oreilly.com/library/view/python-data-science/9781491912126/ch04.html
#   https://www.python-course.eu/matplotlib.php\
#check for empty arrays, exit if one or more are empty using numpy multi-dimension size check
#https://stackoverflow.com/questions/11295609/how-can-i-check-whether-a-numpy-array-is-empty-or-not
