"""
animate_pathfinding.py

By: Reid Smith

Description:
    -Part of the Semester Final Project for CS3
    -This file will be the main file for handling the visual animation aspects of a chosen pathfinding algorithm on a PyGame Screen


TODO:
    -Set Up PyGame Screen -
"""

import pygame
import sys
import ImageConvert
from PIL import Image
from animated_bfs import bfs_img
from animated_astar import astar_img
from animated_dfs import dfs_img
from time import sleep
from matplotlib import pyplot as plt

#Function to gather animation parameters from user to return input w/ error checking
def _get_animation_parameters():

    print("\tGathering Animation Parameters:\n--------------------------------------------------")

    scrn_height = 0
    scrn_width = 0

    is_automatic = None
    time_delay = None

    alg_choice = None

    has_maze = None
    maze_choice = None

    show_graph = None
    save_graph = None
    
    #Error Checking Input
    while scrn_height < 100:
        try:
            scrn_height = int(input("Enter a starting HEIGHT ( >= 100 ) for the screen to animate in: "))
        except ValueError:
            print("Please enter an integer for the screen HEIGHT. Try again.")

    print()

    while scrn_width < 100:
        try:
            scrn_width = int(input("Enter a starting WIDTH ( >= 100 ) for the screen to animate in: "))
        except ValueError:
            print("Please enter an integer for the screen WIDTH. Try again.")

    print()

    while time_delay is None or not (0 < time_delay <= 2.5):
        try:
            time_delay = float(input("Enter a TIME DELAY ( >0 & <= 2.5 )for waiting between steps of algorithm: "))
        except ValueError:
            print("Please enter a real number. Try again.")

    print()


    print("Avaliable Algorithms To Animate:\n\t1.BFS\n\t2.DFS\n\t3.A*\n")

    while alg_choice is None or not (1 <= alg_choice <= 3):
        try:
            alg_choice = int(input("Enter ALGORITHM # (1-3) to animate in screen: "))
        except ValueError:
            print("Please enter an integer for the ALGORITHM #. Try again.")

    print()

    maze_choice = input("Enter NAME of Image Maze File to be used from TestMazes Directory: ")

    maze_choice = "../TestMazes/"+maze_choice

    print()
    
    while show_graph is None:
        graph_choice = input("Enter whether algorithm should DISPLAY GRAPH of performance? (Yes/No): ").strip().lower()[0]

        if graph_choice == "y":
            show_graph = True
        elif graph_choice == "n":
            show_graph = False
        else:
            print("Please enter \'Yes\' or \'No\'. Try Again.")
    
    if show_graph:
        while save_graph is None:
            graph_choice = input("Enter whether algorithm should SAVE DATA of performance? (Yes/No): ").strip().lower()[0]

            if graph_choice == "y":
                save_graph = True
            elif graph_choice == "n":
                save_graph = False
            else:
                print("Please enter \'Yes\' or \'No\'. Try Again.")

        print()

    #print(scrn_height,scrn_width,is_automatic,time_delay,alg_choice,has_maze)

    return (scrn_height, scrn_width, "Deprecated IsAutomatic Variable Placeholder", time_delay, alg_choice, "Deprecated HasMaze Variable PlaceHolder", maze_choice, show_graph, save_graph)


#Function to update pygame screen with given matrix
def _update_screen(screen, matrix: list):
    """
    Avaliable variables:

        -How wide the screen is (screen.get_width())
        -How long the screen is (screen.get_height())
        -How many coords are in a row (len(matrix[0]))
        -How many coords are in a column (len(matrix))
        -
    """
    edge_buffer = 20

    between_spaces = 0 

    space_width = int( (screen.get_width() - 2 * edge_buffer - between_spaces * (len(matrix[0]) - 1) ) / len(matrix[0]) )

    space_height = int( (screen.get_height() - 2 * edge_buffer - between_spaces * (len(matrix) - 1)) / len(matrix) )

    screen.fill((238,255,204))

    for x in range(len(matrix[0])):
        for y in range(len(matrix)):

            tmp_col = ImageConvert._sym_to_pix(matrix[y][x])
            color = (tmp_col[0], tmp_col[1], tmp_col[2])

            space_x = edge_buffer + x * (space_width + between_spaces)
            space_y = edge_buffer + y * (space_height + between_spaces)

            pygame.draw.rect(screen, color, (space_x, space_y, space_width,space_height ))
            #pygame.draw.rect(screen, (0,0,0), (space_x, space_y, space_width,space_height), 1) 


#Function to Animate Maze and display graphs
"""
Get Parameters

Call Animated Version of Algorithm

    -Create Matrix Buffer
    -Everytime there's a change, add the current matrix to the buffer
    -run as normal otherwise
    -Return Matrix Buffer at End


"""
def animate_maze():
    #Contains list of user parameters [screen height, screen width, if maze is automatic, time delay if so, algorithm choice, if already has maze, maze image path] 
    param_list = _get_animation_parameters()

    time_delay = param_list[3]

    image = Image.open("../TestMazes/" + param_list[6])

    alg_choice = param_list[4]

    if alg_choice == 1:
        maze_report = bfs_img(image)
    elif alg_choice == 2:
        maze_report = dfs_img(image)
    elif alg_choice == 3:
        maze_report = astar_img(image)

    matrix_buffer = maze_report["matrix buffer"]

    #Show Final Image
    #ImageConvert.mat_to_img(matrix_buffer[-1]).show()
    pygame.init()

    screen = pygame.display.set_mode((param_list[0],param_list[1]))
    running = True
    start = False

    #Running the Animation
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start = True   
        
        if start:
            current_matrix = matrix_buffer.pop(0)

            if matrix_buffer == []:
                start = False

            _update_screen(screen, current_matrix)
            pygame.display.update()
            pygame.time.delay(int(time_delay * 1000))

    #If Chose to Show Graph
    if param_list[-2]:
       open_set = maze_report["open set"]
       closed_set = maze_report["closed set"]
       plt.plot(list(range(len(open_set))),open_set, label = "Open Set Size")
       plt.plot(list(range(len(closed_set))), closed_set, label = "Closed Set Size")
       plt.ylabel("Size of Set")
       plt.xlabel("Algorithm Step #")
       plt.title("Running "+maze_report["name"])
       plt.legend()

       #If Chose to Save the Graph
       if param_list[-1]:
           plt.savefig("MazeReport Graph: "+maze_report["name"]+" on "+param_list[6][13:])
       plt.show()

    pygame.quit()
    pass
    

     
#If Statement to make Main Function to run when file is directly executed
if __name__ == "__main__":
    animate_maze()

    
