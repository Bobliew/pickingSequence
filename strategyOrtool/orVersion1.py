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
    # 创建RoutingIndexManager，par1:节点数量 par2:车的数量 par3:起始点和终点
    manager = pywrapcp.RoutingIndexManager(len(data['locations']),
                                           data['num_vehicles'], data['depot'])
    # 根据manager参数创建RoutingModel
    routing = pywrapcp.RoutingModel(manager)
    # 调用compute_Manhattan_distance_matrix()函数生成两点之间的距离矩阵
    distance_matrix = compute_Manhattan_distance_matrix(data['locations'])
    # 在main中，定义了callback函数，但在我们这里，callback返回的值就是两点之间的曼哈顿距离
    def distance_callback(from_index, to_index):
        # 将routing model中的节点索引转换为对应的节点编号
        # 该函数作用就是返回两点之间的距离，后续的RegisterTransitCallback会使用；
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]
    # 该函数利用了distance_callback需要用户定义的性质，增加了策略的可拓展性，
    # 例如，如果两点之间的代价不用距离，可以用时间来确定，可以在distance_callback，
    # 进行对应的修改。
    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    # 车辆的行驶成本，实际上仍然是曼哈顿距离；
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    # 路径搜索初始可行解的策略为PATH_CHEAPEST_ARC
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    # 如果不指定局部搜索策略，ortools会自动采用默认的启发式策略，
    # 经过测试，结果是较为类似的，且计算耗时会下降较多，因为如果需要指定局部搜索
    # 策略，就需要定义limit.seconds，无法及时停止；
    #search_parameters.local_search_metaheuristic = (
    #    routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    #search_parameters.time_limit.seconds = 1
    #search_parameters.log_search = True

    # 调用SolveWithParameters()函数，基于search_parameter求解路径规划问题
    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        # 解析求解结果并生成路径列表, 
        # 调用print_solution打印结果, 同时print_solution会返回对应拣货顺序的列表
        route_list = print_solution(manager, routing, solution, xStart, yStart)
        i = 0
        # 将生成的数据导入到原来的json数据集中
        for item1 in json_data:
            for item2 in item1["skuInfo"]:
                # 为每个sku添加“pickingSequence”字段，即该sku在本集单内的拣货顺序
                item2["pickingSequence"] = route_list[i]
                i+=1
        print(f'handled Json data: {json_data}')
        print(route_list)

        # 返回更新后的json数据集
        return json_data
    else:
        print('No solution found.')

async def runMain(raw_data, xStart, yStart):
    # 建立asyncio异步任务列表
    tasks = []
    # 最大协程数量, 目前不需要设置
    # semaphore = asyncio.Semaphore(10)
    for item in raw_data["batchInfo"]:
        # 由于集单之间是没有相关性的，因此把订单池按照集单进行拆分，每个集单
        # 由一个协程处理。
        tasks.append(singleMain(item["outOrderInfo"], xStart, yStart))
    # await会等待所有协程结束然后将所有结果整合为一个list输出到result中
    result = await asyncio.gather(*tasks) # 需要在这之后重新整合为一个
    # 将输出的新字段重新加回到原始数据中并返回
    for i in range(len(raw_data["batchInfo"])):
        raw_data["batchInfo"][i]["outOrderInfo"] = result[i]
    return raw_data
        

