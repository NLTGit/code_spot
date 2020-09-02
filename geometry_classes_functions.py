#python geometry classes and functions

#[1] Generic base class for geometric objects
class Geometry( object ):
    class_counter = int #generate integer counter for object id tracking
    class_counter= 0    #start object index at zero
    def __init__(self): #construct a geometry object and track its object id
        self.id= Geometry.class_counter #assign id to geometry object
        Geometry.class_counter += 1 #increment object id as they are created

#[2] Point subclass of Geometry with 2D location aurgement input (x,y)
class Point(Geometry):
    def __init__(self,x,y): # construct a point geometry object given x and y arguments
        super(Point,self).__init__() #inheretence function
        self.x = x #assign object x property the x arugment
        self.y = y #assign object y property the y arugment
        #constructs a 2D point object with x,y assignments from the arguments coming

    # return x,y coordiantes rounded to 2 decimal degrees using the string mehod and round function
    def __str__(self):
        return "(%s, %s)" % (round(self.x, 2), round(self.y, 2))
        #return x,y coordiantes rounded to 2 decimal degrees using the string method and round function

    #return boolean state for test of equality from two point aurguments
    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True #return true and exit if x and y values of both points are equal
        return False #return false and exit as alternative to true statement of point x,y values not equal

    #return the distance between 2 points given a the orgin (self) and an argument point
    def distance(self, other):
        xdistsquared = (other.x - self.x)**2 #generate distance squared of x values of two points
        ydistsquared = (other.y - self.y)**2 #generate distance squared of y values of two points
        sumofsquares = xdistsquared + ydistsquared #sume the two squared distances
        return sumofsquares**0.5  #return result of square root equavelant using 1/2 (eg 0.5) for the square root

    #return the cartesean quadrant location of a point
    def quadrant (self):
        #check the point location on the quadrant and return the quadrant location as a string
        if self.x > 0 and self.y > 0: return "Quad I" # check coordinate location for quadrant 1
        if self.x < 0 and self.y > 0: return "Quad II" # check coordinate location for quadrant 2
        if self.x < 0 and self.y < 0: return "Quad III" # check coordinate location for quadrant 3
        if self.x > 0 and self.y < 0: return "Quad IV" # check coordinate location for quadrant 4
        if self.x == 0 and self.y == 0: return "Origin" #check if the point is at the origin
        if self.x == 0 : return "Y-axis" #check if the point is on the Y axis
        if self.y == 0 : return "X-axis" #check if the point is on the X axis

#create Line object given 2 points
class Line(Geometry):
    def __init__(self,p1,p2): # construct an instance of a line given two point arguments
        super(Line,self).__init__() #inheretence function
        self.p1=p1 #assign the first aurgment point to the first point of the line
        self.p2=p2 #assign the second argument point tothe second point of the line
        self.m = (p2.y-p1.y)/(p2.x-p1.x) #dervive the slope using the two input points
        self.b = p1.y - self.m*p1.x #dervie the intercept using the slope and one of the point values

    #string method returns a string of the line in "y = m * x + b" format
    def __str__(self):
        return "y = {m:.2f} * x + {b:.2f}".format(m=round(self.m,2), b=round(self.b,2))
        #return the print call of line class objects using string method to format
        # in the point,slope, and intercept expression with riunding to 2 decimal places

    #return boolean state if the slopes of two lines are the same or not
    def parallel (self, other):
        return self.m == other.m
        #return true or false depending on the
        # equality of the two line slopes being equeal or not.

#test colliniearity of 3 points by testing the slope of lines connecting the points
def collinear (p1,p2,p3):
    slope1 = (p2.y-p1.y)/(p2.x-p1.x) #generate  slope between point 1 and point 2
    slope2 = (p3.y-p2.y)/(p3.x-p2.x) #generate slope betwen point 2 ad point 3
    return slope1 == slope2 #return boolean state if the slopes are equal or not between



# Test Input
def pointTest():
    print "***Point Class Test***"
    p1 = Point(0,3)
    p2 = Point(-3,7)
    p3 = Point(-3,7)
    print "P1) ID = %d, Coords = %s, Location = %s" % (p1.id, p1, p1.quadrant())
    print "P2) ID = %d, Coords = %s, Location = %s" % (p2.id, p2, p2.quadrant())
    print "P3) ID = %d, Coords = %s, Location = %s" % (p3.id, p3, p3.quadrant())
    print "Distance between P1 and P2 = %.2f" % p1.distance(p2)
    print "Distance between P2 and P3 = %.2f" % p2.distance(p3)
    print "Distance between P1 and P3 = %.2f" % p1.distance(p3)
    print "P1 == P2?", p1 == p2
    print "P2 == P3?", p2 == p3
    print "P1 == P3?", p1 == p3
pointTest()
def linearTest():
    print "***Linearity Test***"
    p1 = Point(0,0)
    p2 = Point(1,1)
    p3 = Point(2,3)
    print p1, p2, p3
    print "Are P1, P2, and P3 on the same line?", collinear(p1,p2,p3)
    p4 = Point(0,0)
    p5 = Point(-1,-3)
    p6 = Point(-2,-6)
    print p4, p5, p6
    print "Are P4, P5, and P6 on the same line?", collinear(p4,p5,p6)
linearTest()
def lineTest():
    print "***Line Class Test***"
    p1 = Point(-1,-1)
    p2 = Point(1,1)
    p3 = Point(3,4)
    print p1, p2, p3
    line1 = Line(p1,p2)
    line2 = Line(p2,p3)
    print "L1) ID = %d, Equation = %s" % (line1.id, line1)
    print "L2) ID = %d, Equation = %s" % (line2.id, line2)
    print "Are L1 and L2 parallel?", line1.parallel(line2)
lineTest()


""" 
#Main method to run classes and functions tests during development
if __name__ == "__main__":
    p1 = Point(1.216, 3.4582)
    print p1.id, p1

    g=Geometry()  # showing the indexing location is using unoverdided id for gemotery
    print g

    p1, p2 = Point(-2, 1), Point(1, 5)
 

    p1, p2 = Point(-2,1), Point(1,5)
    print p1
    print p2
    print p1==p2
    print p1.distance(p2)
    print p1.quadrant()
    print p2.quadrant()
 
    # p1, p2, p3 = Point(0,0), Point(3,3), Point(2,4)
    # print "Are P1, P2, and P3 on the same line?", collinear(p1, p2, p3)
    p4, p5, p6 = Point(0,0), Point(3,3), Point(5,5)
    print "Are P4, P5, and P6 on the same line?", collinear(p4,p5,p6)

    p1, p2, p3 = Point(0, -6), Point(3, 3), Point(6, 0)  # IDs = 0, 1, 2
    line1 = Line(p1, p2)  # ID = 3
    line2 = Line(p2, p3)  # ID = 4
    print line1.id, line1.m, line1.b
    print line1
    print line2
    print line1.parallel(line2)
    
"""

