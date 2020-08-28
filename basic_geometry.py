class Geometry( object ):
    class_counter= 0
    def __init__(self):
        self.id= Geometry.class_counter
        Geometry.class_counter += 1


class Point(Geometry):
    def __init__(self,x,y):
        super(Point,self).__init__()
        self.x = x
        self.y = y

    def __str__(self):
        return "(%s, %s)" % (round(self.x, 2), round(self.y, 2))
        # return "({x}, {y})".format(x=round(), y=round()) <--alternative format for string method
        # return "({x}, {y})".format(x=round(), y=round())

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False

    def distance(self, other):
        xdistsquared = (other.x - self.x)**2
        ydistsquared = (other.y - self.y)**2
        sumofsquares = xdistsquared + ydistsquared
        return sumofsquares**0.5  #return boolean result of square root equavelant using 1/2 (eg 0.5) for the square root

    def quadrant (self):
        if self.x > 0 and self.y > 0: return "Quad I"
        if self.x < 0 and self.y > 0: return "Quad II"
        if self.x < 0 and self.y < 0: return "Quad III"
        if self.x > 0 and self.y < 0: return "Quad IV"
        if self.x == 0 and self.y == 0: return "Origin"
        if self.x == 0 : return "Y-axis"
        if self.y == 0 : return "X-axis"

class Line(Geometry):
    def __init__(self,p1,p2):
        super(Line,self).__init__()
        self.p1=p1
        self.p2=p2
        self.m = (p2.y-p1.y)/(p2.x-p1.x)
        self.b = p1.y - self.m*p1.x

    def __str__(self):
        return "y = {m:.2f} * x + {b:.2f}".format(m=round(self.m,2), b=round(self.b,2))

    def parallel (self, other):
        return self.m == other.m


def collinear (p1,p2,p3):
    slope1 = (p2.y-p1.y)/(p2.x-p1.x)
    slope2 = (p3.y-p2.y)/(p3.x-p2.x)
    return slope1 == slope2



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
