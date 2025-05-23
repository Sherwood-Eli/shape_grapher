
from shape_graph import Shape_Graph


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
'''
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


def parse_input(equation):
    equation_list = equation.split(" ")
    if len(equation_list) != 3:
        return None, None, None
    print(equation_list)
    return int(equation_list[0]), int(equation_list[1]), int(equation_list[2])


def user_loop(sg):
    while True:
        print("What would you like to do?")
        print("'l' - enter lines")
        print("'c' - enter color rules")
        print("'d' - do coloring")
        if sg.get_coloring_protocol():
            print("'r' - toggle random coloring/follow color rules (current: follow color rules)")
        else:
            print("'r' - toggle random coloring/follow color rules (current: random coloring)")
        if sg.get_auto_color():
            print("'a' - toggle auto color/color when directed (current: auto color)")
        else:
            print("'a' - toggle auto color/color when directed (current: color when directed)")

        action = input("")[0]

        print("action", action)
        print("num shapes:", len(sg.shapes))

        if action == 'l':
            go_on = True
            while go_on:
                print("Enter line or input 'f' when finished")
                new_equation = input("")
                go_on = 'f' != new_equation[0]
                if go_on:
                    y_co, x_co, b = parse_input(new_equation)
                    if y_co != None:
                        if y_co == 0:
                            sg.vertical_line(-1*(b/x_co))
                        else:
                            sg.linear_equation(x_co/y_co, b/y_co)
        elif action == 'd':
            sg.rerender_shapes()  
        elif action == 'r':
            sg.toggle_color_protocol()
        elif action == 'a':
            sg.toggle_auto_color()



sg = Shape_Graph()

user_loop(sg)





