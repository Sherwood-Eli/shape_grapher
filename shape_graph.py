import tkinter as tk
import math
import random

#colors = ["red", "green", "blue", "yellow", "orange", "purple"]

#colors = ["steel blue", "medium aquamarine", "DeepSkyBlue3", "MediumPurple1", "yellow green"]

colors = ["firebrick1", "firebrick2","firebrick3","firebrick4", "DarkOrange1", "DarkOrange2", "DarkOrange3", "DarkOrange4"]

#colors = ["orchid2", "HotPink1", "medium violet red", "light coral", "maroon2", "MediumOrchid1", "dodger blue", "cornflower blue"]

GRID_SCALE = 30

C_WIDTH = (1300//(2*GRID_SCALE))*GRID_SCALE*2
C_HEIGHT = (800//(2*GRID_SCALE))*GRID_SCALE*2

X_OFFSET = C_WIDTH//2
Y_OFFSET = C_HEIGHT//2

Y_MIN = (Y_OFFSET*-1)//GRID_SCALE
Y_MAX = Y_OFFSET//GRID_SCALE
X_MIN = (X_OFFSET*-1)//GRID_SCALE
X_MAX = X_OFFSET//GRID_SCALE

#Converts logical x values to the x values recognized by TK
def x(val):
    return ((val*GRID_SCALE)+X_OFFSET)

#Converts logical y values to the y values recognized by TK
def y(val):
    return ((val*-1*GRID_SCALE)+Y_OFFSET)



#An Intersection is a point on the graph where two or more lines intersect

class Intersection:
    def __init__(self, x_coord, y_coord):
        self.x = x_coord
        self.y = y_coord
        self.lines = []
        self.neighbors = []

    def add_line(self, line):
        for l in self.lines:
            if l.type == "l":
                if l.yint == line.yint and l.slope == line.slope:
                    l.add_intersection(self)
                    return False
            else:
                if l.xint == line.xint:
                    l.add_intersection(self)
                    return False

        self.lines.append(line)
        line.add_intersection(self)
        return True

    def find_neighbors(self):
        self.neighbors = []
        print("Finding neighbors of")
        self.print_self()
        for line in self.lines:
            line.find_neighbors_of(self)

    def add_neighbor(self, new_neighbor):
        self.neighbors.append(new_neighbor)
        print("adding neighbor")
        new_neighbor.print_self()
        print("to")
        self.print_self()

    def print_neighbors(self):
        print("neighbors of (" + str(self.x) + ", " + str(self.y) + ") [", end="")
        for inter in self.neighbors:
            print("(" + str(inter.x) + ", " + str(inter.y) + ")", end=" ")
        print("]")

    def print_self(self):
        print("(" + str(self.x) + ", " + str(self.y) + ")")



class Line:
    def __init__(self, l_type, slope, yint, xint):
        self.type = l_type
        self.slope = slope
        self.yint = yint
        self.xint = xint
        self.intersections = []

    def add_intersection(self, intersection):
        i = 0
        if self.type == "l":
            while i < len(self.intersections) and self.intersections[i].x > intersection.x:
                i+=1
        elif self.type == "v":
            while i < len(self.intersections) and self.intersections[i].y > intersection.y:
                i+=1
        
        if i >= len(self.intersections) or self.intersections[i].x != intersection.x:
            self.intersections.insert(i, intersection)
        return i

    def find_neighbors_of(self, intersection):
        for i in range(0, len(self.intersections)):
            if self.intersections[i].x == intersection.x and self.intersections[i].y == intersection.y:
                if i > 0:
                    intersection.add_neighbor(self.intersections[i-1])
                if i < len(self.intersections)-1:
                    intersection.add_neighbor(self.intersections[i+1])
                return
    
    def print_intersections(self):
        if self.type == "v":
            print("x = " + str(self.xint) + ": [", end="")
        else:
            print("y = " + str(self.slope) + "x + " + str(self.yint) + ": [", end="")
        for inter in self.intersections:
            print("(" + str(inter.x) + ", " + str(inter.y) + ")", end=" ")
        print("]")


class Shape:
    def __init__(s, points):
        s.poly_id = 0
        s.points = points
        s.area = s.get_area()


    def get_area(s):
        return -1



class Shape_Graph:
    def __init__(s):
        print(s.signed_angle((1, 0), (0, 1)))
        print(s.signed_angle((0, 1), (1, 0)))
        print(s.signed_angle((1, -1), (1, 1)))
        print(s.signed_angle((1, 1), (1, -1)))


        #Initialize object lists
        s.lines = []
        s.intersections = []
        s.shapes = []

        #Lets the graph know if the shapes are drawn or not
        s.shapes_are_drawn = False
        s.auto_color = False
        s.coloring_protocol = False

        #Initialize TK features
        s.root = tk.Tk()
        s.canvas = tk.Canvas(s.root, width=C_WIDTH, height=C_HEIGHT, bg='white')
        s.canvas.pack()

        #Initialize Graphing Plane
        
        #X and Y Axes
        s.canvas.create_line(0, C_HEIGHT//2, C_WIDTH, C_HEIGHT//2, fill="black", width=6)
        s.canvas.create_line(C_WIDTH//2, 0, C_WIDTH//2, C_HEIGHT, fill="black", width=6)
        
        #Create grid
        i=0
        while i < Y_MAX:
            i+=1
            s.canvas.create_line(0, y(i), C_WIDTH, y(i), fill="black", width=1);
            s.canvas.create_line(0, y(-i), C_WIDTH, y(-i), fill="black", width=1);
        i=0
        while i < X_MAX:
            i+=1
            s.canvas.create_line(x(i), 0, x(i), C_HEIGHT, fill="black", width=1);
            s.canvas.create_line(x(-i), 0, x(-i), C_HEIGHT, fill="black", width=1);
    
    def mainloop(s):
        s.root.mainloop()

    def toggle_auto_color(s):
        s.auto_color = not s.auto_color

    def get_auto_color(s):
        return s.auto_color

    def toggle_coloring_protocol(s):
        s.coloring_protocol = not s.coloring_protocol

    def get_coloring_protocol(s):
        return s.coloring_protocol





    ########################
    #Graph Drawing Functions
    ########################

    #Draw linear eqution and update logical model accordingly
    def linear_equation(s, slope, yint):
        s.canvas.create_line(0, y((X_MIN*slope)+yint), C_WIDTH, y((X_MAX*slope)+yint), fill="green", width="3")
        
        new_line = Line("l", slope, yint, None)

        for old_line in s.lines:
            s.find_intersection(new_line, old_line)

        s.lines.append(new_line)

        if s.auto_color:
            #No guarantee that any of the shapes have not changed
            #print("calling find all shapes")
            s.find_all_shapes()
            #print("calling draw all shapes")
            s.draw_all_shapes()

    #Draw a vertical line and update logical model accordingly
    def vertical_line(s, xint):
        s.canvas.create_line(x(xint), 0, x(xint), C_HEIGHT, fill="green", width="3")

        new_line = Line("v", None, None, xint)

        for old_line in s.lines:
            s.find_intersection(new_line, old_line)

        s.lines.append(new_line)

        if s.auto_color:
            #No guarantee that any of the shapes have not changed
            s.find_all_shapes()
            s.draw_all_shapes()

    def draw_circle(s, x_coord, y_coord, r):
        s.canvas.create_oval(x(x_coord - r), y(y_coord - r), x(x_coord + r), y(y_coord + r), outline="red", width=2)

    #Draws all shapes that the graph has found, must be run  after draw_all_shapes has been run
    def draw_all_shapes(s):
        print("Drawing " + str(len(s.shapes)) + " shapes")
        for shape in s.shapes:
            s.draw_shape(shape)


    def draw_shape(s, shape):
        shape_coords = []
        for coord in shape.points:
            shape_coords.append((x(coord.x), y(coord.y)))
        #print("making shape: ", shape_coords)
        #c.create_polygon(*shape_coords, fill=colors[random.randint(0,len(colors)-1)], outline='black')
        s.canvas.create_polygon(*shape_coords, fill="#{:02x}{:02x}{:02x}".format(random.randint(0,255), random.randint(0, 255), random.randint(0,255)), outline='black')


    def rerender_shapes(s):
        s.find_all_shapes()
        s.draw_all_shapes()


    
    #################
    #Graph Operations
    #################

    #Finds the intersection between two lines
    #The intersection will have the lines added to it so we can later know which lines go through the point
    def find_intersection(s, l1, l2):
        if l1.type == "v" and l2.type == "v":
            return
        if l1.type == "v":
            x_coord, y_coord = s.vertical_intersection(l2.slope, l2.yint, l1.xint)
        elif l2.type == "v":
            x_coord, y_coord = s.vertical_intersection(l1.slope, l1.yint, l2.xint)
        elif l1.slope == l2.slope:
            return
        else:
            x_coord, y_coord = s.linear_intersection(l1.slope, l1.yint, l2.slope, l2.yint)

        new_intersection = s.add_intersection(x_coord, y_coord)

        new_intersection.add_line(l1)
        new_intersection.add_line(l2)

    #Adds a unique intersection to the graph's intersection data structure only if unique
    def add_intersection(s, x_coord, y_coord):
        i = 0
        while i < len(s.intersections) and x_coord < s.intersections[i][0].x:
            i+=1
        j = 0
        if i < len(s.intersections) and x_coord == s.intersections[i][0].x:
            #print("found row: ", x_coord, "intersect: ", s.intersections[i][0].x, s.intersections[i][0].y)
            while j < len(s.intersections[i]) and y_coord < s.intersections[i][j].y:
                j+=1
            if j < len(s.intersections[i]) and y_coord == s.intersections[i][j].y:
                #intersection already found
                return s.intersections[i][j]
        else:
            s.intersections.insert(i, [])
        
        new_intersection = Intersection(x_coord, y_coord)
        s.intersections[i].insert(j, new_intersection)

        return new_intersection

    #Finds the intersection between two linear equations of the form 'y=mx+b'
    def linear_intersection(s, s1, y1, s2, y2):
        s = s1-s2
        yint = y1-y2

        final_x = (-1*yint)/s
        final_y = (s1*final_x)+y1

        return final_x, final_y

    #Finds the intersection between a vertical line 'x=?' and a linear equation 'y=mx+b'
    def vertical_intersection(s, slope, yint, final_x):
        final_y = (slope*final_x)+yint

        return final_x, final_y



    #Finds the signed angle between two vectors
    #(+) clockwise
    #(-) counter-clockwise
    def signed_angle(s, A, B):
        cross = A[0]*B[1] - A[1]*B[0]
        dot = A[0]*B[0] + A[1]*B[1]
        #by multiplying by negative 1, the resulting angle is positive if B is in the next pi degrees clockwise of A
        return -1*math.atan2(cross, dot)  # result in radians

    
    #Finds the next point in a shape traversal
    #Traversal can be either clockwise or counter-clockwise depending on the sign of 'direction'
    def find_next_point(s, cur_point, vi, direction):
        best_p = None
        best_angle = -4
        best_v = None
        best_i = None
        cur_point.print_neighbors()
        for i in range(len(cur_point.neighbors)):
            n = cur_point.neighbors[i]
            vf = (n.x-cur_point.x, n.y-cur_point.y)
            angle = direction*s.signed_angle(vi, vf)
            print("\nchecking point: (" + str(n.x) + ", " + str(n.y) + ")")
            print("Angle: " + str(angle))
            if angle != math.pi and angle > best_angle:
                best_angle = angle
                best_p = n
                best_v = vf
                best_i = i
                print("looks good!")
            else:
                print("not what we want")

        if best_angle <=0:
            #print("deadend")
            return None, None

        print("choosing next point: (" + str(best_p.x) + ", " + str(best_p.y) + ")")
        print("new_v: " + str(best_v))
        #Remove point from neighbors so we do not consider this unique vector again
        cur_point.neighbors.pop(best_i)
        return best_p, best_v


    #Finds a shape starting with the vector between p1 and p2. Will serch in the direction specified
    def find_a_shape(s, p1, p2, direction):
        print("Finding shapes starting at (" + str(p1.x) + ", " + str(p1.y) + ")-->(" + str(p2.x) + ", " + str(p2.y) + ") and moving in the " + str(direction) + " direction")

        cur_shape = []
        vi = (p2.x-p1.x, p2.y-p1.y)
        cur_point = p2
        cur_shape.append(p1)
        cur_shape.append(p2)
        while (cur_point.x != p1.x or cur_point.y != p1.y):
            cur_point, vi = s.find_next_point(cur_point, vi, direction)
            if cur_point == None:
                return None
            cur_shape.append(cur_point)

        return Shape(cur_shape)



    #Finds all shapes in the current state of the graph
    def find_all_shapes(s):
        #get rid of current shapes if exist
        if len(s.shapes) != 0:
            for shape in s.shapes:
                s.canvas.delete(shape.poly_id)
            s.shapes = []

        s.shapes = []
        for inter_list in s.intersections:
            for inter in inter_list:
                inter.find_neighbors()
                print("(" + str(inter.x) + ", " + str(inter.y) + ")", end=" ")
                s.draw_circle(inter.x, inter.y, .5)
                inter.print_neighbors()

        #Need to check for shapes after all neighbors have been found
        for inter_list in s.intersections:
            for inter in inter_list:
                for n in inter.neighbors:
                    new_shape = s.find_a_shape(inter, n, 1)
                    if new_shape != None:
                        s.shapes.append(new_shape)

            #print("")

        for line in s.lines:
            line.print_intersections()







