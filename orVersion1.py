import json
import time
import asyncio
from strategyOrtool.ortoolTSP import *
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

# 异步对每个集单进行计算
async def singleMain(json_data, xStart, yStart):
    # 调用create_data_model()函数;
    data = create_data_model(json_data, xStart, yStart)
    # 创建
    manager = pywrapcp.RoutingIndexManager(len(data['locations']),
                                           data['num_vehicles'], data['depot'])

    routing = pywrapcp.RoutingModel(manager)
    # 调用compute_Manhattan_distance_matrix()函数生成距离矩阵
    distance_matrix = compute_Manhattan_distance_matrix(data['locations'])
    # 在main中，定义
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

        # 将生成的数据导入到原来的json数据集中
        for item1 in json_data:
            for item2 in item1["skuInfo"]:
                item2["pickingSequence"] = route_list[i]
                i+=1
        print(f'handled Json data: {json_data}')
        print(route_list)

        return json_data
    else:
        print('No solution found.')

async def runMain(raw_data, xStart, yStart):
    tasks = []
    semaphore = asyncio.Semaphore(10)
    for item in raw_data["batchInfo"]:
        tasks.append(singleMain(item["outOrderInfo"], xStart, yStart))
    result = await asyncio.gather(*tasks) # 需要在这之后重新整合为一个
    for i in range(len(raw_data["batchInfo"])):
        raw_data["batchInfo"][i]["outOrderInfo"] = result[i]
    return raw_data
        


if __name__ == '__main__':
    start_time = time.time()
    f = open('./quickStart/output.json', 'r')
    content = f.read()
    a = json.loads(content)
    f.close()
    inputData = json.loads(a)
    #print(type(inputData))
    result = asyncio.run(runMain(inputData, 0, 0))
    end_time = time.time()  # 记录程序结束时间
    print("\n 最终结果：\n")
    print("{}".format(result))
    elapsed_time = end_time - start_time
    print("计算时间为：{}秒".format(elapsed_time))

