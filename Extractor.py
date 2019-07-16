from intent_recognition import IntentRecognizer
from ner_knowledge_graph.ner_combine import ner as ner_py
from ner_trans import result_trans
import re

class StateControl(object):
    def __init__(self, sentence, prev_state, intent):
        self.sentence = sentence
        self.prev_state = prev_state
        self.intent = intent

    def step(self):
        '''
        @usage: Given the current sentcen, intent and previous state, update the conversation state
        '''
        branch = None
        if self.prev_state['intent'] == '核保' and self.intent == 'null_intent':
            yes_res = re.search('(有|是|对)+', self.sentence)
            no_res = re.search('(否|不是|不对|错|无)+', self.sentence)
            if yes_res or no_res:
                current_state = self.prev_state
                if yes_res:
                    branch = 1
                elif no_res:
                    branch = 0

        else:
            current_state = self.prev_state
            current_state['status'] = "end"
            current_state['intent'] = self.intent

        return current_state, branch

class Extractor(object):
    def __init__(self):
        '''
        @param:

        '''
        self.intent_recognizer = IntentRecognizer()
        # self.ner = NER
        self.intent_recognizer.load_model()
        self.ner_class = ner_py()
        self.ner_class.initialize()

    def ner(self, sentence):
        '''
        :param sentence:
        :return
        '''

        ner_res = self.ner_class.ner(sentence)
        if 'age' in ner_res:
            for i in range(len(ner_res['age'])):
                input_dict = dict()
                input_dict['age'] = ner_res['age'][i][0]
                num_extraction = result_trans()
                res_dict = num_extraction.run(input_dict)
                ner_res['age'][i].append(res_dict['age'])

        return ner_res

    def intent_recognition(self, sentence, ner_list):
        intent_clf = self.intent_recognizer.intent_clf(sentence)
        return self.intent_recognizer.pattern_match(intent_clf, sentence, ner_list)


    def gen_extraction(self,sentence):
        ner_res = self.ner(sentence)
        ner_list = []

        if 'insurance' in ner_res:
            ner_list.append('product')
        if 'disease' in ner_res:
            ner_list.append('disease')
        if 'age' in ner_res:
            ner_list.append('age')

        intent_res = self.intent_recognition(sentence, ner_list)
        return intent_res, ner_res

    def ner_trans(self,ner):
        if 'insurance' in ner:
            ner['product_name'] = ner['insurance']['root'][0][0]
        if 'disease' in ner:
            ner['disease'] = ner['disease'][0][0]
        if 'age' in ner:
            ner['age'] = float(ner['age'][0][-1])
        return ner

    def intent_trans(self, intent, ner, branch):
        if intent == '核保' and 'disease' in ner and 'product_name' in ner:
            intent = '230'
        if intent == '犹豫期':
            intent = '13'
        if intent == '年龄':
            intent = '12'
        if intent == '保障范围':
            intent = '16'
        if intent == '核保' and 'age' in ner and 'product_name' in ner:
            intent = '21'
        if intent == '等待期':
            intent = '14'
        if intent == '产品价格':
            intent = '11'
        if intent == '保障期限':
            intent = '15'
        if intent == '核保' and 'age' in ner and 'product_name' not in ner:
            intent = '31'
        if intent == '核保' and 'disease' in ner and 'product_name' not in ner:
            intent = '31'
        if branch == 1:
            intent = '231'
        if branch == 0:
            intent = '232'
        #if intent == '疾病_险种':
        #    intent = '41'
        return intent


if __name__ == '__main__':

    query_extraction = Extractor()

    test_list = [
            ['我妈得了甲亢能买平安福吗', 1, ["disease", 'product']],    #
            ['我妈得了癌症能买平安福吗', 1, ["disease", 'product']],
            ['平安福的犹豫期是多久',0,['product']],
            ['e生保的投保年龄',0,['product']],
            ['平安福都保障什么疾病',0,['product']],

            ['我爸爸60岁了能投保e生保吗？',1,['age','product']],

            ['平安福的等待期是多少',0,['product']],
            ['e生保每年需要交多少钱',0,['product']],
            ['我买e生保可以保障多久', 0, ['product']],
            ['我16岁可以买哪些保险', 1, ['age']],

            #['我去年做过手术可以买重疾险吗',1,['disease','product']],
            #['得了甲肝还可以投保平安福吗',1,['disease','product']],

            ['我得了癌症还可以买哪些保险',1,['disease']],
            ['我得了癌症还可以买什么类型的产品',1,['disease']],
            ['你们卖的最贵的保险是哪个',1,[]],
            ['是', 0, []],
            ['否', 0, []]
            ]


    for sample in test_list:
        intent_res,ner_res = query_extraction.gen_extraction(sample[0])
        current_state = {'status':'start','intent':'核保'}
        state_control = StateControl(sample[0], current_state, intent_res)
        current_state, branch = state_control.step()
        print(intent_res,ner_res)
        print(current_state, branch)


