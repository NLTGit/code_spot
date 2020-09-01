# Purpose: Geospatial Mapping with GeoPandas
#Using verbose variable and function naming style to reduce comment volume

import numpy, pandas, geopandas
#import modules to run numerical, dataframe and geodataframe processes

#UTM zones and EPSG codes dictionary with key string and integer values
utm_epsg = {
  "UTM10N": 26910,
  "UTM11N": 26911,
  "UTM12N": 26912, 
  "UTM13N": 26913,
  "UTM14N": 26914,
  "UTM15N": 26915,
  "UTM16N": 26916,
  "UTM17N": 26917,
  "UTM18N": 26918,
  "UTM19N": 26919,
}

def averageTwoInPython3(): #function to run print an average of two input numbers
    x = float(input("What is the first number?: "))
    y = float(input("What is the second number?: "))
    average = (x+y)/2
    print_this = f"The average of {x} and {y} is {average}"
    print (print_this)

def createGradebook(studentnameslist,quiznameslist):
    #DataFrame gradebook for a varaible number of students and a variable number of quizzes
    #with randomly assign grades between 0 and 5; returns a dataframe
    grades = numpy.random.randint(0,6,(len(studentnameslist),len(quiznameslist)))
    #generate two dimensional array of ramdom numbers between 0 and 5 of matching length of the input lists
    gradebook = pandas.DataFrame(grades,index=studentnameslist,columns=quiznameslist)
    #convert array two a dataframe
    return gradebook

def processGrades(gradebook):
    #create a new column forthe average grade, (2) calculate the average grade for each 
    #student and populate the new column,(3)print the students with an average grade
    #less than 50% (if no students are below, print None).
    averagegrade = gradebook.mean(1) #generate avarage of the dataframe
    gradebook["Average"] = averagegrade #add a columb and insert the average drade values
    print ("***Students with an average grade less than 50%***") 
    for names in gradebook[gradebook['Average'] < 2.5].index: 
        print (names) #print the names of studetns who have less than 50% average
    if len((gradebook[gradebook['Average'] < 2.5].index)) == 0:
        print ('None')

def plotState(country,StateToPlot,PlotColor,EPSGCode):
    #plots a given state in a defined color in the projection of a provided CRS EPSG code. 
    #return the projected geometry.
    try:
        state = country[country["NAME"] == StateToPlot] #extract state to plot from dataset
        if len(state) == 0:
            print (f"Error: State Input '{StateToPlot}' is Not Valid State")
            return None
        state = state.to_crs(epsg=EPSGCode) #reproject to ew EPSG code
        state.plot(facecolor=PlotColor) #plot state with input color
            #automatically raises a ValueError for color issue to use in the except block
        return state['geometry'] #send geometry as return value and exit
    except ValueError: #catch error on color validity from raised error
        print (f"Error: Color Input '{PlotColor}' is Not Valid Color")
        return None

def calcArea(StateToCalcArea,StateNameString,UnitsString):
    #prints the area of a projected geometry and return the calculated area as a floating point
    if UnitsString.lower()  not in ['km', 'mi']: #nomarlize and check for allowed units
        print ("Error: Invalid Units")
        return None
    if UnitsString.lower() == "km": #calculate area for km units
        Area = float(StateToCalcArea.area)/1000000 #km
    else:
        Area = float(StateToCalcArea.area)/2589988.1103 # calculate area for miles
    print(f"{StateNameString} Area = {Area:.3f} {UnitsString}^2") 
    return Area

# Test Input
#census data geo and pop data sources for testing and processing lab
country = geopandas.read_file("your path\gz_2010_us_040_00_5m.json")
population = pandas.read_csv("your path\state_population_data.csv")

print("***Part I***")
students = ["AAA","BBB","CCC","DDD","EEE","FFF","GGG","HHH","III","JJJ"]
labs = ["L1","L2","L3","L4","L5","L6","L7"]
gbook = createGradebook(students,labs)
print(gbook)
processGrades(gbook)
print(gbook)
print("***Part II***")
# Note: The variable "country" should be defined as we did earlier in the lab
maryland = plotState(country, "Maryland", "Mars Red", utm_epsg["UTM13N"])
maryland = plotState(country, "Jupiter", "Red", utm_epsg["UTM13N"])
maryland1 = plotState(country, "Maryland", "Red", utm_epsg["UTM11N"])
maryland2 = plotState(country, "Maryland", "Gold", utm_epsg["UTM18N"])
calcArea(maryland,"Maryland","nm")
md = country[country["NAME"] == "Maryland"]
obs = md["CENSUSAREA"]
print("Observed Area %0.2f mi^2" % obs)
area1 = calcArea(maryland1,"Maryland","mi")
print("Relative Error (UTM11N) = %0.2f%%" % (abs(area1 - obs) / obs * 100))
area2 = calcArea(maryland2,"Maryland","mi")
print("Relative Error (UTM18N) = %0.2f%%" % (abs(area2 - obs) / obs * 100))

