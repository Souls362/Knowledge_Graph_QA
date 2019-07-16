import jieba
import demjson

def split_analyzer(x):
    return x.split()

def load_json(text):
    return demjson.decode(text, encoding='utf-8')


