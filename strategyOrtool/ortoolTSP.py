import json
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

# orVersion1 出于对计算性能的考虑是没有进行可视化的；

def create_data_model(json_data, xStart, yStart):
    locations = []
    # 添加depot点，因为传进来的orderInfo是只有sku的x，y坐标，没包含depot点的坐标的；
    locations.append((xStart, yStart))
    # 添加x，y坐标点到locations列表中；
    for order in json_data:
        for sku in order['skuInfo']:
            locations.append((sku['xCoordAloc'], sku['yCoordAloc']))
    # Ortools计算所需的数据；
    data = {}
    # 需要抵达的sku点；
    data['locations'] = locations
    # 单个集单车辆数；
    data['num_vehicles'] = 1
    # depot点为locations列表中第一个点；
    data['depot'] = 0
    print(data['locations'])
    # 返回depot点坐标
    return data

def compute_Manhattan_distance_matrix(locations):
    # 计算两点之间的曼哈顿距离<F6>
    distances = {}
    for from_counter, from_node in enumerate(locations):
        # from_counter是下标 to_counter是下标；
        # from_node是对应值，to_node是对应值；
        distances[from_counter] = {}
        for to_counter, to_node in enumerate(locations):
            # 如果对应下标相同，则距离为0；
            # 否则计算曼哈顿距离，并存回距离矩阵；
            if from_counter == to_counter:
                distances[from_counter][to_counter] = 0
            else:
                distances[from_counter][to_counter] = int(abs(from_node[0] - to_node[0]) + abs(from_node[1] - to_node[1]))
    # 注意，在orVersion1(1.2.9)中，是没有考虑障碍物的约束的，因此只以曼哈顿距离，
    # 作为衡量标准；
    return distances


# def print_solution(manager, routing, solution):
#    index = routing.Start(0)
#    route_distance = 0
#    while not routing.IsEnd(index):
#        previous_index = index
#        index = solution.Value(routing.NextVar(index))
#        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
#    return route_distance

# 完成求解后，负责将结果进行输出的函数；
def print_solution(manager, routing, solution, xStart, yStart):
    """Prints solution on console."""
    print('\n \n起始点X坐标：{}'.format(xStart))
    print('起始点y坐标：{}'.format(yStart))
    print('路程估算: {} 米'.format(solution.ObjectiveValue()/1000))
    index = routing.Start(0)
    plan_output = '访问路径:\n'
    route_distance = 0
    #print (routing)
    routing_list = []
    routing_map = {}
    j = 0
    
    while not routing.IsEnd(index):
        plan_output += ' {} ->'.format(manager.IndexToNode(index))
        routing_map[index] = j
        j += 1
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += ' {}\n'.format(manager.IndexToNode(index))
    print(plan_output)
    del routing_map[0]
    #print(routing_map)
    # plan_output += 'Route distance: {}miles\n'.format(route_distance)
    for i in range( 1, j):
        routing_list.append(routing_map[i])
    #print(routing_map)
    print(routing_list)
    return routing_list

