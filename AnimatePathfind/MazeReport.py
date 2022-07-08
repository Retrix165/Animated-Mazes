"""
Maze Reporting Module
By: Reid Smith

Notes:
    -None currently

Purpose:
    -To handle the data reporting from pathfinding algorithms in the AnimatePathfind Project
    -At each step of algorithm report
        -Number of Nodes in Open Set
        -Number of Nodes in Closed Set
        -Current Matrix
    -At end of algorithm report:
        -Path Length

"""
#Import deepcopy function
from copy import deepcopy

#MazeReport Class
class MazeReport:
    
    #MazeReport Object Constructor
    """
        A Maze Report Object has:
        -an optional object name
        -a list of sizes of the algorithm's open set over time
        -a list of sizes of the algorithm's closed set over time
        -an animation buffer of matrix frames to animate
        -a length of the found path
    """
    def __init__(self, report_name = "None"):
        self.name = report_name
        self.open_set_data = []
        self.closed_set_data = []
        self.matrix_buffer = []
        self.path_length = None

    #Add Size to Open Set Data List Function
    def add_to_open(self, size: int):
        self.open_set_data.append(size)

    #Add Size to Closed Set Data List Function
    def add_to_closed(self, size: int):
        self.closed_set_data.append(size)

    #Add Matrix Frame to a Matrix Buffer Function
    def add_matrix(self, matrix: list):
        self.matrix_buffer.append(deepcopy(matrix))
   
    #Set the Path Length Found Function
    def set_path_length(self, length: int):
        self.path_length = length

    #Make Data Dictionary of Object Attributes Function
    def get_data(self):
        return {"name": self.name, \
                "open set": self.open_set_data, \
                "closed set": self.closed_set_data, \
                "matrix buffer": self.matrix_buffer, \
                "length": self.path_length}

