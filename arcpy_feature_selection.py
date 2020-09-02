# Stand-alone Script using Hard-coded Values ("SelectLayerByAttribute") and
# Stand-alone Script using User-defined Input ("SelectLayerByLocation")
#code for Part I (step 1 and step 2 are commented out)

# Import modules
import arcpy  #ESRI Arcpy module for geoprocessing

try:
    #PART I CODE
    """
    #Code for Step 1 # create a new polygon feature class
    #(shapefile) containing a subset of parcels from an existing layer called "City of Austin Owned Parcels".
    #Set the arcpy workspace and overwite setting
    arcpy.env.workspace = r"yourpath"  # Your workspace path
    arcpy.env.overwriteOutput = True
    arcpy.MakeFeatureLayer_management("yourshapefile1.shp", "lyr") #make a feature layer

    #Selecting Parcels in the "Austin Housing Authority"
    # query = "\"FIELDNAME\" = \'FIELDVALUE\'"  #setup a query string
    # arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", query) #make a selection from the layer using query string
    arcpy.CopyFeatures_management("lyr", "yourNewhapefile") #copy the selected features of the feature layer into a new "yourNewshapefile "feature class
    print "A new feature class 'yourNewShapefile' has been created!"
    
#Exception handling and messagin back to user in
except Exception as e:
    # This block of code will run if any error occurs!
    print "Error: " + str(e)  # Prints Python-related errors in stand-alone moode
    print arcpy.GetMessages()  # Prints ArcPy-related errors and send them to arcgis process dialog box
    arcpy.AddError(e)  # Adds errors to ArcGIS custom tool and send them back to arcgis process dialog box
    """
    """
    #Code for Step2
    #Selecting parcels with a large area
    #Set the arcpy workspace and overwite setting
    arcpy.env.workspace = r"yourworkspacepath"  # Your workspace path
    arcpy.env.overwriteOutput = True
    arcpy.MakeFeatureLayer_management("yourshapefile.shp", "lyr") #make a feature layer
    query = "\"AreaValueField\" > 10000000" #setup a query string
    arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", query) # make a selection from layer using query string
    print query # The printed query should look just like what you typed into ArcMap!

    arcpy.CopyFeatures_management("lyr", "largefeatures") #copy the feature layer into a new feature class
    print "A new feature class 'large_parcels' has been created!"
    
#Exception handling and messagin back to user in
except Exception as e:
    # This block of code will run if any error occurs!
    print "Error: " + str(e)  # Prints Python-related errors in stand-alone moode
    print arcpy.GetMessages()  # Prints ArcPy-related errors and send them to arcgis process dialog box
    arcpy.AddError(e)  # Adds errors to ArcGIS custom tool and send them back to arcgis process dialog box
    """


    #CODE BLOCK FOR PART II
    #Stand-alone Script using User-defined Input ("SelectLayerByLocation")
    #raw input for the workspace and feature classes for the input, selection, and output file names
    work = raw_input("What is the workspace location? ")
    inFC = raw_input("What is the input feature class name? ")
    selectFC = raw_input("What is the select feature class name? ")
    outFC = raw_input("What is the output feature class name? ")

    #setup arcpy workspace and overwrite setting
    arcpy.env.workspace = work
    arcpy.env.overwriteOutput = True
    print("Arcpy Input Aurguments and Workspace Settings Section Complete")

    #create a feature layer for selection from the input feature class
    print("Make a feature layer from input feature class")
    arcpy.MakeFeatureLayer_management(inFC, 'inFC_lyr')

    #select the features from the feature layer that intersect with the selection feature class
    arcpy.SelectLayerByLocation_management('inFC_lyr','INTERSECT',selectFC)

    # If features matched criteria write them to a new feature class
    #based on example from https://desktop.arcgis.com/en/arcmap/10.3/tools/data-management-toolbox/select-layer-by-location.htm
    matchcount = int(arcpy.GetCount_management('inFC_lyr')[0]) #find out how many features matched the selection
    if matchcount == 0: #check if no features were selected based on the query criteria
        print('no features matched spatial and attribute criteria') # let the user know no feauters met the criteria
    else: #if more than 1 feature have met the selection criteria, write the selected features in the layer to the output feature class
        arcpy.CopyFeatures_management('inFC_Lyr', outFC) #copy selections in the layer to output feature class
        print("A new feature class called {outFCV} has been created!!".format(outFCV=outFC)) #inform user of the new feature class that has been created
#Exception handling and messagin back to user in
except Exception as e:
    # This block of code will run if any error occurs!
    print "Error: " + str(e)  # Prints Python-related errors in stand-alone moode
    print arcpy.GetMessages()  # Prints ArcPy-related errors and send them
    arcpy.AddError(e)  # prints arcpy errors
