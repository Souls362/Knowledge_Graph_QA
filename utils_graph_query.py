#-*-coding: UTF-8 -*-
# queries for knowledge graph

##校验查询

###保险产品查询校验
'''
输入    product_name = 保险产品名(实体) string

返回    node    产品节点   node
        None    无该产品
'''
def check_product(graph, ner):
    product_name = ner['product_name']
    node = graph.find_one(label='产品', property_key='name', property_value=product_name)
    result = node
    if result == None:
        return None
    else:
        return result

# print(check_product(graph, 'e生保'))

###疾病名/别名查询校验
'''
输入    disease_name = 疾病名(实体) string

返回    node    疾病节点    node
        None    无该疾病
'''
def check_disease(graph, ner):
    disease_name = ner['disease']
    for label in ['疾病','疾病.别名']:
        node = graph.find_one(label=label, property_key='name', property_value=disease_name)
        if node != None:
            if label == '疾病.别名':
                n = graph.run('match(n)-[:`疾病.别名`]->(a) where a.name="'+node['name']+'" return n')
                return [i for i in n][0][0]
            else:
                return node
    return None

# print(check_disease(graph, '瘿气'))
# print(check_disease(graph, '甲亢'))

###保险类型查询校验
'''
输入    insurance_name = 保险产品名 string

返回    list    保险类型范围    list
        None    该保险无险种
'''
def check_insurancetype(graph,ner):
    product_name = ner['product_name']
    #校验保险产品
    n = graph.run('match(:产品 {name:"'+product_name+'"})-[: `产品.保险类型`]->(n) return n')
    try:
        n = [i['n']['name'] for i in n]
        return n
    except:
        return None

# print(check_insurancetype(graph,'平安福'))

##属性查询

###保险价格
'''
特殊疑问
e生保的产品价格是多少(元:int)

输入    product_name = 保险产品名(实体) string

返回    None    若产品不存价格
        194(元) 产品价格    int
'''
def check_price(graph, ner):
    product_name = ner['product_name']
    node = graph.run('match(:产品 {name:"' + product_name + '"})-[:`产品.保险价格`]-(n) return n')
    result = [i for i in node]
    if result == []:
        return None
    else:
        return int(result[0]['n']['name'])

# print(check_price(graph, 'e生保'))

###投保年龄

'''
特殊疑问
e生保产品的投保人年龄是什么 (岁:range)
一般疑问
XX岁是否可以买e生保

输入    product_name = 保险产品名(实体) string 
        (Option) age = 年龄(实体)   int

返回    None    若产品不存在投保人年龄
        True    满足投保年龄    boolean
        False   不满足投保年龄    boolean
        (10,100)    投保年龄范围   tuple
'''
def check_age(graph, ner):
    product_name = ner['product_name']
    if 'age' in ner:
        age = ner['age']
    else:
        age = None
    n_min = graph.run('match(:产品 {name:"' + product_name + '"})-[:`产品.最小投保年龄`]-(n_min) return n_min')
    n_max = graph.run('match(:产品 {name:"' + product_name + '"})-[:`产品.最大投保年龄`]-(n_max) return n_max')
    try:
        n_min = [i for i in n_min][0]
        n_max = [i for i in n_max][0]
        if age == None:
            return (n_min[0]['data'],n_max[0]['data'])
        else:
            if age <= n_max[0]['data'] and age >= n_min[0]['data']:
                return True
            else:
                return False
    except:
        return None

# print(check_age(graph,'e生保'))
# print(check_age(graph,'e生保',13))

###犹豫期
'''
特殊疑问
平安福产品的犹豫期是多久(天:int)

输入    product_name = 保险产品名(实体) string

返回    None 若产品不存在犹豫期
        10(天) 产品犹豫期 int
'''
def check_youyuqi(graph,ner):
    product_name = ner['product_name']
    n = graph.run('match(: 产品{name:"'+product_name+'"})-[: `产品.犹豫期`]-(n) return n')
    try:
        n = [i for i in n][0]
        return n[0]['data']
    except:
        None

