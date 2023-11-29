import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
import time


class Node:
    """
        A node class for A* Pathfinding
        parent is parent of the current Node
        position is current position of the Node in the maze
        g is cost from start to current Node
        h is heuristic based estimated cost for current Node to end Node
        f is total cost of present node i.e. :  f = g + h
    """

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position
    
def heuristics(mode, current_position, end_position):
    if mode == 'euclidean':
        return sqrt((end_position[0]-current_position[0])**2 + (end_position[1]-current_position[1])**2)
    elif mode == 'manhattan':
        return abs(end_position[0]-current_position[0]) + abs(end_position[1]-current_position[1])
    else:
        print("no mode exists")
        return 0

#This function return the path of the search
def return_path(current_node,maze):
    path = []
    no_rows, no_columns = np.shape(maze)
    # here we create the initialized result maze with -1 in every position
    result = [[-1 for i in range(no_columns)] for j in range(no_rows)]
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    # Return reversed path as we need to show from start to end path
    path = path[::-1]
    start_value = 0
    # we update the path of start to end found by A-star serch with every step incremented by 1
    for i in range(len(path)):
        result[path[i][0]][path[i][1]] = start_value
        start_value += 1
    return path


def search(maze, start, end, heuristics_mode):
    """
        Returns a list of tuples as a path from the given start to the given end in the given maze
        :param maze:
        :param cost
        :param start:
        :param end:
        :return:
    """

    start_time = time.time()
    print("searching ....")
    maze = maze.T

    # TODO PART 4 Create start and end node with initized values for g, h and f
    start_node = Node(position=start)
    start_node.g = 0
    start_node.h = heuristics(heuristics_mode, start, end)
    start_node.f = start_node.g + start_node.h

    end_node = Node(position=end)
    end_node.g = 0
    end_node.h = 0
    end_node.f = 0

    # Initialize both yet_to_visit and visited list
    # in this list we will put all node that are yet_to_visit for exploration. 
    # From here we will find the lowest cost node to expand next
    yet_to_visit_list = dict() # key = position, value = node object
    # in this list we will put all node those already explored so that we don't explore it again
    visited_list = set() # set of node positions that have already been visited

    # Note that for the yet_to_visit and visited lists, we store the node position instead of the node
    # object as the dict key or set element because node position is a tuple of (x,y) that is 1) hashable
    # and 2) sufficient for checking if two nodes are equivalent.

    # Add the start node
    yet_to_visit_list[start_node.position] = start_node

    # Adding a stop condition. This is to avoid any infinite loop and stop 
    # execution after some reasonable number of steps
    outer_iterations = 0
    max_iterations = (len(maze) // 2) ** 10


    # TODO PART 4 what squares do we search . serarch movement is left-right-top-bottom 
    #(4 movements) from every positon
    x_dist = 1
    y_dist = 1
    move  =  [[0, y_dist], # go up
              [-x_dist, 0], # go left
              [0, -y_dist], # go down
              [x_dist, 0], # go right
              [-x_dist, y_dist], # go up left
              [-x_dist, -y_dist], # go down left
              [x_dist, y_dist], # go up right
              [x_dist, -y_dist]] # go down right


    """
        1) We first get the current node by comparing all f cost and selecting the lowest cost node for further expansion
        2) Check max iteration reached or not . Set a message and stop execution
        3) Remove the selected node from yet_to_visit list and add this node to visited list
        4) Perofmr Goal test and return the path else perform below steps
        5) For selected node find out all children (use move to find children)
            a) get the current postion for the selected node (this becomes parent node for the children)
            b) check if a valid position exist (boundary will make few nodes invalid)
            c) if any node is a wall then ignore that
            d) if child in visited list then ignore it and try next node
            e) calculate child node g, h and f values
            f) if child in yet_to_visit list then
                f.1) if new child has lower g value, update yet_to_visit list with new child
                f.2) else ignore it
            g) else move the child to yet_to_visit list
    """
    # TODO PART 4 find maze has got how many rows and columns 
    no_rows, no_columns = maze.shape


    # Loop until you find the end
    while len(yet_to_visit_list) > 0:
        # Every time any node is referred from yet_to_visit list, counter of limit operation incremented
        outer_iterations += 1    

        # Find the node in yet_to_visit list with the lowest f value and select it as the current node
        current_node = yet_to_visit_list.pop(min(yet_to_visit_list.items(), key=lambda x: x[1].f)[0])

        # if we hit this point return the path such as it may be no solution or 
        # computation cost is too high
        if outer_iterations > max_iterations:
            print ("giving up on pathfinding too many iterations")
            return return_path(current_node,maze)

        # test if goal is reached or not, if yes then return the path
        if current_node == end_node:
            execution_time = time.time() - start_time
            print("A* search execution time: {:.3f} s".format(execution_time))
            return return_path(current_node,maze)

        # Add current node to visited list
        visited_list.add(current_node.position)

        for new_position in move: 

            # TODO PART 4 Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # TODO PART 4 Make sure within range (check if within maze boundary)
            if node_position[0] < 0 or node_position[0] >= no_rows or node_position[1] < 0 or node_position[1] >= no_columns:
                continue

            # Make sure walkable terrain
            if maze[node_position[0],node_position[1]] > 0.8:
                continue

            # Create new node
            child = Node(current_node, node_position)

            # TODO PART 4 Child is on the visited list (search entire visited list) 
            if child.position in visited_list:
                continue

            # TODO PART 4 Create the f, g, and h values
            child.g = sqrt((current_node.position[0] - child.position[0])**2 + (current_node.position[1] - child.position[1])**2) + current_node.g
            # Heuristic costs calculated here, this is using eucledian distance
            child.h = heuristics(heuristics_mode, child.position, end_node.position)

            child.f = child.g + child.h

            if child.position in yet_to_visit_list:
                if child.g < yet_to_visit_list[child.position].g:
                    yet_to_visit_list[child.position] = child
            else:
                yet_to_visit_list[child.position] = child

    print("no path exists")
    return []
