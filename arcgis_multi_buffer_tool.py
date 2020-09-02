
#Toolbox Code for generating multiple buffers based on starting and ending buffer distances and buffer intervals against a selection by attribute and select by distance for each intenterval

# Import modules
import arcpy #ESRI Arcpy module for geoprocessing

try:
    # generate variables from toolbox inputs for assignment to arcpy parameter
    work = arcpy.GetParameterAsText(0) #assign work the directory location from toolbox input
    inFC = arcpy.GetParameterAsText(1) #assing input feature class from from toolbox input
    SelectByAttibute = arcpy.GetParameterAsText(2) #input argument for the selection attribute
    selectFC = arcpy.GetParameterAsText(3) #the selection feature class for the intersect
    BufferStart = int(arcpy.GetParameterAsText(4)) #the buffer start distance
    BufferEnd = int(arcpy.GetParameterAsText(5)) #the buffer end distance
    BufferInterval = int(arcpy.GetParameterAsText(6)) #the buffer interval
    BufferUnits = arcpy.GetParameterAsText(7) #buffering units for buffer analysis toolbox, generated from toolbox input
    outFC = arcpy.GetParameterAsText(8) #assing output base file name for the feature class that will be generated for each buffer interval from from toolbox input


    # setup arcpy and overwrite protection status
    arcpy.env.workspace = work
    arcpy.env.overwriteOutput = True

    # create a feature layer from the input feature class
    arcpy.MakeFeatureLayer_management(inFC, 'inFC_lyr')

    #Strip the file name at the period from the file extension name for use as a string in the base file name for the buffer zone outputs by interval
    outFCsplit = outFC.split('.')

    #Assess the number of rings needed based on Buffer Start, End and Interval Values
    for num in range(BufferStart,BufferEnd+1,BufferInterval):
       #set the outFC based buffer interval value and buffer name at the range in buffers being created
       TempoutFC = outFCsplit[0] + str(num)  + '.shp' #generate the output feature class name for each buffer zone using string method name concatination at each buffer interval assign to "num"

       # generate the query string for the field selection for features that are owened by the SelectByAttribute argument in the toolbox
       query = "\"PY_FULL_OW\" = '{GrabFromDialog}'".format(GrabFromDialog=SelectByAttibute) #GrabFromDialog is a placeholder variable for string insertion
       # process SelectbyAttribute on the input feature layer using the query string
       arcpy.SelectLayerByAttribute_management("inFC_lyr", "NEW_SELECTION", query)

       Distance = str(num) + ' ' + BufferUnits
       # select feature in the input feature layer that intersect the selection feature class by a user defined distance upto
       arcpy.SelectLayerByLocation_management('inFC_lyr', 'INTERSECT', selectFC, Distance, 'SUBSET_SELECTION')
       # If features matched criteria write them to a new feature class
       matchcount = int(arcpy.GetCount_management('inFC_lyr')[0])
       if matchcount == 0:  # #check to see if actual selection features exist at the specified buffer interval (Distance)
           arcpy.AddMessage("no features matched spatial and attribute criteria at bufer interval: " + Distance)
       else:
           #generate the new feature class for the specified buffer interval in the loop
           filenameforprint = TempoutFC.split('\\')[-1]  # split the output filename from the fullpath and use it for messaging
           arcpy.CopyFeatures_management('inFC_Lyr', TempoutFC) #create the new feature class from the selection layer and write it out to the feature class specified at the interval in the loop
           arcpy.AddMessage("A new feature class '{outFCV}' has been created!".format(outFCV=filenameforprint)) #print a message to the arcgis toolbox dialog box specifiying the buffer that was reated
           arcpy.AddWarning("Buffer= {Dist},There are {matchcount_v} features in the new feature class.".format(Dist=Distance, matchcount_v=matchcount))

except Exception as e:
    # This block of code will run if any error occurs!
    print "Error: " + str(e)  # Prints Python-related errors
    print arcpy.GetMessages()  # Prints ArcPy-related errors
    arcpy.AddError(e)  # Adds errors to ArcGIS custom tool
