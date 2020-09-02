import arcpy
arcpy.env.workspace = r"c:\test"
arcpy.env.overwriteOutput = True
infile = "lines.txt" # Input Text File with Point Coordinates of each Line Feature
outfile = "lines.shp" # Output Shapefile Name
arcpy.CreateFeatureclass_management(arcpy.env.workspace,outfile,"Polyline") # Create new Line FC
fields = ["SHAPE@", "ID"]
cur = arcpy.da.InsertCursor(outfile,fields) # Create Insert Cursor to insert lines into new FC
ary, pnt = arcpy.Array(), arcpy.Point() # Create empty Array/Point objects for new lines/points
rfile = open(infile,'r') # Open the text file that contains the line points in "read" mode
lines = rfile.readlines() # Read the lines from the input text file
rfile.close()
ID = -1 # ID of the current line we are creating; initialize to -1
for line in lines:
    pnt.ID, pnt.X, pnt.Y = line.split(";") # Split the line into coordinates
    print pnt.ID, pnt.X, pnt.Y
    if ID == -1: # If ID = -1, then we are starting a new line
        pass # Do Nothing
    elif ID != pnt.ID: # If ID is not the same, we have finished a line; add it to the FC
        feat = [arcpy.Polyline(ary), ID] # Define the Shape and ID fields as the Line Array and Line ID
        cur.insertRow(feat) # Insert the Row/Feature into the FC
        ary.removeAll() # Create an empty Array for a new line
    ary.add(pnt) # Add the new Point to the list of coordinates for the line
    ID = pnt.ID # Set the current line ID
# Once loop is over, add the last line to the FC
feat = [arcpy.Polyline(ary), ID] # Define the Shape and ID fields as the Line Array and Line ID
cur.insertRow(feat) # Add the last line to the FC
del feat, cur
