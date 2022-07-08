"""
Maze Image Solver using Depth First Search Algorithm Module
By: Reid Smith

Notes:
    -Newly written iterative DFS algorithm that reports data on the algorithm process in order to be animated
Purpose:

"""
from PIL import Image
from Coordinates import BasicCoordinate
from ImageConvert import *
from MazeReport import MazeReport

#Maze Solver Algorithm using DFS Algorithm Function
def dfs_img(img: Image) -> Image:

    if img is None:
        raise Exception("None Image Given")

    #Variable Setup
    matrix = img_to_mat(img)

    end_points = _find_end_point_coords(matrix)
    BasicCoordinate.goal_x, BasicCoordinate.goal_y = end_points[1]
    start_coord = BasicCoordinate(end_points[0][0], end_points[0][1], "S")

    yet_to_see = [start_coord]
    already_seen = []

    checked_coords = 0

    data_report = MazeReport(report_name = "DFS")
    data_report.add_matrix(matrix)
    data_report.add_to_open(1) #Known length of open set
    data_report.add_to_closed(0) #Known length of closed set

    neighbors = [(1,0),(-1,0),(0,1),(0,-1)]

    #Pathfinding Loop that explores the Matrix
    while yet_to_see:

        cur_coord = yet_to_see.pop()
        matrix[cur_coord.y][cur_coord.x] = "C"
        checked_coords += 1

        if cur_coord.is_goal():
            print("GOAL FOUND")
            print("Current path length: ",cur_coord.count)
            print("Checked",checked_coords,"coordinates")
            break

        #Check Neighbors of current coordinate
        for neighbor in neighbors:
            tmp_x = cur_coord.x + neighbor[0]
            tmp_y = cur_coord.y + neighbor[1]

            if matrix[tmp_y][tmp_x] == "B":
                continue

            tmp_coord = BasicCoordinate(tmp_x, tmp_y, matrix[tmp_y][tmp_x], parent=cur_coord)

            if (tmp_coord not in yet_to_see) and (tmp_coord not in already_seen):
                yet_to_see.append(tmp_coord)

        already_seen.append(cur_coord)

        #Data Reporting
        data_report.add_matrix(matrix)
        data_report.add_to_open(len(yet_to_see))
        data_report.add_to_closed(len(already_seen))

    else:
        print("GOAL NOT FOUND")
        raise ValueError("Path Not Found")

    data_report.set_path_length(cur_coord.count)

    while cur_coord is not None:

        matrix[cur_coord.y][cur_coord.x] = "P"
        cur_coord = cur_coord.parent

        data_report.add_matrix(matrix)
    
    matrix[end_points[0][1]][end_points[0][0]] = "S"
    matrix[end_points[1][1]][end_points[1][0]] = "F"

    data_report.add_matrix(matrix)

    return data_report.get_data()


#Find End Point Positions Function
def _find_end_point_coords(mat: list) -> tuple:

    if mat is None:
        raise Exception("None Matrix Given")

    start_coords = None
    end_coords = None

    #Find Specific Start and End Points on Matrix
    for y in range(len(mat)):
        for x in range(len(mat[0])):
            if mat[y][x] == "S":
                start_coords = (x,y)
            elif mat[y][x] == "F":
                end_coords= (x,y)
    
    if start_coords is None:
        raise Exception("Starting Coordinates Not Found")

    if end_coords is None:
        raise Exception("Ending Coordinates Not Found")

    return (start_coords, end_coords)


   















