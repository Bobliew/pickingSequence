import json
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def create_data_model(json_data, xStart, yStart):
    locations = []
    locations.append((xStart, yStart))
    for order in json_data:
        for sku in order['skuInfo']:
            locations.append((sku['xCoordAloc'], sku['yCoordAloc']))
    data = {}
    data['locations'] = locations
    data['num_vehicles'] = 1
    data['depot'] = 0
    return data

def compute_euclidean_distance_matrix(locations):
    distances = {}
    for from_counter, from_node in enumerate(locations):
        distances[from_counter] = {}
        for to_counter, to_node in enumerate(locations):
            if from_counter == to_counter:
                distances[from_counter][to_counter] = 0
            else:
                distances[from_counter][to_counter] = int(((from_node[0] - to_node[0])**2 + (from_node[1] - to_node[1])**2)**0.5)
    return distances


# def print_solution(manager, routing, solution):
#    index = routing.Start(0)
#    route_distance = 0
#    while not routing.IsEnd(index):
#        previous_index = index
#        index = solution.Value(routing.NextVar(index))
#        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
#    return route_distance

def print_solution(manager, routing, solution, xStart, yStart):
    """Prints solution on console."""
    print('起始点X坐标：{}'.format(xStart))
    print('起始点y坐标：{}'.format(yStart))
    print('最短路程: {} 米'.format(solution.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = '访问路径:\n'
    route_distance = 0
    print (routing)
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
    print(routing_map)
    # plan_output += 'Route distance: {}miles\n'.format(route_distance)
    for i in range( 1, j):
        routing_list.append(routing_map[i])
    print(routing_map)
    return routing_list

def main(json_data, xStart, yStart):
    data = create_data_model(json_data, xStart, yStart)

    manager = pywrapcp.RoutingIndexManager(len(data['locations']),
                                           data['num_vehicles'], data['depot'])

    routing = pywrapcp.RoutingModel(manager)

    distance_matrix = compute_euclidean_distance_matrix(data['locations'])

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        route_list = print_solution(manager, routing, solution, xStart, yStart)
        i = 0
        for item1 in json_data:
            for item2 in item1["skuInfo"]:
                item2["pickingSequence"] = route_list[i]
                i+=1
        print(f'handled Json data: {json_data}')
        return json_data
    else:
        print('No solution found.')

async def runmain(raw_data, xStart, yStart):
    tasks = []
    for item in raw_data["batchInfo"]:
        tasks.append(main(item["orderInfo"], xStart, yStart))
    result = await asyncio.gather(*tasks) # 需要在这之后重新整合为一个
    for i in range(len(raw_data["batchInfo"])):
        raw_data["batchInfo"][i]["orderInfo"] = result[i]
    return raw_data
        


if __name__ == '__main__':
    input_json = """
                [
                    {
                        "orderCode":"ORD001",
                        "skuInfo":[
                            {
                                "skuCode":"SKU001",
                                "allocateLocation": "LOC001",
                                "xCoordAloc":10.4,
                                "yCoordAloc":9.6,
                                "allocateAmount":1
                            },
                            {
                                "skuCode":"SKU002",
                                "allocatieLocation": "LOC002",
                                "xCoordAloc":11.4,
                                "yCoordAloc":9.6,
                                "allocateAmount":3
                            }
                        ]
                    },
                    {
                        "orderCode":"ORD002",
                        "skuInfo":[
                            {
                                "skuCode":"SKU001",
                                "allocateLocation": "LOC001",
                                "xCoordAloc":10.4,
                                "yCoordAloc":9.6,
                                "allocateAmount":3
                            },
                            {
                                "skuCode":"SKU002",
                                "allocateLocation": "LOC002",
                                "xCoordAloc":11.4,
                                "yCoordAloc":9.6,
                                "allocateAmount":3
                            }
                        ]
                    }
                ]
    """
    json_data = json.loads(input_json)
    main(json_data, 0, 0)
