#-*-coding: UTF-8 -*-

'''
Session_info:
{
'qa_pair':[(q,a),(q,a),...],
'status':'active',
'node': node 多轮对话中的上一节点
}

'''

class session_manage(object):

    def __init__(self):
        self.session_info = {'qa_pair':[],'status':'end','node':'','insurance_type':'','intent':[]}
        self.qa = []

    def update_q(self,value):
        self.qa.append(value)
        return self.qa

    def update_a(self,value):
        self.qa.append(value)
        self.session_info['qa_pair'].append(tuple(self.qa))
        self.qa = []
        return self.session_info

    def update_status(self,value,key='status'):
        self.session_info[key] = value
        return self.session_info

    def update_intent(self,value,key='intent'):
        self.session_info[key].append(value)
        return self.session_info

    def update_node(self,value,key='node'):
        self.session_info[key] = value
        return self.session_info

    def update_insurance_type(self,value,key='insurance_type'):
        self.session_info[key] = value
        return self.session_info

    def update_dialogue(self,a,status,node,insurance_type):
        self.update_a(self, a)
        self.update_status(self,status)
        self.update_node(self,node)
        self.update_insurance_type(self,insurance_type)