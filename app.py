from flask import Flask
app = Flask(__name__)
# 加载所需包
from strategyOrtool.orVersion1 import *
from flask import request, Response
import time
import json


# 定义app为Falsk框架的名称
app = Flask(__name__)
# 放开最大请求大小限制
app.config['MAX_CONTENT_LENGTH'] = None
# 放开JSON响应的容量限制
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
# 放开静态文件的缓存时间限制
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# 开启调试模式
app.config['DEBUG'] = True
# 放开模板自动重新加载的限制
app.config['TEMPLATES_AUTO_RELOAD'] = True

#
'''
请求方式见readme文档
'''
# 默认域名
@app.route('/')
def hello():
    return "Welcome to Picking Sequence Module of Routing Strategies version 1."

# version 1 ortools求解拣货顺序问题
@app.route('/routing_Picking_Sequence_Ortool_version1', methods=['POST'])
def routing_Picking_Sequence_Ortool_version1():
    start_time = time.time()
    jsonData = request.get_json()
    jsonData = json.loads(jsonData)
    print(type(jsonData))
    # (0,0)是设定好的depot点，response_data是从请求获得的数据
    response_data = asyncio.run(runMain(jsonData, 0, 0))
    print(response_data)
    response = Response(response_data, content_type='json')
    # jsonData = json.dumps(str(response_data))
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("最终结果：{}".format(response_data))
    print("计算时间为：{}秒".format(elapsed_time))
    return response_data




if __name__ == '__main__':
    app.run()
