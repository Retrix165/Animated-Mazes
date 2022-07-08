"""
Animated Breadth First Search
By: Reid Smith

Notes:

Purpose:
    -To implement the Breadth First Search algorithm and create a data report that can be used in the Animate Pathfind project

"""
from PIL import Image
from ImageConvert import *
from Coordinates import BasicCoordinate
from copy import deepcopy
from MazeReport import MazeReport

sur_nodes = [(-1,0),(0,-1),(0,1),(1,0)]

#Function to run BFS
def bfs_img(img: Image) -> Image:

    #INTIAL SETUP OF MATRIX AND LISTS
    matrix = img_to_mat(img)
    start, goal = find_start_end(matrix)
    yet_to_see = []
    already_seen = []
    yet_to_see.append(BasicCoordinate(start[1],start[0],"S"))
    goal_node = None
    BasicCoordinate.goal_x = goal[1]
    BasicCoordinate.goal_y = goal[0]
    data_report = MazeReport(report_name = "BFS")
    data_report.add_matrix(matrix)
    data_report.add_to_open(len(yet_to_see))
    data_report.add_to_closed(len(already_seen))

    #BFS LOOP

    #While there are nodes left to check
    while yet_to_see:

        #pop first node in 'queue' of yet to see nodes
        cur_node = yet_to_see.pop(0)

        #flag to break search if goal is found
        found = False


        #check surrounding nodes to add to yet to see list
        for r in sur_nodes:
            t_y = cur_node.y + r[0]
            t_x = cur_node.x + r[1]

            #Check if node is valid space and not already seen by program
            if matrix[t_y][t_x] != 'B' and not check_seen_coord(t_y,t_x,yet_to_see,already_seen):
                    tmp_node = BasicCoordinate(t_x,t_y,matrix[t_y][t_x], parent=cur_node)
                    yet_to_see.append(tmp_node)
                    #add to matrix buffer here once have a color set up for open_set coords

                    #Remember goal node when found
                    if tmp_node.is_goal():
                        goal_node = tmp_node
                        matrix[t_y][t_x] = 'P'
                        found = True

        #Mark seen node on matrix OPTIONAL
        matrix[cur_node.y][cur_node.x] = 'C'


        if found:
            break

        #add seen node to already seen list
        already_seen.append(cur_node)
        
        #Data Reporting
        data_report.add_matrix(matrix)
        data_report.add_to_open(len(yet_to_see))
        data_report.add_to_closed(len(already_seen))

    #ENDING GRAPHICS CODE

    #Mark path from goal_node
    if goal_node is not None:
        print("Path found in "+str(goal_node.count)+" steps.")
        data_report.set_path_length(goal_node.count)

    else:
        print("Didn't find path to goal node!")

    while goal_node is not None:
        matrix[goal_node.y][goal_node.x] = 'P'
        goal_node = goal_node.parent

        #Add to Matrix Buffer
        data_report.add_matrix(matrix)

    #Mark start and end nodes
    matrix[start[0]][start[1]] = 'S'
    matrix[goal[0]][goal[1]] = 'F'

    data_report.add_matrix(matrix)

    return data_report.get_data() 

#Function to return the positions of the start and end coordinates
def find_start_end(matrix: list) -> list:
    out = [None,None]
    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            if matrix[y][x] == 'S':
                out[0] = (y,x)
            if matrix[y][x] == 'F':
                out[1] = (y,x)
    if out[0] is None or out[1] is None:
        print("Could not find Start/End")
    return out

#Function to check if coordinate given is already processed or in processing
def check_seen_coord(y:int, x:int, open_set: list, closed_set: list) -> bool:
    tmp_coord = BasicCoordinate(x,y,None)
    return (tmp_coord in open_set) or (tmp_coord in closed_set)



#""" Testing Code
def main():
    testImage = Image.open("../TestMazes/TestMaze2.png")
    m_buff = bfs_img(testImage)
    mat_to_img(m_buff[-1]).show()

if __name__ == "__main__":
    main()

#"""End of Testing Code
