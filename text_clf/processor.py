#coding:utf-8

'''
    This file defines the processor class which is responsible for data loading, 
    segmenting, vectorizing and traing set preparation. 
'''

import numpy as np
from numpy import random
import jieba
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.externals import joblib
from text_clf.utils import split_analyzer
from text_clf.config import Config


class Processor(object):
    def __init__(self, config, clf_flag):
        '''
        @usage:         
            init Processor and load params
        @param:
            config:     (class instance) the config class containing configuration
            clf_flag:   (string) The flag of classifcation kind to search the config {"ques_type", "sen_fun"}
        '''

        self.config = config
        self.clf_flag = clf_flag
        self.sentences = []
        self.labels =[]
        self.cut_sens = []
        self.join_sens = []
        self.sparse_vector = None


    def data_loader(self):
        '''
        @usage:     
            load the sentences and labels to pocessor
        @return:    
            (1d list) labels, sentences 
        ''' 

        file_path = self.config.get(self.clf_flag, "data", "corpus_path")
        sen_file = self.config.get(self.clf_flag, "data", "sen_file")
        label_file = self.config.get(self.clf_flag, "data", "label_file")

        if self.clf_flag == 'ques_type':
            with open(os.path.join(file_path, sen_file), 'r', encoding='utf-8') as f:
                combs = [line.strip().split('\t') for line in f.readlines()]
            random.shuffle(combs)
            
            self.sentences = [line[1] for line in combs]
            self.labels = [int(line[0]) for line in combs]


        if self.clf_flag == 'sen_fun':
            with open(os.path.join(file_path, sen_file), 'r', encoding='utf-8') as f:
                self.sentences = [line.strip() for line in f.readlines()]

            with open(os.path.join(file_path, label_file), 'r', encoding='utf-8') as f:
                double_labels = [line.strip().split() for line in f.readlines()]
                for i in range(min(len(self.sentences), 1000)): # Only get the first 10000 lines
                    self.labels.append(np.argmax(double_labels[i * 2]))

            self.sentences = self.sentences[:1000]
        #  return self.labels, self.sentences


    def sen_segment(self):
        # The sen_fun corpus alreay tokenized so only segment the ques_type corpus 
        '''
        @usage:
            Tokenize the sentence 

        @param:
            corpus: 1d list, list of sentences
        
        @return:
            segmented_corpus: 2d list, list of sentences
        ''' 
        if self.clf_flag == 'ques_type':   
            for i, sen in enumerate(self.sentences):
                cut_sen = jieba.lcut(sen)
                join_sen = ' '.join(cut_sen)
                self.cut_sens.append(cut_sen)
                self.join_sens.append(join_sen)
        else:
            self.join_sens = self.sentences


    def feature_extract(self, tfidf_save=True):
        '''
        @usage:
            vectorize the sentences with sklearn tfidf vectorizer
        @param:
            tfidf_save:   (bool) whether save the tfidf matrix
        '''
        vectorizer = TfidfVectorizer(smooth_idf=True,
                                     analyzer=split_analyzer,
                                     ngram_range=(1, 1),
                                     min_df=1, norm='l1')

        self.sparse_vector = vectorizer.fit_transform(self.join_sens)
        if tfidf_save:
            joblib.dump(vectorizer, self.config.get(self.clf_flag, 'data', 'tfidf_vectorizer_path'))


    def generator(self):
        self.data_loader()
        self.sen_segment()
        self.feature_extract()
    