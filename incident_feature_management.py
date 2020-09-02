#arcp code to manage wilfire incidents

class overwriteError(Exception):
    pass

class existsError(Exception):
    pass

import arcpy  #ESRI Arcpy module for geoprocessing
import os #module for os and  file and directory operations

try:
    work = raw_input("Enter the full path of WildlandFires.gdb (or press enter if its YourWorkSpacePath\WildlandFires.gdb ): ") or r'your YourWorkSpacePath\WildlandFires.gdb'
    if not os.path.exists(work):
        raise existsError
        #exit the program down to exception block
    inFile = raw_input("Enter the full path of wildfire text file (or press enter if its YourWorkSpacePath\NorthAmericaWildfires_2007275.txt ): ") or rYourWorkSpacePath\NorthAmericaWildfires_2007275.txt'
    if not os.path.isfile(inFile):
        raise existsError
        #exit the program down to exception block
  
    newOutputFeatureClass = raw_input("Enter the name of the new output feature class(or press enter if its 'newFireIncidents' ): ") or 'newFireIncidents'

    arcpy.env.workspace = work # Set the workspace to the geodatabase
    arcpy.env.overwriteOutput = True #change overwrite protection status
    if arcpy.Exists(newOutputFeatureClass):
        overwriteQ = raw_input("WARNING! This file exists! Overwrite? (Y or N):")     
        if overwriteQ.lower() == "n":
           raise overwriteError
            #exit the program down to exception block

    f = open(inFile, 'r')
    lstFires = f.readlines()
    f.close()
    
    ConfVariable = lstFires[0].split(',')[2] #grab variable confidence field name
    ConfVariable = ConfVariable.strip() #stripping new line value
    arcpy.CreateFeatureclass_management(work,newOutputFeatureClass,'POINT')
    arcpy.AddField_management(newOutputFeatureClass,ConfVariable,'LONG')
    fields = ["SHAPE@", ConfVariable]
    cur = arcpy.da.InsertCursor(newOutputFeatureClass, fields)

    cntr = 0
    minThreshold = -1
    minThreshold = int(raw_input("Specify the minimum confidence threshold (0-100): "))
    while not 0 <= minThreshold <= 100:
        minThreshold = int(raw_input("Warning...Threshold must be between 0 and 100...Re-enter: "))

    #search cursor to access the polygon object and name
    searchCurs = arcpy.da.SearchCursor('NationalParks',['SHAPE@','Name']) 
    #need code to create polygon variable for the first row in searchcurser
    row = searchCurs.next()
    polygon = row[0]
    name = row[1]
    print name
    inNationalPark = 0
    for fire in lstFires:
        if 'Latitude' in fire: # Skip the header
            continue
        listValues = fire.split(',')
        if int(listValues[2]) > minThreshold:
            pnt = arcpy.Point() # Create a new Point object   
            latitude = listValues[0]
            longitude = listValues[1]
            confid = listValues[2]
            pnt.X = longitude
            pnt.Y = latitude
            #if the point is in the polygon, insert it into new feature class and increment record count and number in polygon count
            row = [pnt, confid]
            cur.insertRow(row)
            cntr = cntr + 1
            print "Record # " + str(cntr) + " written to feature class"
            if pnt.within(polygon):
                inNationalPark +=1
    del cur, searchCurs #delete both cursors
    print 'The were {num} fires within {name}'.format(num = inNationalPark, name = name) 

    #Analyze Clustering of Fire Points
    nn_output = arcpy.AverageNearestNeighbor_stats(newOutputFeatureClass, "EUCLIDEAN_DISTANCE", "NO_REPORT",'#') 
    zscoreval = round(float(nn_output[1]),2)
    if nn_output[1] < -1.65:
        print "The fire incidents are *signifiantly clustered* (z-score= ({score})".format(score=zscoreval)
    elif nn_output[1] > 1.65:
        print "The fire incidents are *significantly disperesed* (z-score= {score})".format(score=zscoreval)
    else:
        print "The fire incidents are *sptially random* (z-score= {score})".format(score=zscoreval)

except overwriteError:
    print "Program Ended... No Feature Class Created"
except existsError:
    print "Program Ended... Path Does Not Exist"
except Exception as e:
    print "Error: " + str(e) # Prints Python-related errors
    print arcpy.GetMessages() # Prints ArcPy-related errors
    arcpy.AddError(e) # Adds errors to ArcGIS custom tool
