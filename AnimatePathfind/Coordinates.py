"""
Basic Coordinate Module
By: Reid Smith

Notes:
    -Baseline Infomration of a Coordinate/Node/Vertice for pathfinding the AnimatePathfind Project

Purpose:
    -To Store information about a 

"""

#Basic Coordinate Class (Used in BFS)
class BasicCoordinate: 

    goal_x = None
    goal_y = None


    #Constructor of Coordinate Class
    def __init__(self, x, y, data, parent = None):

        self.x = x
        self.y = y
        self.data = data
        self.parent = parent

        if self.parent is None:
            self.count = 0
        else: 
            self.count = self.parent.count + 1

    #Check if is Goal Position Function
    def is_goal(self):

        return BasicCoordinate.goal_x == self.x and BasicCoordinate.goal_y == self.y


    #Object Comparison (for in/not in Operators) Function
    def __eq__(self,other):

        if other is None or not isinstance(other,BasicCoordinate):
            return False

        return other.x == self.x and other.y == self.y


    #String Typecast Function
    def __str__(self):

        #Parent attribute not listed to prevent recursive loop
        return "x: {} y: {} data: {}".format(self.x, self.y, self.data)




#A* Coordinate Class
class AStarCoordinate(BasicCoordinate):

    #Initialization (Constructor) Function that Overrides Parent Class
    def __init__(self, x, y, data, parent = None):
        
        self.x = x
        self.y = y
        self.data = data
        self.parent = parent

        self._update_costs()


    #G (Cost to Reach Coordinate) Function
    def _calculate_g(self):

        if self.parent is not None:
            return self.parent.g + 1
        else:
            return 0


    #H (Heuristic to Reach Goal Coordinate) Function (Uses Manhattan Distance Estimation)
    def _estimate_h(self):

        if BasicCoordinate.goal_x is None or BasicCoordinate.goal_y is None:
            raise Exception("Goal Position Not Set")

        x_dist = self.x - BasicCoordinate.goal_x
        y_dist = self.y - BasicCoordinate.goal_y

        if y_dist < 0:
            y_dist *= -1
        if x_dist < 0:
            x_dist *= -1
        
        return x_dist + y_dist

    
    #F (Combined G & H Cost) Function
    def _calculate_f(self):

        return self.g + self.h


    #Update Object's Costs Function
    def _update_costs(self):

        self.g = self._calculate_g()
        self.h = self._estimate_h()
        self.f = self._calculate_f()

    
    #Less Than Operator (Used for Sorting AStarCoordinate Objects within a PriorityQueue Object)
    #Essentially, implementing a .compareTo(other) for python
    def __lt__(self, other):
        
        if other is None:
            raise Exception("None Other Coordinate Given")

        if not isinstance(other,BasicCoordinate):
            raise ValueError("Unfit Comparison between Coordinate and Non-Coordinate Object")

        return self.f < other.f


    #String Typecast Function that Overrides Parent Class
    def __str__(self):

        return "x: {} y: {} data: {} g: {} h: {} f: {}".format(self.x, self.y, self.data, self.g, self.h, self.f)





#Diagnostics of Construction and Functions (if run directly)
if __name__ == "__main__":

    print("Running Coordinate's BasicCoordinate Class Diagnostics:")
    print("\tCreating Test BasicCoordinate Objects and Set Up Goal: ", end= "")

    BasicCoordinate.goal_x = 0
    BasicCoordinate.goal_y = 0

    coord_1 = BasicCoordinate(5, 10, "Test Value")
    coord_2 = BasicCoordinate(5, 10, "Another Test Value", parent= coord_1)

    print("Success!")
    print("\tComparing Two BasicCoordinate Objects: ", end= "")

    assert(coord_1 == coord_2)

    coord_1.x = 100

    assert(not (coord_1 == coord_2))

    coord_1.x = 5

    list_coord = BasicCoordinate(5,10,"Testicles: Hero of Troy")

    test_list = [list_coord]

    assert(coord_1 in test_list)

    print("Success!")
    print("\tCheck if BasicCoordinates are at Goal Position: ",end="")

    assert(not coord_1.is_goal())

    coord_1.x = 1
    coord_1.y = 1

    BasicCoordinate.goal_x = 1
    BasicCoordinate.goal_y = 1

    assert(coord_1.is_goal())

    print("Success!")

