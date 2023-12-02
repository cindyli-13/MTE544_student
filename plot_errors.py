import matplotlib.pyplot as plt
from utilities import FileReader
import numpy as np
def plot_errors():


    path_cell_1 = np.loadtxt('path_cell_2023-12-01 15_18_09_KF_InLab_Run1.txt')

    path_cell_2 = np.loadtxt('path_cell_2023-12-01 15_18_56_KF_InLab_Run2.txt')

    imageArray = np.loadtxt('imageArray.txt')

    plt.imshow(imageArray, cmap='gray')

    plt.scatter(path_cell_1[0][0], path_cell_1[0][1], label='Start Point 1', color='r')
    plt.scatter(path_cell_1[-1][0], path_cell_1[-1][1], label='Intermediate Point', color='c')
    plt.plot([lin[0] for lin in path_cell_1], [lin[1] for lin in path_cell_1])

    plt.scatter(path_cell_2[0][0], path_cell_2[0][1], color='c')
    plt.scatter(path_cell_2[-1][0], path_cell_2[-1][1], label='End Point 2', color='y')

    plt.plot([lin[0] for lin in path_cell_2], [lin[1] for lin in path_cell_2])
    plt.title('Ideal Path Trajectory')

    
    plt.legend()
    plt.grid()

    plt.show()
    
    

if __name__=="__main__":
    plot_errors()