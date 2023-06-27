import matplotlib.pyplot as plt

def tspVisualization(xStart, yStart, route_list, data):       # 可视化
    depot_coor = (xStart, yStart)
    plt.plot(depot_coor[0], depot_coor[1], 'r*')
    routeList = [0]
    routeList+=route_list
    # 通过遍历routeList,将点和连线进行可视化
    for i in range(0,len(routeList)-1):
        start_coor = data['locations'][routeList[i]]
        end_coor = data['locations'][routeList[i+1]]
        plt.arrow(start_coor[0], start_coor[1], end_coor[0] - start_coor[0], end_coor[1] - start_coor[1])
    
    # 将终点与depot相连
    start_coor = data['locations'][routeList[i]]
    end_coor = data['locations'][routeList[i+1]]
    plt.arrow(start_coor[0], start_coor[1], end_coor[0] - start_coor[0], end_coor[1] - start_coor[1])
    plt.xlabel("X coordinate", fontsize = 14)
    plt.ylabel("Y coordinate", fontsize = 14)
    plt.title("TSP path for orTest", fontsize = 16)
    plt.show()
