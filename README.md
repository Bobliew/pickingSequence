# 路径规划模块拣货顺序
## 实现方法
### Ortools
关于Ortools的详细资料，可以参考[ortools官方文档](https://developers.google.com/optimization?hl=zh-cn)
基于Ortools实现的拣货顺序计算文件位于strategyLkh目录下，可用的测试数据位于quickStart目录下，本地调用方式如下所示：
``` bash
Invoke-RestMethod -Method POST -Uri http://localhost:5000/routing_Picking_Sequence_Ortool_version1 -ContentType "application/json" -Body (Get-Content "output.json" -Raw)

```
目前也已经在公司的服务器中进行了测试部署，调用方式为：
``` bash
Invoke-RestMethod -Method POST -Uri http://172.16.11.15:8890/routing_Picking_Sequence_Ortool_version1 -ContentType "application/json" -Body (Get-Content "output.json" -Raw)
```

### LKH-3
关于LKH-3的详细资料，可以参考[LKH官方文档](http://webhotel4.ruc.dk/~keld/research/LKH-3/)
目前LKH-3的本地实现已经基本完成，目前正在进行与框架的对接工作；

## 联系我们
廖铭浩

## 项目状态
持续开发中，预期与wms1.2.9版本同步上线。