# print(check_youyuqi(graph,'平安福'))

###等待期
'''
特殊疑问
平安福产品的等待期是几天(天:int)

输入    product_name = 保险产品名(实体) string

返回    None 若产品不存在等待期
        10(天) 产品等待期 int
'''
def check_dengdaiqi(graph,ner):
    product_name = ner['product_name']
    n = graph.run('match(: 产品{name:"'+product_name+'"})-[: `产品.等待期`]-(n) return n')
    try:
        n = [i for i in n][0]
        return n[0]['data']
    except:
        None

# print(check_dengdaiqi(graph,'平安福'))

#保障期限
'''
特殊疑问
e生保产品的保障期限是多久(年:int)

输入    product_name = 保险产品名(实体) string

返回    None 若产品不存在保障期限 
        1(年) 产品保障期限 int
'''
def check_baozhangqixian(graph,ner):
    product_name = ner['product_name']
    n = graph.run('match(: 产品{name:"'+product_name+'"})-[: `产品.保障期限`]-(n) return n')
    try:
        n = [i for i in n][0]
        return n[0]['data']
    except:
        None

# print(check_baozhangqixian(graph,'e生保'))

#保障疾病
'''
特殊疑问
平安福产品的保障疾病有哪些(list)
一般疑问
平安福是否保障XXX(疾病)

输入    product_name = 保险产品名(实体) string
        (Option) disease = 疾病(实体，支持别名) string

返回    True    疾病在该产品保障范围内  boolean
        False   疾病不在该产品保障范围内    boolean
        ['心脏瓣膜手术', '脊髓小脑变性症', '闭锁综合征', '系统性红斑狼疮并发肾功能损害',...] 保障疾病范围    list
        []  无保障疾病  list
'''
def check_disease_guarantee(graph, ner):
    product_name = ner['product_name']
    n = graph.run('match(:产品 {name:"' + product_name + '"})-[:`产品.保障疾病`]-(n) return n')

    try:
        n = [i for i in n]
        disease_range = [i[0]['name'] for i in n]
        if 'disease' in ner:
            disease_name = check_disease(graph, ner)
            disease_name = disease_name['name']
            if disease_name in disease_range:
                return True
            else:
                False
        else:
            return disease_range
    except:
        return []

# print(check_disease_guarantee(graph,'平安福','早期运动神经元病'))
# print(check_disease_guarantee(graph,'平安福'))

#疾病核保-触发
'''
特殊疑问
XX疾病可以买XX险(险种)吗
XX疾病可以买XX险(保险产品)吗

多轮问答
触发多轮核保对话

输入    insurance_type = 保险类型(查询结果) list
        disease = 疾病名(查询结果)  node

返回    True    可投保 boolean
        False   不可投保 boolean
        (node,'start')    触发核保问题,对话状态   String,String
        None    无法判定    String
'''
def check_disease_satisfy_insurance(graph, insurance_type, disease):

    if disease == None:
        return (False,'end')
    if insurance_type == []:
        return None
    # 判断是否触发核保状态
    n = graph.run('match(:对话状态 {name:"触发状态-核保"})-[:后继对话状态]->(n) return n')
    hebao_disease_list = [i['n']['disease'] for i in n]
    verified_type = []
    if disease['name'] in hebao_disease_list:
        # 根据保险类型触发多轮对话
        for i in insurance_type:
            name = disease['name'] + '-' + i + '-核保'
            node = graph.find_one('核保类型', 'name', name)
            if node != None:
                verified_type.append(node)
                result = graph.run('match(:核保类型 {name:"' + node['name'] + '"})-[:对话流程]->(n) return n')
                return ([i for i in result][0]['n'], 'start',insurance_type)
    if verified_type == []:
        return None
    return (True,'end')

# print(check_disease_satisfy_insurance(graph,'平安福','甲亢'))

