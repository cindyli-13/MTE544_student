import matplotlib.pyplot as plt
from utilities import FileReader
import numpy as np
def plot_errors():

    obstacles = np.loadtxt('obstaclesMap_2023-12-01 10:41:27.txt')
    path_cart = np.loadtxt('path_cart_2023-12-01 10:41:27.txt')
    path_cell = np.loadtxt('path_cell_2023-12-01 10:41:27.txt')
    imageArray = np.loadtxt('imageArray.txt')
    headers, values=FileReader("robotPose_2023-11-30 22:28:19.csv").read_file()
    plt.imshow(imageArray, cmap='gray')
    # plt.scatter([lin[0] for lin in obstacles], [lin[1] for lin in obstacles])
    plt.scatter(path_cell[0][0], path_cell[0][1])
    plt.scatter(path_cell[-1][0], path_cell[-1][1])
    plt.plot([lin[0] for lin in path_cell], [lin[1] for lin in path_cell])
    # plt.plot([lin[0] for lin in values], [lin[1] for lin in values])
    plt.legend()
    plt.grid()

    plt.show()
    
    

if __name__=="__main__":
    plot_errors()