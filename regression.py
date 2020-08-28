#regression analysis code including pi estimation, 
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

def rmse (observed,predicted):
    if predicted.size == 0 or observed.size == 0:
      raise Error_EmptyArray
    if predicted.size != observed.size:
      raise Error_ArraySizeDifferent
    error = predicted - observed
    #2.Calculate Squared Error (SE) = (Error)2
    se = error**2
    #3.Calculate Mean Squared Error (MSE) = Average(SE)
    mse = np.average(se)
    remse = np.sqrt(mse)
    return remse

def r_squared(observed,predicted):
    if predicted.size == 0 or observed.size == 0:
      raise Error_EmptyArray
    if predicted.size != observed.size:
      raise Error_ArraySizeDifferent
    #Yobs = The observed output data (measured)
    Yobs = observed
    #Ymean = The average of the observed output data
    Ymean = np.average(Yobs)
    #Ypred = The predicted output data (modeled)
    Ypred = predicted
    SStot = np.sum(np.square(Yobs-Ymean))
    SSres = np.sum(np.square(Yobs-Ypred))
    rsquared = 1-(np.divide(SSres,SStot))
    return rsquared

def raster_regression(workspace,explanatory,dependent):
    #print "starting raster regression"
    arcpy.CheckOutExtension("Spatial")
    arcpy.env.workspace = workspace #Get the workspace path 
    arcpy.env.overwriteOutput = True #setup overwrite protection status
    
    #convert input strings into rasters
    #print "converting input data to rasters"
    Exp_raster = arcpy.sa.Raster(explanatory)
    Dep_raster = arcpy.sa.Raster(dependent)
    arcpy.CheckInExtension("Spatial")

    #convert rasters to numpy array
    #print "converting rasters to numpy arrays"
    Exp_array = arcpy.RasterToNumPyArray(Exp_raster,nodata_to_value=0)
    Dep_array = arcpy.RasterToNumPyArray(Dep_raster,nodata_to_value=0)

    #print "rshape arrays"
    #reshape arrays from 2D to 1D
    Exp_array1D = np.reshape(Exp_array,-1)
    Dep_array1D = np.reshape(Dep_array,-1)

    #print "getting coefficients"
    #get coefficients
    model_coeffs = np.polyfit(Exp_array1D, Dep_array1D, 1)

    #print"polyfit 1d"
    #polyfit 1D function
    PolyFit1D = np.poly1d(model_coeffs)
    
    fitted_predicted_list = [] #defining a list to convert to an array
    for x in Exp_array1D:
        fitted_predicted_list.append(PolyFit1D(x))

    fitted_predicted_array = np.array(fitted_predicted_list) #converting the fitted prediction to an array

    #print the model function
    print "{dep_name} = {coeff1:.3f} * {exp_name} + {coeff2:.3f}".format(dep_name=dependent,coeff1=model_coeffs[0],exp_name=explanatory,coeff2=model_coeffs[1])
    #generate and print RMSE R_Squared
    print "RMSE = {rmse:.2f}".format(rmse=rmse(Dep_array1D,fitted_predicted_array))

    #generate and print R_Squared
    print "R^2 = {rsquared:.2f}".format(rsquared=r_squared(Dep_array1D,fitted_predicted_array))
    return model_coeffs

def plot_regression(workspace,explanatory,dependent,model_coeffs,samples):
    #print "starting plotting regression"
    arcpy.CheckOutExtension("Spatial")
    arcpy.env.workspace = workspace #Get the workspace path 
    arcpy.env.overwriteOutput = True #setup overwrite protection status
    
    #convert input strings into rasters
    #print "converting input data to rasters"
    Exp_raster = arcpy.sa.Raster(explanatory)
    Dep_raster = arcpy.sa.Raster(dependent)
    outGDB = workspace
    outName = "RandomPoints"
    conFC = Exp_raster
    numField = samples
    #print "generating random points"
    RandomPoints = arcpy.CreateRandomPoints_management(outGDB, outName, "", conFC, numField)
    Exp_rastrer_Extract2Points = arcpy.sa.ExtractValuesToPoints(RandomPoints,  Exp_raster, "Exp_raster_FCPnts")
    Dep_rastrer_Extract2Points = arcpy.sa.ExtractValuesToPoints(RandomPoints,  Dep_raster, "Dep_raster_FCPnts")
    arcpy.CheckInExtension("Spatial")

    Exp_numpy_array = arcpy.da.FeatureClassToNumPyArray(Exp_rastrer_Extract2Points,"RASTERVALU")
    Dep_numpy_array = arcpy.da.FeatureClassToNumPyArray(Dep_rastrer_Extract2Points,"RASTERVALU")
    X = Exp_numpy_array
    X_sorted = np.sort(X)
    #print X[0][0]
    #print X[-1][0]
    Y = Dep_numpy_array
    plt.scatter(X, Y)
    #source: https://www.kite.com/python/answers/how-to-plot-a-polynomial-fit-from-an-array-of-points-using-numpy-and-matplotlib-in-python
    x_predict = np.linspace(X_sorted[0][0],X_sorted[-1][0]) #/samples #not workiing frome kite
    #x_predict = np.array(range(35)) #/ this gives me a line 35 units length
    #val_range = np.amax(X,axis=1)
    #x_predict = np.array(range(val_range)) #/ 
    predict = np.poly1d(model_coeffs)
    y_predict = predict(x_predict)
    plt.plot(x_predict,y_predict, c= 'r')
    plt.show()
    
try:
    # Test Input
    n_samples = 5000
    plot_darts(n_samples)
    print "***Part II***"
    y_predicted = numpy.array([1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9])
    y_observed = numpy.array([1.9, 2.8, 3.7, 4.6, 5.5, 6.4, 7.3, 8.2, 9.1])
    model_rmse = rmse(y_predicted,y_observed)
    print "RMSE:",model_rmse
    model_r_2 = r_squared(y_predicted,y_observed)
    print "R^2:",model_r_2
    #y_empty = numpy.array([])
    #y_error = numpy.array([42])
    #model_rmse = rmse(y_predicted,y_empty)
    #model_r_2 = r_squared(y_error,y_observed)
    print "***Part III***"
    workspace = r"C:\Users\gherm\Desktop\geog656\lab7\biomass_lidar.gdb"
    biomassRaster = "biomass_mgha"
    lidarRaster1 = "lidar_med_z"
    lidarRaster2 = "lidar_max_z"
    #model1 = raster_regression(workspace,lidarRaster1,biomassRaster)
    model2 = raster_regression(workspace,lidarRaster2,biomassRaster)
    #plot_regression(workspace,lidarRaster1,biomassRaster,model1,1000)
    plot_regression(workspace,lidarRaster2,biomassRaster,model2,1000)

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
