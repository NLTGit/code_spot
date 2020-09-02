import arcpy  #ESRI Geoprocessing Pythong Module
arcpy.env.overwriteOutput = True #enable feature class overwriting for iterative processing

def myNewBuffer_standalone(work, inFC, outFC, distance,units): #testing with 5 arguments including units
   arcpy.env.workspace = work  # Set the workspace to incoming workspace argument
   arcpy.env.overwriteOutput = True
   distwunits = "{dist} {units}".format(dist=distance, units=units)
   if units == "Feet" or units == "Meters": #check to make sure correct units are provided before processing buffer
       result = arcpy.Buffer_analysis(inFC, outFC, distwunits) #run buffer with explicit unit arguments
       print ('The '+str(distance)+ ' ' + units + ' buffer '+ "'" + outFC + "'" +' has been created.')
       # print buffer completion status message including units and output file name
   else: print("Error! Envalid units!")

# run from arcgistoolsbox paramters
def myNewBuffer(work, inFC, outFC, distance,units): #testing with 5 arguments including units
   arcpy.env.workspace = work  # Set the workspace to incoming workspace argument
   arcpy.env.overwriteOutput = True
   distwunits = "{dist} {units}".format(dist=distance, units=units)
   if units == "Feet" or units == "Meters": #check to make sure correct units are provided before processing buffer
       result = arcpy.Buffer_analysis(inFC, outFC, distwunits) #run buffer with explicit unit arguments
       arcpy.AddWarning ('The '+str(distance)+ ' ' + units + ' buffer '+ "'" + outFC + "'" +' has been created.')
   else: arcpy.AddError("Error! Envalid units!")
   
if __name__ == "__main__":   
    # work = r"your geodb path"  # PATH = Your workspace path
    # inFC, outFC, distance, units = "futrds", "futrds_feet", 2500, "Feet"
    # myNewBuffer_standalone(work, inFC, outFC, distance, units)
    DialogWorkspace = arcpy.GetParameterAsText(0) #input variable from tool dialog for workspace
    DialoginFC = arcpy.GetParameterAsText(1) #input variable from tool dialog for input feature class
    DialogDistance = arcpy.GetParameterAsText(2) #input vriable from tool for buffer distance
    DailogUnits = arcpy.GetParameterAsText(3) #input vriable from tool for distance units
    DialogOutput =arcpy.GetParameterAsText(4) #input variable from tool for output feature class
    # my new buffer running with tool parameter inputs
    myNewBuffer(DialogWorkspace,DialoginFC, DialogOutput, DialogDistance,DailogUnits)
