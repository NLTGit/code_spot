# Purpose: Part III - Create a Custom ArcGIS Tool from a Python Script

# Import modules
import arcpy #ESRI Arcpy module for geoprocessing

try:
    # generate variables from toolbox inputs for assignment to arcpy parameters
    work = arcpy.GetParameterAsText(0) #assign work the directory location from toolbox input
    inFC = arcpy.GetParameterAsText(1) #assing input feature class from from toolbox input
    selectFC = arcpy.GetParameterAsText(2) #assign selection feature class from toolbox input
    outFC = arcpy.GetParameterAsText(3) #assign selection feature class from input toolbox

    # setup arcpy and overwrite protection status
    arcpy.env.workspace = work
    arcpy.env.overwriteOutput = True

    # create a feature layer from the input feature class
    arcpy.MakeFeatureLayer_management(inFC, 'inFC_lyr')
    # select feature in the input feature layer that intersect the selection feature class
    arcpy.SelectLayerByLocation_management('inFC_lyr', 'INTERSECT', selectFC)

    # If features matched criteria write them to a new feature class
    # example from https://desktop.arcgis.com/en/arcmap/10.3/tools/data-management-toolbox/select-layer-by-location.htm
    matchcount = int(arcpy.GetCount_management('inFC_lyr')[0])
    if matchcount == 0:  # check for empty selection to prevent creating a new empty feature class
        print('no features matched spatial and attribute criteria')
    else:
        filenameforprint = outFC.split('\\')[-1]  # split the output filename from the fullpath and use it for messaging
        arcpy.CopyFeatures_management('inFC_Lyr', outFC)
        arcpy.AddMessage("A new feature class '{outFCV}' has been created!".format(outFCV=filenameforprint))
        arcpy.AddWarning("There are {matchcount_v} features in the new featuer class.".format(matchcount_v=matchcount))

except Exception as e:
    # This block of code will run if any error occurs!
    print "Error: " + str(e)  # Prints Python-related errors
    print arcpy.GetMessages()  # Prints ArcPy-related errors
    arcpy.AddError(e)  # Adds errors to ArcGIS custom tool
