import matplotlib.pyplot as plt
from utilities import FileReader
import numpy as np
def plot_errors():

    obstacles = np.loadtxt('obstaclesMap_2023-11-30 22:28:31.txt')
    path_cart = np.loadtxt('path_cart_2023-11-30 22:28:31.txt')
    headers, values=FileReader("robotPose_2023-11-30 22:28:19.csv").read_file()
    plt.scatter([lin[0] for lin in obstacles], [lin[1] for lin in obstacles])
    plt.scatter([lin[0] for lin in path_cart], [lin[1] for lin in path_cart])
    plt.scatter([lin[0] for lin in values], [lin[1] for lin in values])
    plt.legend()
    plt.grid()

    plt.show()
    
    

if __name__=="__main__":
    plot_errors()