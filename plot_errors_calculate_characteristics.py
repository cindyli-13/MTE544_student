import matplotlib.pyplot as plt
from utilities import FileReader
plt.rcParams.update({'font.size': 18})

def removeColumns(list, cols, header=False):
    for col in cols:
        if header:
            del list[col]
        else:
            for row in list:
                del row[col]

    return list

def calculateOvershoot(list):
    # first value
    firstValue = list[0][0]
    # check for largest value on other side of 0
    if firstValue < 0:
        overshoot = -1000 # arbitrary large neg
        for val in list:
            if val[0] > overshoot:
                overshoot = val[0]
        if overshoot < 0:
            overshoot = 0
    else: 
        overshoot = 1000 # arbitrary large pos
        for val in list:
            if val[0] < overshoot:
                overshoot = val[0]
        if overshoot > 0:
            overshoot = 0
    
    return overshoot/firstValue*100

def calculateAgility(list, timeList):
    firstValue = list[0][0]
    # find the 63% point
    agileValue = (1-0.63)*firstValue
    index = -2
    if firstValue < 0:
        for i in range(len(list)):
            if (list[i][0] > agileValue):
                index = i
                break
    else:
        for i in range(len(list)):
            if (list[i][0] < agileValue):
                index = i
                break

    if index == -2:
        return 0
    else:
        return timeList[i]/1e9
    

