import tkinter as tk
import math
import random
import threading

#colors = ["red", "green", "blue", "yellow", "orange", "purple"]

#colors = ["steel blue", "medium aquamarine", "DeepSkyBlue3", "MediumPurple1", "yellow green"]

colors = ["firebrick1", "firebrick2","firebrick3","firebrick4", "DarkOrange1", "DarkOrange2", "DarkOrange3", "DarkOrange4"]

#colors = ["orchid2", "HotPink1", "medium violet red", "light coral", "maroon2", "MediumOrchid1", "dodger blue", "cornflower blue"]

class Intersection:
    def __init__(self, x_coord, y_coord):
        self.x = x_coord
        self.y = y_coord
        self.lines = []
        self.neighbors = []
        self.found_by = -1

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
        for line in self.lines:
            line.find_neighbors_of(self)

    def add_neighbor(self, new_neighbor):
        self.neighbors.append(new_neighbor)


    def be_found(self, found_id):
        if self.found_id == -1:
            self.found_id = found_id
            for n in self.neighbors:
                n.be_found(found_id+1)


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

        self.intersections.insert(i, intersection)
        return i

    def find_neighbors_of(self, intersection):
        for i in range(0, len(self.intersections)):
            if self.intersections[i].x == intersection.x and self.intersections[i].y == intersection.y:
                if i > 0:
                    intersection.add_neighbor(self.intersections[i-1])
                if i < len(self.intersections)-1:
                    intersection.add_neighbor(self.intersections[i+1])





GRID_SCALE = 30

