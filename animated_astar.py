"""
Maze Image Solver using A* Algorithm Module
By: Reid Smith

Notes:
    -Upgraded version of the A* image maze solver from previous project that reports data/statistics now
Purpose:

"""
from PIL import Image
from Coordinates import * 
from ImageConvert import * 
from PriorityQueue import PQ
from MazeReport import MazeReport


#Maze Solver Algorithm using A* Algorithm Function
def astar_img(img: Image) -> Image:

    if img is None:
        raise Exception("None Image Given")

    #Variable Setup
    matrix = img_to_mat(img)

    end_points = _find_end_point_coords(matrix)
    BasicCoordinate.goal_x, BasicCoordinate.goal_y = end_points[1]
    start_coord = AStarCoordinate(end_points[0][0], end_points[0][1], "S")

    coords_yet_to_see = PQ()
    coords_yet_to_see.push(start_coord)
    coords_already_seen = []

    checked_coords = 0

    data_report = MazeReport(report_name = "A*")
    data_report.add_matrix(matrix)
    data_report.add_to_open(len(coords_yet_to_see))
    data_report.add_to_closed(len(coords_already_seen))

    neighbors_simple = [(1,0),(-1,0),(0,1),(0,-1)]

    #Searching Process Loop, Exploration Stage
    while coords_yet_to_see:

        cur_coord = coords_yet_to_see.pop()
        matrix[cur_coord.y][cur_coord.x] = "C"
        checked_coords += 1

        if cur_coord.is_goal():
            print("GOAL FOUND")
            print("Current path length: ",cur_coord.g)
            print("Checked",checked_coords,"coordinates")
            break

        #Check close neighbors to current coordinate on matrix
        for neighbor_shift in neighbors_simple:
            tmp_x = cur_coord.x + neighbor_shift[0]
            tmp_y = cur_coord.y + neighbor_shift[1]

            if matrix[tmp_y][tmp_x] == "B":
                continue

            tmp_coord = AStarCoordinate(tmp_x,tmp_y, matrix[tmp_y][tmp_x], parent=cur_coord)

            if (tmp_coord not in coords_yet_to_see) and (tmp_coord not in coords_already_seen):
                coords_yet_to_see.push(tmp_coord)

        coords_already_seen.append(cur_coord)

        #Data Reporting
        data_report.add_matrix(matrix)
        data_report.add_to_open(len(coords_yet_to_see))
        data_report.add_to_closed(len(coords_already_seen))

    else:
        print("GOAL NOT FOUND")
        raise ValueError("Path Not Found")

    
    #Retrace Path of Goal Coordinate Function
    data_report.set_path_length(cur_coord.g)

    while cur_coord is not None:

        matrix[cur_coord.y][cur_coord.x] = "P"
        cur_coord = cur_coord.parent

        data_report.add_matrix(matrix)

    matrix[end_points[0][1]][end_points[0][0]] = "S"
    matrix[end_points[1][1]][end_points[1][0]] = "F" 

    data_report.add_matrix(matrix)

    return data_report.get_data()


#Find Positions of Start and End Points Function
def _find_end_point_coords(mat: list) -> tuple:

    if mat is None:
        raise Exception("None Matrix Given")

    if not isinstance(mat[0],list):
        raise Exception("1-Dimensional List Given")

    start_coords = None
    end_coords = None

    #Checking Matrix for Specific Start and End Coordinate Symbols
    for y in range(len(mat)):
        for x in range(len(mat[0])):
            if mat[y][x] == "S":
               start_coords = (x,y)
            elif mat[y][x] == "F":
                end_coords = (x,y)

    if start_coords is None:
        raise Exception("Starting Coordinates Not Found")

    if end_coords is None:
        raise Exception("Ending Coordinates Not Found")

    return (start_coords,end_coords)

