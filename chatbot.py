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
        # self.intent = intent()

    def run(self, user_input):

        if user_input == 'state':
            return self.session_manage.session_info
        self.session_manage.update_q(user_input)
        intent_res, ner_res = self.query_extraction.gen_extraction(user_input)
        state_control = StateControl(user_input, self.session_manage.session_info, intent_res)
        current_state, branch = state_control.step()
        ner_res = self.query_extraction.ner_trans(ner_res)
        intent_res = self.query_extraction.intent_trans(intent_res, ner_res, branch)
        result = self.graph_search.run(intent_res, ner_res, self.session_manage.session_info)
        #result = result_modify.run(result)
        #self.session_manage.update_a(intent_res,ner_res,result)
        return result


if __name__ == '__main__':
    chatbot = chatbot()

    while True:
        #print(chatbot.session_manage.session_info)
        user_input = input('Plz Enter: ')
        print(chatbot.run(user_input))