#疾病核保-进行中
'''
输入    上轮节点 node
        险种 string
        意图/回答 (是否)
        
返回    ('延期','end')    投保结果
        ('有无并发症','start')    核保问题下一轮,对话状态   String,String
        None    无法判定    String
'''
def check_disease_satisfy_insurance_dialogue(graph,answer,node,insurance_type):
    current_name = node['name']
    current_disease = node['disease']
    result = graph.run('match(n {name:"'+current_name+'",disease:"'+current_disease+'"})-[:`后继对话状态`{answer:"'+answer+'"}]->(a) return a')
    result = [i for i in result]
    if result == []:
        result = graph.run(
            'match(n {name:"' + current_name + '",disease:"' + current_disease + '"})-[:`后继对话状态`{answer:"是|否"}]->(a) return a')
        result = [i for i in result]
        if result == None:
            return None
    result = result[0]['a']
    if result['status_type'] == "continue":
        return(result,"start")
    if result['status_type'] == "end":
        result = graph.run('match(n {name:"'+current_name+'", disease:"'+current_disease+'"})-[:`'+'核保结果-'+insurance_type[0]+'-'+answer+'`]->(a) return a')
        result = [i for i in result][0]['a']
        if result['name'] == '统一回复':
            result = graph.run('match(n {name:"' + current_disease + '"})-[:`疾病.投保建议`]->(a) return a')
            result = [i for i in result][0]['a']
        return(result,'end')
# print(check_disease_satisfy_insurance_dialogue(graph,'否',node,'寿险'))


#保险推荐场景
'''
输入    attribute dict 
            {'disease':'羊水过少'}
            {'age':16}
            {'price':500/'None'}
        return_type String
            'insurace_type'/'insurance'
        
返回    保险产品/险种list list
'''
def check_product_by_attribute(graph,intent,attribute):
    #满足该年龄条件的保险产品有那些
    if 'age' in attribute:
        result_max = graph.run('match(n:`产品`)-[:`产品.最大投保年龄`]-(a) where a.data>' + str(attribute['age']) + ' return n')
        if result_max != []:
            result_max = [i['n']['name'] for i in result_max]
        result_min = graph.run('match(n:`产品`)-[:`产品.最小投保年龄`]-(a) where a.data<' + str(attribute['age']) + ' return n')
        if result_min != []:
            result_min = [i['n']['name'] for i in result_min]
        result = [i for i in result_max if i in result_min]

    if "price" in attribute:
        result = []
        insurace = []
        lowest_insurance = []
        for i in graph.find("产品"):
            price = graph.run('match(产品 {name:"' + i["name"] + '"})-[:`产品.保险价格`]-(n) return n')
            price = [i for i in price]
            if price == []:
                continue
            insurace.append(i)
            lowest_insurance.append(float(price[0]['n']['name']))
        if attribute['price'] == 'None':
            result.append(insurace[lowest_insurance.index(min(lowest_insurance))]['name'])
        else:
            result = [insurace[i]['name'] for i in range(len(insurace)) if
                      float(lowest_insurance[i]) <= attribute['price']]

    if "disease" in attribute:
        result = graph.run('match(n:`产品`)-[:`产品.保障疾病`]->(:`疾病` {name:"'+attribute['disease']+'"}) return n')
        result = [i for i in result]
        if result != []:
            result = [i['n']['name'] for i in result]

    if intent == '41':
        result_type = []
        for i in result:
            tmp = graph.run('match(产品 {name: "'+i+'"})-[: `产品.保险类型`]->(n) return n')
            tmp = [i for i in tmp]
            if tmp != []:
                result_type.extend([i['n']['name'] for i in tmp])
        return list(set(result_type))
    else:
        return result

# print(check_product_by_attribute(graph,{"age":13},'insurance_type'))
# print(check_product_by_attribute(graph,{"age":0},'insurance_type'))
# print(check_product_by_attribute(graph,{"price":500},'insurance_type'))
# print(check_product_by_attribute(graph,{"price":'None'},'insurance_type'))
# print(check_product_by_attribute(graph,{"disease":'羊水过少'},'insurance_type'))
# print(check_product_by_attribute(graph,{"disease":'羊水过少aa'},'insurance_type'))