C_WIDTH = (1300//(2*GRID_SCALE))*GRID_SCALE*2
C_HEIGHT = (800//(2*GRID_SCALE))*GRID_SCALE*2

X_OFFSET = C_WIDTH//2
Y_OFFSET = C_HEIGHT//2

Y_MIN = (Y_OFFSET*-1)//GRID_SCALE
Y_MAX = Y_OFFSET//GRID_SCALE
X_MIN = (X_OFFSET*-1)//GRID_SCALE
X_MAX = X_OFFSET//GRID_SCALE

cur_explorer_id = 0

linear_equations = []
verticals = []
intersections = []

shapes = []

root = tk.Tk()
canvas = tk.Canvas(root, width=C_WIDTH, height=C_HEIGHT, bg='white')
canvas.pack()

canvas.create_line(0, C_HEIGHT//2, C_WIDTH, C_HEIGHT//2, fill="black", width=6)
canvas.create_line(C_WIDTH//2, 0, C_WIDTH//2, C_HEIGHT, fill="black", width=6)

def x(val):
    return ((val*GRID_SCALE)+X_OFFSET)

def y(val):
    return ((val*-1*GRID_SCALE)+Y_OFFSET)


def add_intersection(x_coord, y_coord):
    i = 0
    while i < len(intersections) and x_coord < intersections[i][0].x:
        i+=1
    j = 0
    if i < len(intersections) and x_coord == intersections[i][0].x:
        print("found row: ", x_coord, "intersect: ", intersections[i][0].x, intersections[i][0].y)
        while j < len(intersections[i]) and y_coord < intersections[i][j].y:
            j+=1
        if j < len(intersections[i]) and y_coord == intersections[i][j].y:
            #intersection already found
            return intersections[i][j]
    else:
        intersections.insert(i, [])
    
    new_intersection = Intersection(x_coord, y_coord)
    intersections[i].insert(j, new_intersection)

    return new_intersection

        

def find_intersection(l1, l2):
    if l1.type == "v" and l2.type == "v":
        return
    if l1.type == "v":
        x_coord, y_coord = vertical_intersection(l2.slope, l2.yint, l1.xint)
    elif l2.type == "v":
        x_coord, y_coord = vertical_intersection(l1.slope, l1.yint, l2.xint)
    elif l1.slope == l2.slope:
        return
    else:
        x_coord, y_coord = linear_intersection(l1.slope, l1.yint, l2.slope, l2.yint)

    new_intersection = add_intersection(x_coord, y_coord)

    new_intersection.add_line(l1)
    new_intersection.add_line(l2)

def signed_angle(A, B):
    cross = A[0]*B[1] - A[1]*B[0]
    dot = A[0]*B[0] + A[1]*B[1]
    return math.atan2(cross, dot)  # result in radians
        
def find_next_point(cur_point, vi, direction):
    best = None
    best_angle = -4
    best_v = None
    for n in cur_point.neighbors:
        vf = (n.x-cur_point.x, n.y-cur_point.y)
        angle = direction*signed_angle(vi, vf)
        print("\nchecking point: (" + str(n.x) + ", " + str(n.y) + ")")
        print("Angle: " + str(angle))
        if angle != math.pi and angle > best_angle:
            best_angle = angle
            best = n
            best_v = vf
            print("looks good!")
        else:
            print("not what we want")

    if best_angle <=0:
        print("deadend")
        return None, None

    print("choosing next point: (" + str(best.x) + ", " + str(best.y) + ")")
    print("new_v: " + str(best_v))
    return best, best_v


def find_a_shape(p1, p2, direction):
    print("Finding shapes starting at (" + str(p1.x) + ", " + str(p1.y) + ")-->(" + str(p2.x) + ", " + str(p2.y) + ") and moving in the " + str(direction) + " direction")

    cur_shape = []
    vi = (p2.x-p1.x, p2.y-p1.y)
    cur_point = p2
    cur_shape.append(p1)
    cur_shape.append(p2)
    while (cur_point.x != p1.x or cur_point.y != p1.y):
        cur_point, vi = find_next_point(cur_point, vi, direction)
        if cur_point == None:
            return None
        cur_shape.append(cur_point)

    return cur_shape


def find_shapes(starting_point):
    all_shapes = []

    for n in starting_point.neighbors:
        new_shape = find_a_shape(starting_point, n, 1)
        if new_shape != None:
            all_shapes.append(new_shape)

    return all_shapes



def linear_intersection(s1, y1, s2, y2):
    s = s1-s2
    yint = y1-y2

    final_x = (-1*yint)/s
    final_y = (s1*final_x)+y1

    return final_x, final_y

def vertical_intersection(s, yint, final_x):
    final_y = (s*final_x)+yint

    return final_x, final_y


#Create grid
def create_grid():
    i=0
    while i < Y_MAX:
        i+=1
        canvas.create_line(0, y(i), C_WIDTH, y(i), fill="black", width=1);
        canvas.create_line(0, y(-i), C_WIDTH, y(-i), fill="black", width=1);
    i=0
    while i < X_MAX:
        i+=1
        canvas.create_line(x(i), 0, x(i), C_HEIGHT, fill="black", width=1);
        canvas.create_line(x(-i), 0, x(-i), C_HEIGHT, fill="black", width=1);


def linear_equation(slope, yint):
    canvas.create_line(0, y((X_MIN*slope)+yint), C_WIDTH, y((X_MAX*slope)+yint), fill="green", width="3")
    linear_equations.append(Line("l", slope, yint, None))

def vertical_line(xint):
    canvas.create_line(x(xint), 0, x(xint), C_HEIGHT, fill="green", width="3")
    verticals.append(Line("v", None, None, xint))

def draw_circle(c, x_coord, y_coord, r):
    c.create_oval(x(x_coord - r), y(y_coord - r), x(x_coord + r), y(y_coord + r), outline="red", width=2)

def draw_shape(shape, c):
    shape_coords = []
    for coord in shape:
        shape_coords.append((x(coord.x), y(coord.y)))
    print("making shape: ", shape_coords)
    #c.create_polygon(*shape_coords, fill=colors[random.randint(0,len(colors)-1)], outline='black')
    c.create_polygon(*shape_coords, fill="#{:02x}{:02x}{:02x}".format(random.randint(0,255), random.randint(0, 255), random.randint(0,255)), outline='black')

'''
#Incomplete, not sure if I will want to use this anyway
def parse_equation(equation):
    c = 0
    cur_token=""
    x_co = 0
    y_co = 0
    b_val = 0
    equals_found=False
    cur_sign = 1
    while c < len(equation):
        if equation[c].isnumeric():
            while equation[c].isnumeric():
                cur_token += equation[c]
                c+=1
            if equation[c] == 'x':
                x_co += (cur_sign*float(cur_token)
        elif equation[c] == '-':
            cur_sign = -1

'''
    

'''
linear_equation(2, 4)
linear_equation(0, 4)
linear_equation(0, -2)
vertical_line(2)
vertical_line(-1)
vertical_line(-5)
linear_equation(0, -5)
linear_equation(-1, 10)
'''

create_grid()
'''
linear_equation(0, 5)
linear_equation(0, -12)
linear_equation(0, 12)
linear_equation(0, -5)
linear_equation(0, 0)
linear_equation(-1, 4)
linear_equation(-1, -4)
linear_equation(1, 4)
linear_equation(5, 0)
linear_equation(.2, 0)
linear_equation(-5, 0)
linear_equation(-.2, 0)
linear_equation(1, -4)
vertical_line(-7)
vertical_line(7)
vertical_line(-18)
vertical_line(18)
'''


#Rueben:
linear_equation(2, 0)
linear_equation(-2, 0)
linear_equation(.5, 0)
linear_equation(-.5, 0)
linear_equation(0, 0)
linear_equation(0, 4)
linear_equation(0, -4)
linear_equation(1, -6)
linear_equation(1, 6)
linear_equation(-1, -6)
linear_equation(-1, 6)
vertical_line(-4)
vertical_line(4)
vertical_line(0)


'''
eleanor
vertical_line(4)
vertical_line(-4)
linear_equation(-1, 2)
linear_equation(1, 2)
linear_equation(1, -2)
linear_equation(-1, -2)
linear_equation(-1, 0)
linear_equation(1, 0)
linear_equation(0, 4)
linear_equation(0, -4)
linear_equation(1, 6)
linear_equation(1, -6)
linear_equation(-1, -6)
linear_equation(-1, 6)
'''

'''
Nathaniel
linear_equation(0, 0)
linear_equation(0, 2)
linear_equation(2, 16)
linear_equation(0, 4)
linear_equation(0, 7)
linear_equation(0, 8)
linear_equation(0, 3)
linear_equation(0, 9)
vertical_line(-10)
vertical_line(7)
vertical_line(9)
vertical_line(10)
vertical_line(11)
'''

for i1 in range(0, len(linear_equations)):
    for i2 in range(i1+1, len(linear_equations)):
        l1 = linear_equations[i1]
        l2 = linear_equations[i2]
        find_intersection(l1, l2)

for v in verticals:
    for l in linear_equations:
        find_intersection(v, l)

shapes = []
for inter_list in intersections:
    for inter in inter_list:
        inter.find_neighbors()
        print("(" + str(inter.x) + ", " + str(inter.y) + ")", end=" ")
        #draw_circle(canvas, inter.x, inter.y, .5)
        shapes.extend(find_shapes(inter))
    print("")

print(shapes)
for shape in shapes:
    draw_shape(shape, canvas)

'''
def user_loop():
    while true:
        print("What would you like to do?")
        print("'l' - graph a line")
        action = input("")[0]

        if action == 'l':
            go_on = True
            while go_on:
                print("Add line? ('y' or 'n')")
                go_on = 'y' == input("")[0]
                if go_on:
                    y_co = input("Y-coefficient: ")
                    x_co = input("X-coefficient: ")
                    b = input("b: ")
'''


root.mainloop()
