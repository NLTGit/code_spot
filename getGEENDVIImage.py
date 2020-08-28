#get GEE NDVI Image for a given year given an AOI
import os #import os process controls
import geopandas #modele for handling json file handling support
import json #json functions
import ee # Import the Google Earth Engine module 
#ee.Authenticate() # This only needs to be done once!
#ee.Initialize() # Initialize the Earth Engine module/this code runs inside functions now and only needed if code is run in the body of this script
#print(ee.Image('USGS/SRTMGL1_003').getInfo()) # Print metadata

def convertBit(image): #function to rescale landsat images to 8bit streatching at 512bits
    return image.multiply(512).uint8()
def getNDVIImage(workingdir,geojsonfilename,year):
    #function to export to google drive an ndvi image for a given area
    class existsError(Exception):
        pass
    class ExtensionError(Exception):
        pass
    class ValidYearError(Exception):
        pass
    
    try:
        if not os.path.exists(workingdir):
            raise existsError #exit the program down to exception block        
        outputfilenamesuffix = geojsonfilename.partition(".")[2] #create a list of the parts of the file name and access using index
        outputfilenamesuffix = outputfilenamesuffix.lower()
        if outputfilenamesuffix != "json":
            raise ExtensionError #exit the program down to exception block       
        if year not in range(2013,2021):
            raise ValidYearError  #exit the program down to exception block
        
        #import json
        fullpath = workingdir+ '\\' + geojsonfilename
        workingpath = fullpath
        json_geo_df = geopandas.read_file(workingpath)
        json_geo_js = json_geo_df.to_json()
        json_geo_js_dict = json.loads(json_geo_js)
        for feature in json_geo_js_dict['features']:
            json_geo = feature['geometry']['coordinates']
            
        ee.Initialize() # Initialize the Earth Engine module 
        area = ee.Geometry.Polygon (json_geo)
    
        #Select GEE Data Source
        collection = ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA")
        #Set Collection Area of Interest and print selection info
        collection_AOI = collection.filterBounds(area)
        #print("Images (After Area Filter): ",collection_AOI.size().getInfo())
        
        #Set Collection Time Period and print selection info
        year_start_string = str(year) + '-01-01'
        year_end_string = str(year) + '-12-31'
        collection_date = collection_AOI.filterDate(year_start_string, year_end_string)
        #print("Images Collection Size  (After Date Filter) :",collection_date.size().getInfo())
        
        #switch to calling function ImageCollectoin
        #Select least cloudy image from the date and area filters and print date of the image
        least_cloudy = ee.Image(collection_date.sort('CLOUD_COVER').first())
        print("Selected Image Date: ",least_cloudy.get('DATE_ACQUIRED').getInfo())
        selected_image_date = least_cloudy.get('DATE_ACQUIRED').getInfo()
        
        #generatge NDVI on least_cloudy image
        ndvi_image = least_cloudy.normalizedDifference(['B5', 'B4'])
        
        # #selection RGB Bands for diplay and rescale bit range
        # image_rgb = least_cloudy.select(['B4', 'B3', 'B2']) # Select RGB Bands
        
        #rescale NDVI Image
        image_out = ndvi_image.multiply(512).uint8() # Convert to 8-bit Image
        
        
        task = ee.batch.Export.image.toDrive(image_out, folder="Google Drive Folder Name Goes Here", description='NDVIImage', dimensions = 720, region=area)
        task.start() # Sends the process to the GEE cloud
        #print('RGB Image Task Status:',task.status()['state'])
    
       # #print("Image Date: ",least_cloudy.get('DATE_ACQUIRED').getInfo())
       #  print("Selected Image Cloud Cover (%): {:.3f}".format(least_cloudy.get('CLOUD_COVER').getInfo()))
        
        #print (geojsonfilename.partition(".")[0])
        outputfilenameprefix = geojsonfilename.partition(".")[0]
        outputfilenameprefix = outputfilenameprefix +'_NDVIImage_'+ str(selected_image_date)
        task = ee.batch.Export.image.toDrive(image_out, folder="MY_GEE_OUTPUT", description=outputfilenameprefix, dimensions = 720, region=area)
        task.start() # Sends the process to the GEE cloud
        print(f"Selected NDVI Image '{outputfilenameprefix}.tif' sent to Google Drive")
        
    except existsError:
        print ("Error: Input File Does Not Exist")
    except ExtensionError:
        print ("Error: Input File must be JSON File")
    except ValidYearError:
        print ("Error: Input Year is Not Valid")
    except Exception as e:
        print ("Error: " + str(e)) # Prints Python-related errors

    return #end function / no return values

print("Generate an NDVI image")
#Part V - Creating Time Series getVideo()
work = r"yourfilederand"
jsonfile = "YourJSONFile.json"
year = 2019
getNDVIImage(work,jsonfile,year)
