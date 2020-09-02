# Purpose: Develop functions and script to deal with cursor objects and exception 
# handling. Intro scripts and 5 functions created to deal with multi-function 
# geoprocessing as well as script body exception handling and in-functio modular error and exception handling.

import arcpy  #ESRI Arcpy module for geoprocessing
import os #os module for checking file and directory status

#numSchools Function:
"""The function should have three input parameters: (1) a string for the workspace, (2) a string for the shapefile name, and (3) a string for the facility type (e.g. "HIGH SCHOOL"), and one output parameter: (1) an integer for the number of schools of that facility type in the shapefile. """
def numSchools(work,shapefile,sType):
    arcpy.env.workspace = work #setup arcp work space to incoming argmumen
    whereClause = "\"FACILITY\" = '{type}'".format(type=sType)
    searchCurs = arcpy.SearchCursor(shapefile, whereClause)
    count = 0
    for row in searchCurs:
        count +=1
    return count

#schoolsStats Function
"""The function should have two input parameters: (1) a string for the workspace and (2) a string for the shapefile name. There are no output parameters."""
def schoolsStats(work,shapefile):
    arcpy.env.workspace = work #setup arcp work space to incoming argmumen
    searchCurs = arcpy.SearchCursor(shapefile) #create a search cursor for inFC
    row = searchCurs.next() #create row object for FC iteration
    ListofAllRows = [] #create an empty list for row ingestion
    for row in searchCurs:  #iterate and load all the rows into list
        name =  row.getValue("FACILITY") 
        ListofAllRows.append(name)

    UniqueRows=list(set(ListofAllRows)) #aquiring the unique row set using using set casting and back to list casting
    for item in UniqueRows: #get unique rwos
        num = numSchools(work,shapefile,item) #for each unique item get quantitiy
        print item + '\t'  + str(num)  #print unique item name and quantity
    return 

#searchHospitals Function
""""searchHospitals" that prints the names of all hospitals ina 5-digit zip code area based on the shapefile "Hospital.shp". Also print the number of hospitals.
The function should have two input parameters: (1) a string representing the workspace and (2)an integer representing the zip code. The function should have no output parameters."""
def searchHospitals(work,zipcode):
    arcpy.env.workspace = work #setup arcp work space to incoming argmumen
    #generate selection clause using incoming arugment
    whereClause = "\"ZIPCODE\" LIKE '{type}%'".format(type=zipcode) 
    #create a search cursor based on subselection by whereClause
    searchCurs = arcpy.SearchCursor("Hospitals.shp",whereClause)
    cntr = 0
    #iterate through row and get the number of items for the subselection
    for row in searchCurs:
        name =  row.getValue("NAME")
        print name
        cntr +=1
    print "Total {count} hospitals were found in zip-code {zip}.".format(count=cntr,zip=zipcode)
    return 

#selectSchools Function
"""selectSchools" that: (1) selects schools of specifiedfacility type, (2) outputs the results to a new shapefile, and (3) deletes records not verified."""
def selectSchools(work,facilityType,outFC):
    try:
        #https://www.geeksforgeeks.org/python-os-path-isdir-method/  
        if not os.path.isdir(work):
            raise Exception('THE WORKSPACE \'{workspace}\' DOES NOT EXIST'.format(workspace = work))
            #exit the function with an empty string
    except Exception, e:
        print e
        print "ERROR IN FUNCTION 'selectSchools'"
        return ""  #returns an empty string
    # setup arcpy and change overwrite protection status
    arcpy.env.workspace = work #setup arcp work space to incoming argmumen
    arcpy.env.overwriteOutput = True #change overwrite protection status

    inFC = "Schools.shp"
    # create a feature layer from the input feature class
    arcpy.MakeFeatureLayer_management(inFC, 'inFC_lyr')

    whereClause = "\"FACILITY\" = '{type}'".format(type=facilityType)

    # process SelectbyAttribute on the input feature  using the whereClause string
    arcpy.SelectLayerByAttribute_management('inFC_lyr', "NEW_SELECTION", whereClause)
    
    # copy out the selected features to a new feature class
    #first check to see if selection is empty
    #use: https://pro.arcgis.com/en/pro-app/tool-reference/data-management/get-count.htm for eror protection
    #matchcount = int(arcpy.GetCount_management('inFC_lyr')[0]) #count the number of features selected 
    matchcount = arcpy.GetCount_management('inFC_lyr') #count the number of features selected 
    #print arcpy.GetCount_management('inFc_lyr') #testing counter on just the layer without index
    #print arcpy.GetCount_management('inFC_lyr')
    print matchcount
    try:
        if matchcount == 0:  # if there are no features selected, print a statement and raise an exception
            raise Exception('NO FEATURES SELECTED FOR \'{NSF}\''.format(NSF = inFC))
    except Exception, e:
        print e
        print "ERROR IN FUNCTION 'selectSchools'"
        return ""

    #generate the new feature class for the selection set in the layer out to the output feature class
    arcpy.CopyFeatures_management('inFC_lyr', outFC) #create the new feature class from the selection layer and write it out to the feature class outFC

    #select and delete the unverified rows in outFC
    whereClause = "\"VERIFIED\" not in ('y','Y')" #quicker  version sql statement. need lookup
        #"\"VERIFIED\" <> \'y\' AND \"VERIFIED\" <> \'Y\'"
    uCursor = arcpy.UpdateCursor(outFC, whereClause)
    counter = 1
    newRow = uCursor.next() # Get the first row in the table...
    print "The following {records} schools have not been verified and have been deleted".format(records=facilityType)
    while newRow != None: # Loop until row is empty...
        # get the row
        name =  newRow.getValue("NAME")
        print "{counter}) {name}".format(counter=counter,name=name)
        # Delete the row from the feature class
        uCursor.deleteRow(newRow)
        newRow = uCursor.next()
        counter +=1
    del newRow, uCursor #unlock outFC
    return outFC

