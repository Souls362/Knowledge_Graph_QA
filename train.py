from text_clf.model import SentenceFunClf
 
class Trainer(object):
    def __init__(self, clf_flag):
        self.clf_flag = clf_flag
                
    def train(self):
        model = SentenceFunClf(self.clf_flag)
        model.train(best_flg=-1)


if __name__ == '__main__':
    sen_fun_trainer = Trainer('sen_fun')
    print("sen_fun trainer created")
    
    ques_type_trainer = Trainer('ques_type')
    print("ques_type trainer created")

    ques_type_trainer.train()
    print("ques_type model saved")

    sen_fun_trainer.train()
    print("sen_fun model saved")
    

