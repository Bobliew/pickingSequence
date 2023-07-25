import json

# 假设 jsonString 是包含分配信息的 JSON 字符串
jsonString = "{\"batchInfo\":[{\"pickingCode\":\"0\",\"outOrderInfo\":[{\"orderCode\":\"OB0101103305670624\",\"skuInfo\":[{\"skuCode\":\"81389774641\",\"allocateLocation\":\"A-04-15\",\"xCoordAloc\":-24179.9345,\"yCoordAloc\":24379.6405,\"allocateAmount\":1}]},{\"orderCode\":\"OB0101062827023533\",\"skuInfo\":[{\"skuCode\":\"81624684198\",\"allocateLocation\":\"A-04-03\",\"xCoordAloc\":-24179.9345,\"yCoordAloc\":24379.6405,\"allocateAmount\":1}]},{\"orderCode\":\"OB0101235145874182\",\"skuInfo\":[{\"skuCode\":\"81988809473\",\"allocateLocation\":\"A-04-01\",\"xCoordAloc\":-24794.9928,\"yCoordAloc\":24379.6405,\"allocateAmount\":1}]},{\"orderCode\":\"OB0101005114939112\",\"skuInfo\":[{\"skuCode\":\"CN-PEN-00022\",\"allocateLocation\":\"A-04-06\",\"xCoordAloc\":-22763.6333,\"yCoordAloc\":27631.7274,\"allocateAmount\":1}]},{\"orderCode\":\"OB0101144240707483\",\"skuInfo\":[{\"skuCode\":\"CN-PEN-00022\",\"allocateLocation\":\"A-04-06\",\"xCoordAloc\":-22763.6333,\"yCoordAloc\":27631.7274,\"allocateAmount\":1}]},{\"orderCode\":\"OB0101121913833919\",\"skuInfo\":[{\"skuCode\":\"CN-QUA-51117\",\"allocateLocation\":\"A-03-06\",\"xCoordAloc\":-22763.6333,\"yCoordAloc\":16743.3011,\"allocateAmount\":1}]},{\"orderCode\":\"OB0102051404499303\",\"skuInfo\":[{\"skuCode\":\"CN-PEN-00022\",\"allocateLocation\":\"A-03-06\",\"xCoordAloc\":-22763.6333,\"yCoordAloc\":16743.3011,\"allocateAmount\":1}]},{\"orderCode\":\"OB0101114934016952\",\"skuInfo\":[{\"skuCode\":\"82329843804\",\"allocateLocation\":\"A-03-08\",\"xCoordAloc\":-22148.5751,\"yCoordAloc\":16743.3011,\"allocateAmount\":1}]},{\"orderCode\":\"OB0101112838987220\",\"skuInfo\":[{\"skuCode\":\"CN-ANK-83240\",\"allocateLocation\":\"A-03-12\",\"xCoordAloc\":-20148.5751,\"yCoordAloc\":16743.3011,\"allocateAmount\":1}]},{\"orderCode\":\"OB0101003918241851\",\"skuInfo\":[{\"skuCode\":\"CN-JIN-09001\",\"allocateLocation\":\"A-03-18\",\"xCoordAloc\":-16763.9009,\"yCoordAloc\":16763.1665,\"allocateAmount\":1}]}]},{\"pickingCode\":\"1\",\"outOrderInfo\":[{\"orderCode\":\"OB0102053330792539\",\"skuInfo\":[{\"skuCode\":\"CN-UND-32804\",\"allocateLocation\":\"A-02-01\",\"xCoordAloc\":-24794.9928,\"yCoordAloc\":-90.2249,\"allocateAmount\":1}]},{\"orderCode\":\"OB0101232746805071\",\"skuInfo\":[{\"skuCode\":\"CN-UND-32804\",\"allocateLocation\":\"A-02-01\",\"xCoordAloc\":-24794.9928,\"yCoordAloc\":-90.2249,\"allocateAmount\":1}]},{\"orderCode\":\"OB0101191228609380\",\"skuInfo\":[{\"skuCode\":\"CN-UND-32804\",\"allocateLocation\":\"A-02-01\",\"xCoordAloc\":-24794.9928,\"yCoordAloc\":-90.2249,\"allocateAmount\":1}]},{\"orderCode\":\"OB0102051150044802\",\"skuInfo\":[{\"skuCode\":\"CN-UND-32804\",\"allocateLocation\":\"A-02-08\",\"xCoordAloc\":-22148.5751,\"yCoordAloc\":3293.3011,\"allocateAmount\":1}]},{\"orderCode\":\"OB0101070411955973\",\"skuInfo\":[{\"skuCode\":\"82002075413\",\"allocateLocation\":\"A-02-14\",\"xCoordAloc\":-18763.9009,\"yCoordAloc\":3313.1665,\"allocateAmount\":1}]},{\"orderCode\":\"OB0101032936960069\",\"skuInfo\":[{\"skuCode\":\"81634475074\",\"allocateLocation\":\"A-02-14\",\"xCoordAloc\":-18763.9009,\"yCoordAloc\":3313.1665,\"allocateAmount\":1}]},{\"orderCode\":\"OB0102075129547806\",\"skuInfo\":[{\"skuCode\":\"CN-JIN-5A001\",\"allocateLocation\":\"A-02-16\",\"xCoordAloc\":-18148.8426,\"yCoordAloc\":3313.1665,\"allocateAmount\":1}]},{\"orderCode\":\"OB0101093230184171\",\"skuInfo\":[{\"skuCode\":\"82301043168\",\"allocateLocation\":\"A-02-16\",\"xCoordAloc\":-18148.8426,\"yCoordAloc\":3313.1665,\"allocateAmount\":1}]},{\"orderCode\":\"OB0101113453943054\",\"skuInfo\":[{\"skuCode\":\"CN-UND-94497\",\"allocateLocation\":\"A-02-22\",\"xCoordAloc\":-14763.9009,\"yCoordAloc\":3313.1665,\"allocateAmount\":1}]},{\"orderCode\":\"OB0101102605295855\",\"skuInfo\":[{\"skuCode\":\"80862975308\",\"allocateLocation\":\"A-03-01\",\"xCoordAloc\":-24794.9928,\"yCoordAloc\":10929.6405,\"allocateAmount\":1}]}]},{\"pickingCode\":\"2\",\"outOrderInfo\":[{\"orderCode\":\"OB0101195440599106\",\"skuInfo\":[{\"skuCode\":\"82003079736\",\"allocateLocation\":\"A-05-25\",\"xCoordAloc\":-12713.9009,\"yCoordAloc\":37195.8194,\"allocateAmount\":1}]},{\"orderCode\":\"OB0101064633467094\",\"skuInfo\":[{\"skuCode\":\"82167939023\",\"allocateLocation\":\"A-05-23\",\"xCoordAloc\":-14098.8426,\"yCoordAloc\":37215.6849,\"allocateAmount\":1}]},{\"orderCode\":\"OB0102110148757868\",\"skuInfo\":[{\"skuCode\":\"CN-JIN-09001\",\"allocateLocation\":\"A-05-21\",\"xCoordAloc\":-14713.9009,\"yCoordAloc\":37215.6849,\"allocateAmount\":2}]},{\"orderCode\":\"OB0102142828141361\",\"skuInfo\":[{\"skuCode\":\"CN-PEN-00022\",\"allocateLocation\":\"A-03-22\",\"xCoordAloc\":-14763.9009,\"yCoordAloc\":16763.1665,\"allocateAmount\":1}]},{\"orderCode\":\"OB0102125015066311\",\"skuInfo\":[{\"skuCode\":\"CN-PEN-00022\",\"allocateLocation\":\"A-03-27\",\"xCoordAloc\":-12148.8426,\"yCoordAloc\":12773.4356,\"allocateAmount\":1}]},{\"orderCode\":\"OB0101143518077216\",\"skuInfo\":[{\"skuCode\":\"CN-CON-90890\",\"allocateLocation\":\"A-03-01\",\"xCoordAloc\":-24794.9928,\"yCoordAloc\":10929.6405,\"allocateAmount\":1}]},{\"orderCode\":\"OB0101004918225403\",\"skuInfo\":[{\"skuCode\":\"82044910785\",\"allocateLocation\":\"A-01-27\",\"xCoordAloc\":-12148.8426,\"yCoordAloc\":-13406.6989,\"allocateAmount\":2}]}]}]}"


# 解析 JSON 字符串为 Python 对象
jsonData = json.loads(jsonString)

# 获取 batchInfo 数组
batchInfo = jsonData["batchInfo"]

# 遍历 batchInfo 数组，并删除每个 SKU 的 xCoordAloc 和 yCoordAloc 字段
for batch in batchInfo:
  pickingCode = batch["pickingCode"]
  outOrderInfo = batch["outOrderInfo"]
  batch["shelfInfo"] = outOrderInfo
  del batch["outOrderInfo"]
  for orderInfo in outOrderInfo:
    del orderInfo["orderCode"]
    skuInfo = orderInfo["skuInfo"]
    del orderInfo["skuInfo"]
    for sku in skuInfo:
      # 删除 xCoordAloc 和 yCoordAloc 字段
      del sku["xCoordAloc"]
      del sku["yCoordAloc"]
      del sku["allocateAmount"]
      del sku["skuCode"]
print (jsonData)

