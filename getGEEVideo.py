#get GEE Video for a given year given an AOI
import os #import os process controls
import geopandas #modele for handling json file handling support
import json #json functions
import ee # Import the Google Earth Engine module 
#ee.Authenticate() # This only needs to be done once!
#ee.Initialize() # Initialize the Earth Engine module/this code runs inside functions now and only needed if code is run in the body of this script
#print(ee.Image('USGS/SRTMGL1_003').getInfo()) # Print metadata

def convertBit(image): #function to rescale landsat images to 8bit streatching at 512bits
    return image.multiply(512).uint8()

def getVideo(workingdir,geojsonfilename,year):
    #functio to export a video given a geojson area of interest and year
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
        area = ee.Geometry.Polygon (json_geo) #assign ROI to json file input area object
      
        #Select GEE Data Source
        collection = ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA")
        print("Images (All Landsat): ",collection.size().getInfo())
        
        #Set Collection Area of Interest and print selection info
        collection_AOI = collection.filterBounds(area)
        print("Images (After Area Filter): ",collection_AOI.size().getInfo())
        
        #Set Collection Time Period and print selection info
        year_start_string = str(year) + '-01-01'
        year_end_string = str(year) + '-12-31'

        collection_date = collection_AOI.filterDate(year_start_string, year_end_string)
        print("Images (After Date Filter) :",collection_date.size().getInfo())
        
        #select imagery with less than 5% cloud cover
        collection_filt = collection_date.filter(ee.Filter.lt('CLOUD_COVER', 5))
        print("Images (After Cloud Filter) :",collection_filt.size().getInfo())
        
        ## Select bands
        bands = collection_filt.select(['B4', 'B3', 'B2'])
        
        #rescale collection_filt images to 8bit
        collection_output = bands.map(convertBit)
        
        #create prefix for the output video name
        outputfilenameprefix = geojsonfilename.partition(".")[0]
        outputfilenameprefix = outputfilenameprefix +'Movie_'+ str(year)
        print(outputfilenameprefix)
        
        #task = ee.batch.Export.video.toDrive(collection_output,description=outputfilenameprefix, folder="GEOG656_GEE",,dimensions = 720,region=area,framesPerSecond: 12,maxFrames=30)
        task = ee.batch.Export.video.toDrive(collection_output, description='myExportVideoTask', folder="MY_GEE_OUTPUT", fileNamePrefix=outputfilenameprefix, framesPerSecond=12, dimensions=720, region=area, maxFrames=30)
        task.start() # Sends the process to the GEE cloud
        print(f"Time Series Video '{outputfilenameprefix}.mp4' sent to Google Drive")
        print('Time Series Video Task Status:',task.status()['state'])
            
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
work = r"G:\My Drive\Geog656\lab9"
jsonfile = "EIT.json"
year = 2019
getNDVIImage(work,jsonfile,year)
