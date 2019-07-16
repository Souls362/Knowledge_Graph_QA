#coding:utf-8
'''
    This file defines the model of text classification base on xgboost
'''
import xgboost as xgb
import numpy as np
from sklearn.model_selection import ParameterGrid
from sklearn.externals import joblib
from text_clf.processor import Processor
from text_clf.config import Config
from text_clf.utils import load_json


class SentenceFunClf(object):
    def __init__(self, clf_flag):
        '''
        @usage: 
            Initilaize the classifer
        @param:
            clf_flag:   (string) The flag of classifcation kind to search the config {"ques_type", "sen_fun"}
    
        ''' 
        self.config = Config()
        self.clf_flag = clf_flag
        self.corpus = Processor(self.config, self.clf_flag)
        self.vectorizer = None
        self.model = None
        self.params = {}


    def setup_model(self):
        '''
        @usage:
            prepare the data and parameters for the xgboost model
        '''
        self.corpus.generator()
        self.train_matrix = xgb.DMatrix(self.corpus.sparse_vector, label=self.corpus.labels)
        self.params['max_depth']= load_json(self.config.get(self.clf_flag, 'model', 'max_depth'))
        self.params['eta'] = load_json(self.config.get(self.clf_flag, 'model', 'eta'))
        self.params['subsample'] = load_json(self.config.get(self.clf_flag, 'model', 'subsample'))
        self.params['objective'] = load_json(self.config.get(self.clf_flag, 'model', 'objective'))
        self.params['silent'] = load_json(self.config.get(self.clf_flag, 'model', 'silent'))
        self.params['num_boost_round'] = load_json(self.config.get(self.clf_flag, 'model', 'num_boost_round'))
        self.params['num_class'] = self.config.get(self.clf_flag, 'model', 'num_class')
        self.params['nfold'] = load_json(self.config.get(self.clf_flag, 'model', 'nfold'))
        self.params['stratified'] =True if int(self.config.get(self.clf_flag, 'model', 'stratified')) else False
        self.params['metrics'] = self.config.get(self.clf_flag, 'model', 'metrics')
        self.params['early_stopping_rounds'] = int(self.config.get(self.clf_flag, 'model', 'early_stopping_rounds'))


    def param_select(self, best_flg):
        '''
        @usage:
            param grid search for the
        @param:
            best_flg: (int){-1,1} indicate whether the metric is positive or negative(1 best or 0 best).
        @return:
            best metric, param and iter round
        '''
        params = {'max_depth': self.params['max_depth'],
                  'eta': self.params['eta'],
                  'subsample': self.params['subsample'],
                  'objective': self.params['objective'],
                  'silent': self.params['silent']}
        
        if self.clf_flag=='sen_fun':
            params['num_class']=[3]
        
        best_metric, best_param, best_iter_round = - 1 * best_flg, {}, 0
        
        param_grid = ParameterGrid(params)

        for i, param in enumerate(param_grid):
            print(i)
            cv_result = xgb.cv(param, self.train_matrix,
                               num_boost_round=self.params['num_boost_round'],  # max iter round
                               nfold=self.params['nfold'],
                               stratified=self.params['stratified'],
                               metrics=self.params['metrics'],  # metrics focus on
                               early_stopping_rounds=self.params['early_stopping_rounds'])  # stop when metrics not get better
            cur_metric = cv_result.ix[len(cv_result)-1, 0]
            cur_iter_round = len(cv_result)
            if (cur_metric - best_metric) * best_flg > 0:
                best_metric, best_param, best_iter_round = cur_metric, param, cur_iter_round

            print('Param select {}, {}: {}, iter_round: {}, params: {}, now best {}: {}'
                  .format(i, self.params['metrics'], cur_metric, cur_iter_round, param, self.params['metrics'], best_metric))

        return best_param, best_iter_round


    def train(self, best_flg, model_name='xgb_model'):
        '''
        @usage: train and save the xgboost model based on the best param
        '''
        self.setup_model()
        best_param, best_iter_round= self.param_select(best_flg)
        print(best_param)
        self.model = xgb.train(dtrain=self.train_matrix, params=best_param, num_boost_round=best_iter_round)
        self.save_model(model_name)


    def save_model(self, name='xgb_model'):
        '''
        @usage: save the xgboost model
        '''
        model_path = self.config.get(self.clf_flag, 'model', 'model_path').format(name)
        joblib.dump(self.model, model_path)


    def load_model(self, name='xgb_model', model='model'):
        model_path = self.config.get(self.clf_flag, 'model','model_path').format(name)
        self.__dict__[model]= joblib.load(model_path)


    def transform(self, sentence):
        if not self.vectorizer:
            self.load_model('tfidf_vectorizer', 'vectorizer')
        feature_matrix = self.vectorizer.transform([sentence])
        return xgb.DMatrix(feature_matrix)


    def predict(self, sentence):
        if not self.model:
            self.load_model()
        feature_matrix = self.transform(sentence)
        prob = self.model.predict(feature_matrix)
        return prob


# class IntentRecognition(object):
#   def __init__(self, ner_list):
#       self.pattern_dict = {}
#       self.config = get_config()
#       self.ner_list = ner_list
#       self.sen_clf = sen_clf

#   def read_pattern(self, pattern_file):
#       with open(pattern_file, 'r', encoding='utf-8') as f:
#           self.pattern_dict = json.load(f)

#   def match_pattern(self, sentence, pattern):
                        

#   def intent_clf(self, cut_sentence):
#       for()       