def plot_errors(filename):
    
    headersUntuned, valuesUntuned=FileReader('linear_Part4PController.csv').read_file()
    headersTuned, valuesTuned=FileReader('linear_Part4PControllerTuned.csv').read_file()
    headersUntunedAng, valuesUntunedAng=FileReader('angular_Part4PController.csv').read_file()
    headersTunedAng, valuesTunedAng=FileReader('angular_Part4PControllerTuned.csv').read_file()
    
    time_listUntuned=[]
    
    first_stamp=valuesUntuned[0][-1]
    
    for val in valuesUntuned:
        time_listUntuned.append(val[-1] - first_stamp)

    first_stamp=valuesTuned[0][-1]
    time_listTuned = []
    for val in valuesTuned:
        time_listTuned.append(val[-1] - first_stamp)   

    first_stamp=valuesUntunedAng[0][-1]
    time_listUntunedAng = []
    for val in valuesUntunedAng:
        time_listUntunedAng.append(val[-1] - first_stamp)

    first_stamp=valuesTunedAng[0][-1]
    time_listTunedAng = []
    for val in valuesTunedAng:
        time_listTunedAng.append(val[-1] - first_stamp)

    # calculate overshoot
    print("Overshoot Linear Untuned: " + str(calculateOvershoot(valuesUntuned)))
    print("Overshoot Linear Tuned: " + str(calculateOvershoot(valuesTuned)))
    print("Overshoot Angular Untuned: " + str(calculateOvershoot(valuesUntunedAng)))
    print("Overshoot Angular Tuned: " + str(calculateOvershoot(valuesTunedAng)))

    # calculate agility
    print("Agility Linear Untuned: " +str(calculateAgility(valuesUntuned, time_listUntuned)))
    print("Agility Linear Tuned: " +str(calculateAgility(valuesTuned, time_listTuned)))
    print("Agility Angular Untuned: " +str(calculateAgility(valuesUntunedAng, time_listUntunedAng)))
    print("Agility Angular Tuned: " +str(calculateAgility(valuesTunedAng, time_listTunedAng)))

    # calculate steady state error
    print("ess Linear Untuned: " + str(valuesUntuned[-1][0]))
    print("ess Linear Tuned: " + str(valuesTuned[-1][0]))
    print("ess Angular Untuned: " + str(valuesUntunedAng[-1][0]))
    print("ess Angular Tuned: " + str(valuesTunedAng[-1][0]))

    figA, ((axA1, axA2), (axA3, axA4)) = plt.subplots(2,2)    
    figB, ((axA5, axA7), (axA6, axA8)) = plt.subplots(2,2)
    axA1.set_title("Untuned Linear P Controller")
    for i in range(0, len(headersUntuned) -1 ):
        axA1.plot(time_listUntuned, [lin[i] for lin in valuesUntuned], label=headersUntuned[i]+" linear")
    axA1.set_ylabel('Error e[m] e_dot[m/s] e_int [m*s]' )
    axA1.set_xlabel('Time (ns)')
    axA1.set_ylim(-0.4, 2.5)
    axA1.legend()
    axA1.grid()

    axA3.set_title("Tuned Linear P Controller")
    for i in range(0, len(headersTuned) -1 ):
        axA3.plot(time_listTuned, [lin[i] for lin in valuesTuned], label=headersTuned[i]+" linear")
    axA3.set_ylabel('Error e[m] e_dot[m/s] e_int [m*s]')
    axA3.set_xlabel('Time (ns)')
    axA3.set_ylim(-0.4, 2.5)
    axA3.legend()
    axA3.grid()

    axA2.set_title("Untuned Angular P Controller")
    for i in range(0, len(headersUntunedAng) -1 ):
        axA2.plot(time_listUntuned, [lin[i] for lin in valuesUntunedAng], label=headersUntunedAng[i]+" angular")
    axA2.set_ylabel('Error e[rad] e_dot[rad/s] e_int [rad*s]')
    axA2.set_xlabel('Time (ns)')
    axA2.set_ylim(-1.2, 0.7)
    axA2.legend()
    axA2.grid()

    axA4.set_title("Tuned Angular P Controller")
    for i in range(0, len(headersTunedAng) -1 ):
        axA4.plot(time_listTunedAng, [lin[i] for lin in valuesTunedAng], label=headersTunedAng[i]+" angular")
    axA4.set_ylabel('Error e[rad] e_dot[rad/s] e_int [rad*s]')
    axA4.set_xlabel('Time (ns)')
    axA4.set_ylim(-1.2, 0.7)
    axA4.legend()
    axA4.grid()

    axA5.set_title("Untuned P Controller e vs. e_dot linear")
    axA5.plot([lin[0] for lin in valuesUntuned], [lin[1] for lin in valuesUntuned])
    axA5.set_ylabel('e_dot [m/s]')
    axA5.set_xlabel('e [m]')
    axA5.set_ylim(-0.3, 0)
    axA5.set_xlim(0, 2.5)
    axA5.legend()
    axA5.grid()

    axA6.set_title("Tuned P Controller e vs. e_dot linear")
    axA6.plot([lin[0] for lin in valuesTuned], [lin[1] for lin in valuesTuned])
    axA6.set_ylabel('e_dot [m/s]')
    axA6.set_xlabel('e [m]')
    axA6.set_ylim(-0.3, 0)
    axA6.set_xlim(0, 2.5)
    axA6.legend()
    axA6.grid()

    axA7.set_title("Untuned P Controller e vs. e_dot angular")
    axA7.plot([lin[0] for lin in valuesUntunedAng], [lin[1] for lin in valuesUntunedAng])
    axA7.set_ylabel('e_dot [rad/s]')
    axA7.set_xlabel('e [rad]')
    axA7.set_ylim(-0.2, 0.5)
    axA7.set_xlim(-1, 0.8)
    axA7.legend()
    axA7.grid()

    axA8.set_title("Tuned P Controller e vs. e_dot angular")
    axA8.plot([lin[0] for lin in valuesTunedAng], [lin[1] for lin in valuesTunedAng])
    axA8.set_ylabel('e_dot [rad/s]')
    axA8.set_xlabel('e [rad]')
    axA8.set_ylim(-0.2, 0.5)
    axA8.set_xlim(-1, 0.8)
    axA8.legend()
    axA8.grid()



    plt.show()
    
    





import argparse

if __name__=="__main__":

    plot_errors('')



