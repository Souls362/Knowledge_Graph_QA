# coding: utf-8

class Config(object):
    def __init__(self):
        self.config_dict = {
            'sen_fun':{
                'data': {
                    'corpus_path': 'data',
                    'sen_file': 'weibo_pair_train_pattern.response',
                    'label_file': 'weibo_pair_train_pattern.label',
                    'tfidf_vectorizer_path': 'model_sen_fun/tfidf_vectorizer.model',
                },
                'model': {
                    'max_depth': '[4, 5, 6]',
                    'eta': '[0.1, 0.05, 0.02]',
                    'subsample': '[0.5, 0.7, 1.0]',
                    'max_iterations': '50',
                    'objective': '["multi:softmax"]',
                    'silent': '[1]',
                    'num_boost_round': '2000',
                    'nfold': '5',
                    'num_class':'[3]',
                    'stratified': '1',
                    'metrics': 'merror',
                    'early_stopping_rounds': '50',
                    'model_path': 'model_sen_fun/{}.model'
                }
            },
            'ques_type':{
                'data': {
                    'corpus_path': 'data',
                    'sen_file': 'ques_clf.txt',
                    'label_file': '',
                    'tfidf_vectorizer_path': 'model_ques_type/tfidf_vectorizer.model',
                },
                'model': {
                    'max_depth': '[4, 5, 6]',
                    'eta': '[0.1, 0.05, 0.02]',
                    'subsample': '[0.5, 0.7, 1.0]',
                    'max_iterations': '50',
                    'objective': '["binary:logistic"]',
                    'silent': '[1]',
                    'num_boost_round': '2000',
                    'nfold': '5',
                    'num_class':'[]',
                    'stratified': '1',
                    'metrics': 'error',
                    'early_stopping_rounds': '50',
                    'model_path': 'model_ques_type/{}.model'
                }
            }
        }   

    def get(self, clf_flag, section_name, arg_name):
        return self.config_dict[clf_flag][section_name][arg_name]   

