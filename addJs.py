import asyncio
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
import math

def create_data_model(json_data, xStart, yStart):
    """Stores the data for the problem."""
    data = {}
    locations = []
    demands = []
    vehicle_capacities = []
    num_vehicles = 1
    depot = 0
    json_data = eval(json_data)

    locations.append((xStart, yStart))
    demands.append(0)
    vehicle_capacities.append(1000)

    for order in json_data:
        for sku in order['skuInfo']:
            locations.append((sku['xCoordAloc'], sku['yCoordAloc']))
            demands.append(sku['allocateAmount'])
            vehicle_capacities.append(1000)

    data['locations'] = locations
    data['num_vehicles'] = num_vehicles
    data['depot'] = depot
    data['demands'] = demands
    data['vehicle_capacities'] = vehicle_capacities

    return data


def compute_euclidean_distance_matrix(locations):
    """Creates callback to return distance between points."""
    distances = {}
    for from_counter, from_node in enumerate(locations):
        distances[from_counter] = {}
        for to_counter, to_node in enumerate(locations):
            if from_counter == to_counter:
                distances[from_counter][to_counter] = 0
            else:
                # Euclidean distance
                distances[from_counter][to_counter] = math.sqrt(
                    ((from_node[0] - to_node[0]) ** 2) + ((from_node[1] - to_node[1]) ** 2))
    return distances


async def run_tasks():
    input_json_1 = """
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
    input_json_2 = """
                [
                    {
                        "orderCode":"ORD001",
                        "skuInfo":[
                            {
                                "skuCode":"SKU001",
                                "allocateLocation": "LOC001",
                                "xCoordAloc":10.4,
                                "yCoordAloc":9.6,
                                "allocateAmount":2
                            },
                            {
                                "skuCode":"SKU002",
                                "allocatieLocation": "LOC002",
                                "xCoordAloc":11.4,
                                "yCoordAloc":9.6,
                                "allocateAmount":1
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
                                "allocateAmount":2
                            }
                        ]
                    }
                ]
    """
    tasks = []
    tasks.append(asyncio.create_task(main(input_json_1, 10.5, 9.5)))
    tasks.append(asyncio.create_task(main(input_json_2, 10.5, 9.5)))
    await asyncio.gather(*tasks)


async def main(json_data, xStart, yStart):
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model(json_data, xStart, yStart)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['locations']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Define cost of each arc.
    distance_matrix = compute_euclidean_distance_matrix(data['locations'])

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Capacity constraint.
    def demand_callback(from_index):
        """Returns the demand of the node."""
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        return print_solution(manager, routing, solution)


def print_solution(manager, routing, solution):
    """Prints solution on console."""
    max_route_distance = 0
    for vehicle_id in range(routing.GetNumberOfVehicles()):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            plan_output += ' {0} -> '.format(node_index)
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
        node_index = manager.IndexToNode(index)
        plan_output += ' {0}\n'.format(node_index)
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        print(plan_output)
        max_route_distance = max(route_distance, max_route_distance)
    print('Maximum distance of all routes: {}m'.format(max_route_distance))


if __name__ == '__main__':
    asyncio.run(run_tasks())
