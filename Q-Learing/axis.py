import math as m 

class Point2D:
    ...


class Line2D:
    ...

class Point2D():
    """
    A class object that describes the coordinate of the 2D object

    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property # This method let the functions only be readable
    def length(self):
        vector_length = m.sqrt(self.x**2 + self.y**2)
        
        return vector_length

    def __add__(self, input_Point: Point2D):
        new_Point = Point2D(input_Point.x + self.x, input_Point.y + self.y)

        return new_Point
    
    def __sub__(self, input_Point: Point2D):
        new_Point = Point2D(input_Point.x - self.x, input_Point.y - self.y)

        return new_Point

    def __mul__(self, input_scalar):
        new_Point = Point2D(input_scalar * self.x, input_scalar * self.y)

        return new_Point
    
    def __div__(self, input_scalar):
        if input_scalar != 0:
            new_Point = Point2D(self.x / input_scalar, self.y / input_scalar)
            return new_Point
        else:
            print("can not divide by 0")
    
    def distanceToPoint(self, input_point: Point2D):
        """
        This method is used for calculating the distance between 2 points

        Args:
            input_point: another point coordinate
        
        Returns:
            A length between 2 points
        """

        vector = self - input_point
        vector_length = vector.length

        return vector_length

    def distanceToLine(self, input_line: Line2D):
        """
        A method to describe d(P, L) = |aP_x0+b_y0+c|/sqrt(a^2+b^2)

        Args:
            input_line: A line representation

        Returns:
            A length between a point and a line
        """
        length = abs(input_line.a*self.x + input_line.b*self.y + input_line.c) / m.sqrt(input_line.a**2 + input_line.b**2)

        return length
    
    def rotate(self, angle):
        """
        A method to rotate the position of a point
        | x' |   | cosθ -sinθ | | x |
        | y' | = | sinθ  cosθ | | y |

        (x', y') = (cosθ*x-sinθ*y , sinθ*x+cosθ*y)
        Args:
            angle: theta of rotation matrix

        Returns:
            a Point2D object that describes rotated point

        """
        
        rad_angle = (angle / 180)*m.pi
        rotated_point = Point2D(self.x*m.cos(rad_angle) - self.y*m.sin(rad_angle), self.x*m.sin(rad_angle) + self.y*m.cos(rad_angle))

        return rotated_point
    
    def isInRect(self, rect_DiagP1: Point2D, rect_DiagP2: Point2D):
        """
        A method that checks the point is in a rectangle,
        which is formed by rect_DiagP1 and rect_DiagP2

        Args:
            rect_DiagP1: the diagonal point of the rectangle
            rect_DiagP2: the diagonal point of the rectangle

        Return:
            true if the point is in the rectangle, otherwise false
        
        """
        checker = False

        # Decide which diagonal points are Left-Up and Right-Down
        if rect_DiagP1.x > rect_DiagP2.x:
            right_x = rect_DiagP1.x
            left_x = rect_DiagP2.x
        else:
            right_x = rect_DiagP2.x
            left_x = rect_DiagP1.x

        if rect_DiagP1.y > rect_DiagP2.y:
            up_y = rect_DiagP1.y
            down_y = rect_DiagP2.y
        else:
            up_y = rect_DiagP2.y
            down_y = rect_DiagP1.y

        Left_Up_Point = Point2D(left_x, up_y)
        Right_Down_Point = Point2D(right_x, down_y)

        # check if this point is in the rectangle
        if Left_Up_Point.x <= self.x and self.x <= Right_Down_Point.x:
            if Left_Up_Point.y >= self.y and self.y >= Right_Down_Point.y:
                checker = True

        return checker



class Line2D():
    """
    A class object that describes the function of the 2D Line
    
    """
     
    def __init__(self, P1: Point2D, P2: Point2D):
        """
        form: (y-y1) / (x-x1) = (y2-y1) / (x2-x1) => ax + by + c = 0
        class members:
            a: (y2-y1)
            b: -(x2-x1)
            c: (x2*y1-x1*y2)

        """
        self.a = (P2.y - P1.y)
        self.b = -1 * (P2.x - P1.x)
        self.c = (P2.x*P1.y - P1.x*P2.y)
        self.start = P1
        self.end = P2
        
        if self.b == 0:
            self.slope = None  # vertical line
        else:
            self.slope = self.a / (-1*self.b)

    def pointInLine(self, input_point: Point2D, epsilon=1e-9):
        """
        A method to check the input point is in this line or not (with floating point tolerance)

        Args:
            input_point: A Point2D object

        Returns:
            If point is in the line, return True
        """

        checker = False

        if (self.start.x - epsilon <= input_point.x <= self.end.x + epsilon and
            self.start.y - epsilon <= input_point.y <= self.end.y + epsilon):
            checker = True
        elif (self.end.x - epsilon <= input_point.x <= self.start.x + epsilon and
            self.end.y - epsilon <= input_point.y <= self.start.y + epsilon): 
            checker = True

        return checker

    def angleBetweenLines(self, input_line: Line2D):
        """
        A method that find a angle between 2 lines
        we use the slope of 2 lines to get the angle

        tanθ = (m1 - m2) / 1 + m1*m2
        
        Args:
            input_line: another line 

        Returns:
            Angle that is not rad!
        """
        
        if self.slope is None or input_line.slope is None:
            return 90.0  # or handle separately
        else:
            tan = (self.slope - input_line.slope) / (1  + (self.slope*input_line.slope))
            angle = m.atan(tan)
        
            return angle
    
    def lineCollidedCheck(self, input_line: Line2D):
        """
        A method that checks if 2 lines are collided

        we need to consider 3 conditions

        1. 1 intersection point => the slope of 2 lines are different which means they will intersect at a point
        2. no intersection points => parallel, no collided
        3. infinite intersection point => overlap, collided, but we don't need to get the coordinate

        Args:
            input_line: another line

        Returns:
            True if 2 lines are collided, otherwise false
            Return the collided point position
        
        """
        
        isCollided = False
        intersect_p1 = None
        intersect_p2 = None

        # check 3rd & 2nd & 1st condition
        if self.slope == input_line.slope:
            if self.c == input_line.c: # 3rd
                isCollided = True
            else: # 2nd
                isCollided = False
        else:
            isCollided = True

            # Calculate intersect point
            # ax + by + c = 0
            # dx + ey + f = 0
            # x = (bf - ce) / (ae - bd)
            # y = (af - cd) / (bd - ae)
            f1 = self.a * input_line.b # ae
            f2 = self.b * input_line.a # bd 
            f3 = self.b * input_line.c # bf
            f4 = self.c * input_line.b # ce
            f5 = self.a * input_line.c # af
            f6 = self.c * input_line.a # cd
            f12 = f1 - f2 

            if f12 != 0:
                intersect_p1 = (f3-f4) / f12
                intersect_p2 = (f5-f6) / (-1*f12)
            else:
                print("divisor is zero!")

        
        intersect_point = Point2D(intersect_p1, intersect_p2)
        return isCollided, intersect_point


