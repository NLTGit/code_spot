# Purpose: Land suitability analysis aims to evaluate the land's capability for specific uses based on certain conditions. When 
#you analyze land suitability for housing, you may consider the slope, aspect, and current land use type as your criteria of 
#evaluation (i.e. how suitable is an area of land).
import arcpy  #ESRI Arcpy module for geoprocessing
import os #module for os and  file and directory operations
import traceback #debugging support

#Error Handling to prevent check for licensing and parameter input errors
class LicenseError(Exception):
    pass
class WeightCheckError(Exception):
    pass
class UnitsError(Exception):
    pass

try:
    if arcpy.CheckExtension("Spatial") == "Available": 
        #Check for availability of Spaital Analyst Exentnsion and procedd accordngly
        arcpy.CheckOutExtension("Spatial")
    else:
        # raise a custom exception and exit program
        raise LicenseError

    arcpy.env.workspace = arcpy.GetParameterAsText(0) #Get the workspace path 
    arcpy.env.overwriteOutput = True #setup overwrite protection status

    #INPUT PARAMETERS
    #Need to create an arcgis toolbox to source  the input parameters.
    #Get the rest of the parameters as direct Parameter Object Extracts from the toolbox
    #https://desktop.arcgis.com/en/arcmap/10.3/analyze/arcpy-functions/getparameter.htm
    inputDEM = arcpy.GetParameter(1) #returns as a raster dataset directly instead asText() which is a path to the raster data set
    inputLandUse = arcpy.GetParameter(2) #get input landyuse feature class
    W1 = arcpy.GetParameterAsText(3) #suitability weight parameter input 1
    W2 = arcpy.GetParameterAsText(4) #suitablity weight parameter input 2
    W1 = float(W1) #convert to float from string
    W2 = float(W2) #convert to float from string
    if (W1 + W2) != 1.0 or W1 < 0 or W2 < 0: # making sure the weights 0 t0 1 and equal to 1
        raise WeightCheckError #exit program if weights don't equal to 1 or aren't between 0 and 1


    AreaCalcUnits = arcpy.GetParameterAsText(5) # get the units string value directly
    if AreaCalcUnits.lower() not in ['acres','hectares']: #check if units are in hecteras or acers, else exit program
        raise UnitsError

    #OUTPUT PARAMETERS
    finalSuitabilityRaster = arcpy.GetParameterAsText(6) #get the string to name for the output final suitability raster
    outputTextFile = arcpy.GetParameterAsText(7) #get the output text file to store the suitablity result matrix
    arcpy.AddMessage('Starting Suitability Model...') #notify user that the suitabliity model program has started

    #CALCULATE SLOPE
    outSlope = arcpy.sa.Slope(inputDEM,"DEGREE") #generate slope from input DEM using degree units
    outSlope.save(arcpy.GetParameterAsText(0) + "\\outSlope") #save slope raster
    arcpy.AddMessage("Slope Raster Created!") #message back status of slope creation

    #RECLASSIFY THE SLOPE RASTER
    myRemapRange = arcpy.sa.RemapRange([[0, 3, 5], [3, 6, 4], [6, 9, 3],[9, 15, 2], [15,30, 1]])   
    outSlopeReclass = arcpy.sa.Reclassify(outSlope,"Value",myRemapRange)
    outSlopeReclass.save(arcpy.GetParameterAsText(0) + "\\outSlopeReclass")
    arcpy.AddMessage("Slope Raster Reclassified!")

    #•GENERATE & Reclassify the aspect raster based on the table above
    outAspect = arcpy.sa.Aspect(inputDEM)
    outAspect.save(arcpy.GetParameterAsText(0) + "\\outAspect")
    arcpy.AddMessage("Aspect Raster Created!")
    #generating aspect directional value variables for insertion into reclassifier
    Flat = [-1,0,5]
    NorthEast = [0,45,1]
    East = [45,135,3]
    South = [135,225,5]
    West = [225,315,3]
    NorthWest = [315,360,1]
    myRemapRange = arcpy.sa.RemapRange([Flat,NorthEast,East,South,West,NorthWest]) 
    outAspectReclass = arcpy.sa.Reclassify(outAspect,"Value",myRemapRange)
    outAspectReclass.save(arcpy.GetParameterAsText(0) + "\\outAspectReclass")
    arcpy.AddMessage("Aspect Raster Reclassified!")
 
    #RECLASSIFY LANDUSE
    #using raster using provided remap ranges
    #generate remap values
    remapValue = arcpy.sa.RemapValue([[21,1],[31, 1],[52,1],[71,1]])
    #RECLASSIFY VALUES TO TABLE OR 'NO DATA' FIRST, THAN TO 0]
    outLandUseReclassNoData = arcpy.sa.Reclassify(inputLandUse,"Value",remapValue,"NODATA")
    outLandUseReclassNoData.save(arcpy.GetParameterAsText(0) + "\\outLandUseReclassNoData")
    #RECLASSIFY VALUES FROM 1 to 1 and 'NODATA' TO 0
    remapValue = arcpy.sa.RemapValue([[1,1],['NODATA',0]])
    outLandUseReclass = arcpy.sa.Reclassify(outLandUseReclassNoData,"Value",remapValue)
    outLandUseReclass.save(arcpy.GetParameterAsText(0) + "\\outLandUseReclass")
    arcpy.AddMessage("Land Use Raster Reclassified!")  

    #•Calculate the final output suitability raster based on the model above
    SuitabilityRaster = arcpy.sa.Int((W1*outSlopeReclass) + (W2*outAspectReclass))*outLandUseReclass
    SuitabilityRaster.save(finalSuitabilityRaster)
    arcpy.AddMessage("Output Raster '"+finalSuitabilityRaster+"' Saved!") 
    #Check in/return the Sptial Analyst Extension
    arcpy.CheckInExtension("Spatial")

    #get raster cell sizes
    get_cell_sizeXY = arcpy.GetRasterProperties_management(finalSuitabilityRaster,"CELLSIZEX")
    getcellsizeX = get_cell_sizeXY.getOutput(0)
    get_cell_sizeXY = arcpy.GetRasterProperties_management(finalSuitabilityRaster,"CELLSIZEY")
    getcellsizeY = get_cell_sizeXY.getOutput(0)

    searchCurs = arcpy.SearchCursor(finalSuitabilityRaster) #create a search cursor for FinalSuitabailityRaster
    SuitabilityCatsArea = 0
    #write out the header to the output text file
    #using https://docs.python.org/2/reference/simple_stmts.html#the-print-statement
    f = open(outputTextFile, 'w')
    if AreaCalcUnits.lower() == "hectares":
        print >>f,"Suitability Class, Pixel Count, Total Area (hectares)"
    else:
        print >>f,"Suitability Class, Pixel Count, Total Area (acres)"
    for row in searchCurs:  #iterate and load all the rows for processing
        AreaInSqM = int(getcellsizeX) * int(getcellsizeY) * int(row.getValue('Count')) 
        if AreaCalcUnits.lower() == 'hectares':
            SuitabilityCatsArea =  AreaInSqM * 0.000247105 #area in hectares
        else:
            SuitabilityCatsArea = AreaInSqM * 0.0001 #area in acres
        SuitabilityCatsArea = round(SuitabilityCatsArea,3)  
        arcpy.AddMessage('Stuibility Class {classnum} - Area = {area:.3f} {units}'.format(classnum=row.getValue('Value'),area=SuitabilityCatsArea,units=AreaCalcUnits))
        #f.write(str(row.getValue('Value')) + "," + str(int(row.getValue('Count'))) + "," + str(SuitabilityCatsArea) + "\n")
        print >>f,str(row.getValue('Value')) + "," + str(int(row.getValue('Count'))) + "," + str(SuitabilityCatsArea)
    row = searchCurs.next() #move to next search curser row
    f.close()

except LicenseError:
    arcpy.AddError("Spatial Analysis extension is unavailable")
except WeightCheckError:
    arcpy.AddError("The Weight Values need to be within 0 to 1 AND also add up to 1")
except UnitsError:
    arcpy.AddError("The Area Units need to be in hectares or acres")

except Exception as e:
    arcpy.AddError(traceback.format_exc()) #error unsuppression for debugging
    arcpy.AddError(e) # Adds errors to ArcGIS custom tool
    print "Error: " + str(e) # Prints Python-related errors
    print arcpy.GetMessages() # Prints ArcPy-related errors

