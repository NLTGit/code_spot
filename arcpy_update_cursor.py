#Stand-alone Script that uses the Update Cursor Object
    work = raw_input("Enter the full workspace path: ")
    arcpy.env.workspace = work
    arcpy.AddField_management("Hospitals.shp", "FullAddr", "TEXT", 50)
    updCursor = arcpy.UpdateCursor("Hospitals.shp")
    row = updCursor.next()
    cntr = 1
    while row:
        strAddress = row.getValue("Address")
        strCity = row.getValue("City")
        strState = row.getValue("State")
        strZip = row.getValue("Zipcode")
        strFullAddress = strAddress+","+strCity+","+strState+","+strZip
        row.setValue("FullAddr", strFullAddress)
        updCursor.updateRow(row)
        print "Updated record number: " + str(cntr)
        cntr = cntr + 1
        row = updCursor.next()
    print "Update Complete"
    del row, updCursor # Delete the Row and Cursor and remove locks
