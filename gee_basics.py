#Genertate imagery area coordinate set using geojson.io
area = ee.Geometry.Polygon ([
          [
            [
              38.719940185546875,
              15.275574270229807
            ],
            [
              38.717193603515625,
              15.257854691372964
            ],
            [
              38.72028350830078,
              15.211975569898625
            ],
            [
              38.82396697998047,
              15.213135093253888
            ],
            [
              38.8231086730957,
              15.273587102218679
            ],
            [
              38.719940185546875,
              15.275574270229807
            ]
          ]
        ])

collection = ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA")
import os #import os process controls
import geopandas #modele for handling json file handling support
import json #json functions
import ee # Import the Google Earth Engine module 
#ee.Authenticate() # This only needs to be done once!
#ee.Initialize() # Initialize the Earth Engine module/this code runs inside functions now and only needed if code is run in the body of this script
#print(ee.Image('USGS/SRTMGL1_003').getInfo()) # Print metadata

def convertBit(image): #function to rescale landsat images to 8bit streatching at 512bits
    return image.multiply(512).uint8()

print("Images (Entire Collection):",collection.size().getInfo())

collection_first = collection.sort('system:time_start', True).limit(1);
image_first = ee.Image(collection_first.first())
print("First Image Date:",image_first.get('DATE_ACQUIRED').getInfo())
collection_last = collection.sort('system:time_start', False).limit(1);
image_last = ee.Image(collection_last.first())
print("Last Image Date:",image_last.get('DATE_ACQUIRED').getInfo())


#Select GEE Data Source
collection = ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA")
#Set Collection Area of Interest and print selectio info
collection_AOI = collection.filterBounds(area)
print("Images (After Area Filter): ",collection_AOI.size().getInfo())

#Set Collection Time Period and print selection info
collection_date = collection_AOI.filterDate('2019-01-01', '2019-12-31')
print("Images (After Date Filter) :",collection_date.size().getInfo())

#Select least cloudy image from the date and area filters and print date of the image
least_cloudy = ee.Image(collection_date.sort('CLOUD_COVER').first())
print("Selected Image Date: ",least_cloudy.get('DATE_ACQUIRED').getInfo())

#selection RGB Bands for diplay
image_rgb = least_cloudy.select(['B4', 'B3', 'B2']) # Select RGB Bands
image_out = image_rgb.multiply(512).uint8() # Convert to 8-bit Image

task = ee.batch.Export.image.toDrive(image_out, folder="GEOG656_GEE", description='EIT_Feb82019_L8_RGB720', dimensions = 720, region=area)
task.start() # Sends the process to the GEE cloud
print('RGB Image Task Status:',task.status()['state'])

print("Satellite ID: ",least_cloudy.get('SPACECRAFT_ID').getInfo())
path = least_cloudy.get('WRS_PATH').getInfo()
row = least_cloudy.get('WRS_ROW').getInfo()
print(f"Worldwide Reference System (WRS) Path/Row: {path}/{row}")
print("Selected Image ID: ",least_cloudy.get('LANDSAT_SCENE_ID').getInfo())
print("Image Date: ",least_cloudy.get('DATE_ACQUIRED').getInfo())
print("Cloud Cover (%): {:.3f}".format(least_cloudy.get('CLOUD_COVER').getInfo()))
numberOfBands = len(least_cloudy.bandNames().getInfo())
print("Number of Bands: ",numberOfBands)
listOfBands = least_cloudy.bandNames().getInfo()
print("List of Bands Names: ",listOfBands)
b1scale = least_cloudy.select('B1').projection().nominalScale().getInfo();
print('Image Resolution (m): ', b1scale); 
