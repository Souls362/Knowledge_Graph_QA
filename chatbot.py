#-*-coding: UTF-8 -*-

from dialogue_session_manage import session_manage
from knowledge_graph_search import graph_search
from Extractor import Extractor, StateControl
from result_modify import result_modify


class chatbot(object):

    def __init__(self):
        self.session_manage = session_manage()
        self.query_extraction = Extractor()
        self.graph_search = graph_search()
        self.result_modify = result_modify()

    def run(self, user_input):

        if user_input == 'state':
            return self.session_manage.session_info
        self.session_manage.update_q(user_input)
        intent_res, ner_res = self.query_extraction.gen_extraction(user_input)
        state_control = StateControl(user_input, self.session_manage.session_info, intent_res)
        current_state, branch = state_control.step()
        ner_res = self.query_extraction.ner_trans(ner_res)
        intent_res = self.query_extraction.intent_trans(intent_res, ner_res, branch)
        #print(intent_res,ner_res)
        try:
            result = self.graph_search.run(intent_res, ner_res, self.session_manage.session_info)
            result = self.result_modify.run(intent_res,ner_res,result)
        except:
            result = None
        self.session_manage.update_a(result)
        return result


if __name__ == '__main__':
    chatbot = chatbot()

    while True:
        #print(chatbot.session_manage.session_info)
        user_input = input('用户: ')
        if user_input == 'exit':
            break
        print('智能客服: ' + str(chatbot.run(user_input)))

# '我妈得了甲亢能买平安福吗'
# '平安福的犹豫期是多久'
# 'e生保的投保年龄'
# '平安福都保障什么疾病'
# '我爸爸60岁了能投保e生保吗？'
# '我爸爸48岁了能投保e生保吗？'
# '平安福的等待期是多少'
# 'e生保每年需要交多少钱'
# '我买e生保可以保障多久'
# '我16岁可以买哪些保险'

# '我得了癌症还可以买哪些保险'
# '我得了癌症还可以买什么类型的产品'
# '你们卖的最贵的保险是哪个'