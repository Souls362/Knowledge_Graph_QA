# coding; utf-8
from text_clf.model import SentenceFunClf
from pattern.pattern_match import PatternMatch

import jieba
import numpy as np


class IntentRecognizer(object):
    '''
    @usage:	
        Define the Intent Recognizer
    '''

    def __init__(self):
        '''
        @usage:
            init two classfiers, load the patterns of each intent branch
        '''
        self.sen_fun_clf = SentenceFunClf('sen_fun')
        self.ques_type_clf = SentenceFunClf('ques_type')
        self.matcher = PatternMatch()

    def load_model(self):
        '''
        @usage: load the xgb model
        '''
        self.sen_fun_clf.load_model()
        self.ques_type_clf.load_model()

    def intent_clf(self, sentence):
        '''
        @usage: return the 
        @param: 
            sentence:	(string) original sentence
        @return:
            the intent classification, 0 for search, 1 for check 
        '''
        cut_sen = ' '.join(jieba.lcut(sentence))
        probs_sen_fun = self.sen_fun_clf.predict(cut_sen)

        intent_flg = 0
        if np.argmax(probs_sen_fun) == 0:
            probs_ques_type = self.ques_type_clf.predict(cut_sen)
            if probs_ques_type[0] > 0.5:
                intent_flg = 1

        return intent_flg

    def pattern_match(self, intent_flg, sentence, ner_type_list):
        '''

        '''

        intent_branch = self.matcher.match(sentence, intent_flg, ner_type_list)

        return intent_branch


if __name__ == '__main__':
    recognizer = IntentRecognizer()
    recognizer.load_model()
    test_list = [['我妈得了癌症能买吗', 1],
                 ['这个产品的犹豫期是多久', 0],
                 ['平安福的投保年龄', 0],
                 ['福满分都保障哪些疾病', 0],
                 ['我爸爸60岁了能投保吗？', 1],
                 ['这款产品的等待期是多少', 0],
                 ['平安福每年需要交多少钱', 0],
                 ['我去年做过手术可以买重疾险吗', 1],
                 ['我买这个可以保障多久', 0]]

    wrong_num = 0
    for sample in test_list:
        res = recognizer.intent_clf(sample[0])
        if res != sample[1]:
            print("wrong sample:", sample[0])
            wrong_num += 1
    print("wrong clf: {} out of {}".format(wrong_num, len(test_list)))