#countHospitals Function
""""countHospitals" that uses the output shapefile from the"selectSchools" function and counts the number of hospitals within a 3-mi radius of each school."""
def countHospitals(workspace,inFC):
    try:
        #https://www.geeksforgeeks.org/python-os-path-isdir-method/  
        if not os.path.isfile(inFC):
            raise Exception('THE FEATURE CLASS \'{inFC}\' DOES NOT EXIST'.format(inFC = inFC))
            #exit the function if not a real file
    except Exception, e:
        print e
        print "ERROR IN FUNCTION 'selectSchools'"
        return ""  #returns an empty string

    try:  
        # setup arcpy and overwrite protection status
        arcpy.env.workspace = workspace #setup arcp work space to incoming argmumen
        arcpy.env.overwriteOutput = True #set overwrite status

        #hardcoud feature classes for processing. The files do/will exist in workspace from arguments.
        HospitalsFC = "Hospitals.shp"
        SchoolsBuff3mi_Output = "SchoolsBuff3mi_Output.shp"
        outFC_spatialjoin = "outFC_spatialjoin.shp"

        # create a feature layer from the input feature class
        arcpy.MakeFeatureLayer_management(inFC, 'inFC_lyr')

        #make a 3 mile buffer around selected features
        arcpy.Buffer_analysis("inFC_lyr",SchoolsBuff3mi_Output,"3 Miles")

        #perform spatial join on schools buffer selection and hospitals to get count of hospitals within 3 miles of selected schools
        arcpy.SpatialJoin_analysis(SchoolsBuff3mi_Output,HospitalsFC,outFC_spatialjoin,"JOIN_ONE_TO_ONE","KEEP_ALL","","CONTAINS")
        #use resulting spatial joint counts to find schools that do not have hospitals within 3 miles using search cursor row iteration.
        whereClause = "\"Join_Count\" = 0"
        searchCurs = arcpy.SearchCursor(outFC_spatialjoin,whereClause)
        row = searchCurs.next()
        cntr = 1
        for row in searchCurs:
            name =  row.getValue("NAME")
            print name
            cntr +=1
        print "Total {count} schools with no hostpitals within 3mi".format(count=cntr)
        return 
    except Exception,e:
        print e
        print "ERROR IN FUNCTION countHospitals"


try:
    # Test Input
    print "***Testing the numSchools() Function***"
    work = r"YourWorkSpacePath"
    shapefile = "Schools.shp"
    sType = "JUNIOR HIGH"
    print numSchools(work, shapefile, sType)
    sType = "SPECIAL CENTER"
    elemSchools = numSchools(work, shapefile, sType)
    print "There are a total of %d %s." % (elemSchools,sType)
    print "***Testing the schoolStats() Function***"
    schoolsStats(work, shapefile)
    print "***Testing the searchHospitals() Function***"
    zip5 = 78759
    searchHospitals(work,zip5)
    searchHospitals(work,66666)
    print "***Testing the selectSchools() Function***"
    sType = "HIGH SCHOOL"
    outFile = "output.shp"
    result = selectSchools(r"C:\Fake_Dir",sType,outFile)
    print result
    result = selectSchools(work,"TOO COOL FOR SCHOOL",outFile)
    print result
    result = selectSchools(work,sType,outFile)
    print result
    print "***Testing the countHospitals() Function***"
    countHospitals(work, result)
    countHospitals(work, "fake_shapefile.shp")
    
except Exception, e:
    print "Python Error: " + str(e) # Prints Python-related errors
    print "Arcpy Traceback Errors below:"
    print arcpy.GetMessages() # Prints ArcPy-related errors #only throws errors for ArcPy
    arcpy.AddError(e) # Adds errors to ArcGIS custom tool and to console

