#-*-coding: UTF-8 -*-
# convert intent to search query
from py2neo import *
from utils_graph_query import *

'''
意图:{'11','12','13','14','15','16','21','22','23','241','242'}
对话状态{'end','start'}
ner:{'product_name','disease','age'}
'''
class graph_search(object):

    def __init__(self):
        self.graph = Graph('http://neo4j:423329_Ice@localhost:7474/db/data/')
        self.intent_class = {
            '11': check_price,
            '12': check_age,
            '13': check_youyuqi,
            '14': check_dengdaiqi,
            '15': check_baozhangqixian,
            '16': check_disease_guarantee,
            '21': check_age,
            '22': check_disease_guarantee,
            '230': check_disease_satisfy_insurance,
            '231': check_disease_satisfy_insurance_dialogue,
            '232': check_disease_satisfy_insurance_dialogue,
            '31': check_product_by_attribute,
            '41': check_product_by_attribute
        }
        self.ner_class = {
            '11': ['product_name'],
            '12': ['product_name'],
            '13': ['product_name'],
            '14': ['product_name'],
            '15': ['product_name'],
            '16': ['product_name'],
            '21': ['product_name', 'age'],
            '22': ['product_name', 'disease'],
            '230': ['product_name', 'disease'],
            '231': ['product_name', 'disease'],
            '232': ['product_name', 'disease'],
            '31': ['disease','age','price'], #any one
            '41': ['disease','age','price']
        }

    #NER结果与意图校验 question_type 1-2
    def intent_ner_validation(self,intent,ner):
        # 校验NER/Intent结果
        if intent == '31' or intent == '41' or intent == '231' or intent == '232':
            return True

        ner_result = [i for i in self.ner_class[intent] if i in ner]
        #if sorted(ner_result) != sorted(self.ner_class[intent]):
        if sorted([i for i in self.ner_class[intent] if i in ner_result]) != sorted(self.ner_class[intent]):
            # NER结果与意图结果没有对齐
            return None
        for i in ner_result:
            if i not in ner_result:
                ner.pop(i)

        insurance_name = check_product(self.graph, ner)
        if insurance_name == None:
            return None

        # 校验图谱中NER结果
        for i in ner:
            if i == 'disease':
                disease_name = check_disease(self.graph, ner)
                if disease_name == None:
                    return None
            if i == 'product_name':
                insurance_name = check_product(self.graph, ner)
                if insurance_name == None:
                    return None
                if intent == '23':
                    insurance_type = check_insurancetype(self.graph, ner)
                    if insurance_type == None:
                        return None
        return True

    #普通属性相关
    def find_attribute(self,intent,ner):
        #意图转换搜索语句
        return self.intent_class[intent](self.graph, ner)

    def find_underwriting(self, intent, ner, session_info):

        if intent == '230':
            insurance_type = check_insurancetype(self.graph,ner)
            disease = check_disease(self.graph,ner)
            result = self.intent_class[intent](self.graph, insurance_type, disease)
            if result != None:
                session_info['node'] = result[0]
                session_info['status'] = result[1]
                session_info['insurance_type'] = result[2]
        else:
            if intent == '231':
                answer = '是'
            if intent == '232':
                answer = '否'
            node = session_info['node']
            insurance_type = session_info['insurance_type']
            result = self.intent_class[intent](self.graph, answer, node, insurance_type)
            if result[1] == 'end':
                session_info['status'] = ''
                session_info['node'] = ''
                session_info['insurance_type'] = ''
            else:
                session_info['node'] = result[0]
        return result

    #产品推荐场景
    def recommend_product(self,intent,ner):
        return self.intent_class[intent](self.graph, intent, ner)

    def run(self,intent, ner, session_info):

        if self.intent_ner_validation(intent,ner) == None:
            # return 'intent & ner not match'
            return None
        if intent[0] == '1' or intent == '21' or intent == '22':
            return self.find_attribute(intent,ner)
        if intent == '31' or intent == '41':
            return self.recommend_product(intent,ner)
        if intent[0:2] == '23':
            return self.find_underwriting(intent, ner, session_info)


if __name__ == '__main__':

    graph_search = graph_search()
    session_info = {}

    #e生保的价格是多少
    intent = '11'
    ner = {'product_name':'e生保'}
    print(graph_search.run(intent, ner, session_info))

    # e生保的投保年龄
    intent = '12'
    ner = {'product_name': 'e生保'}
    print(graph_search.run(intent, ner, session_info))

    # 平安福的犹豫期是几天
    intent = '13'
    ner = {'product_name': '平安福'}
    print(graph_search.run(intent, ner, session_info))

    #平安福的等待期是几天
    intent = '14'
    ner = {'product_name': '平安福'}
    print(graph_search.run(intent, ner, session_info))

    # 平安福的保障期限是多久
    intent = '15'
    ner = {'product_name': 'e生保'}
    print(graph_search.run(intent, ner, session_info))

    # 平安福的保障哪些疾病
    intent = '16'
    ner = {'product_name': '平安福'}
    print(graph_search.run(intent, ner, session_info))

    # 13岁可以买e生保吗
    intent = '21'
    ner = {'product_name': 'e生保', 'age':13}
    print(graph_search.run(intent, ner, session_info))

    # 早期运动神经元病在平安福保障范围内吗
    intent = '22'
    ner = {'product_name': '平安福', 'disease': '早期运动神经元病'}
    print(graph_search.run(intent, ner, session_info))

    # 甲亢可以买平安福吗
    intent = '230'
    ner = {'product_name': '平安福', 'disease': '甲亢'}
    print(graph_search.run(intent, ner, session_info))

    # 目前甲功是否正常-是
    intent = '231'
    ner = {'product_name': '平安福', 'disease': '甲亢'}
    graph = Graph('http://neo4j:423329_Ice@localhost:7474/db/data/')
    node = graph.find_one("对话状态",'name','澄清状态-目前甲功是否正常')
    session_info['node'] = node
    session_info['insurance_type'] = '寿险'
    print(graph_search.run(intent, ner, session_info))

    # 目前甲功是否正常-否
    intent = '232'
    print(graph_search.run(intent, ner, session_info))
    #print(graph_search.find_attribute('16','a',{'product_name':'平安福','disease':'心脏瓣膜手术'}))

    # 18岁可以买哪种险
    intent = '31'
    ner = {'age': 18, 'return_type': 'insurance_type'}
    print(graph_search.run(intent, ner, session_info))

    # 50000元一下的保险产品有什么
    intent = '31'
    ner = {'price': 50000, 'return_type': 'insurance'}
    print(graph_search.run(intent, ner, session_info))

    # 哪个保险保障羊水过少
    intent = '31'
    ner = {'disease': '羊水过少', 'return_type': 'insurance'}
    print(graph_search.run(intent, ner, session_info))