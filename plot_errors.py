import matplotlib.pyplot as plt
from utilities import FileReader
plt.rcParams.update({'font.size':14})



def plot_errors(filename):
    
    headers, values=FileReader(filename).read_file()
    
    time_list=[]
    
    first_stamp=values[0][-1]
    
    for val in values:
        time_list.append(val[-1] - first_stamp)

    
    
    fig, axes = plt.subplots(2,2)
    fig.tight_layout()
    fig.suptitle('Spiral Q=0.5 R=0.1')
    axes[0][0].plot([lin[len(headers) - 5] for lin in values], [lin[len(headers) - 4] for lin in values])
    axes[0][0].set_title("state space")
    axes[0][0].set_xlabel('X (m)')
    axes[0][0].set_ylabel('Y (m)')
    axes[0][0].grid()

    
    axes[0][1].set_title("IMU")
    for i in range(0, 4):
        axes[0][1].plot(time_list, [lin[i] for lin in values], label= headers[i])

    axes[0][1].set_xlabel('Time (ns)')
    axes[0][1].legend()
    axes[0][1].grid()

    axes[1][0].set_title("V and W")
    for i in range(4, 8):
        axes[1][0].plot(time_list, [lin[i] for lin in values], label= headers[i])

    axes[1][0].set_xlabel('Time (ns)')
    axes[1][0].legend()
    axes[1][0].grid()

    axes[1][1].set_title("X and Y and Theta")
    for i in range(8, 14):
        axes[1][1].plot(time_list, [lin[i] for lin in values], label= headers[i])

    axes[1][1].set_xlabel('Time (ns)')
    axes[1][1].legend()
    axes[1][1].grid()

    plt.show()
    
    





import argparse

if __name__=="__main__":

    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('--files', nargs='+', required=True, help='List of files to process')
    
    args = parser.parse_args()
    
    print("plotting the files", args.files)

    filenames=args.files
    for filename in filenames:
        plot_errors(filename)


