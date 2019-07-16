


class result_modify(object):

    def __init__(self):
        pass

    def run(self, intent, ner, result):
        self.output = '你好，'
        if result == None:
            self.output = '不好意思，该问题暂时无法回答，请核实输入信息'
            return self.output
        if intent == '11':
            self.output = self.output + ner['product_name'] + '的价格是' + str(result) + '元'
        if intent == '12':
            self.output = self.output + ner['product_name'] + '的投保年龄范围是' + str(result) + '岁'
        if intent == '13':
            self.output = self.output + ner['product_name'] + '的犹豫期是' + str(result) + '天'
        if intent == '14':
            self.output = self.output + ner['product_name'] + '的等待期是' + str(result) + '天'
        if intent == '15':
            self.output = self.output + ner['product_name'] + '保障期限是' + str(result) + '年'
        if intent == '16':
            self.output = self.output + ner['product_name'] + '疾病保障范围包含' + ' ' +','.join(result)
        if intent == '21':
            if result == True:
                self.output = self.output + '该年龄符合' + ner['product_name'] + '购买条件'
            if result == False:
                self.output = self.output + '该年龄不符合' + ner['product_name'] + '购买条件'
        if intent == '230':
            if 'default_answer' in result[0]:
                self.output = self.output + '请问' + result[0]['default_answer']
        if intent == '231' or intent == '232':
            if 'default_answer' in result[0]:
                self.output = self.output + '请问' + result[0]['default_answer']
            else:
                self.output = self.output + '根据你的情况，审核建议为: ' + result[0]['name']
        if intent == '31' or intent == '41':
            if result == []:
                self.output = self.output + '抱歉暂时没有符合该条件的产品'
            else:
                self.output = self.output + ' ' + ','.join(result) + '满足购买条件'
        # if intent == '16':
        #     self.output = self.output + ner['product_name'] + '疾病保障范围包含' + str(result)
        # if intent == '16':
        #     self.output = self.output + ner['product_name'] + '疾病保障范围包含' + str(result)
        # if intent == '16':
        #     self.output = self.output + ner['product_name'] + '疾病保障范围包含' + str(result)
        return self.output



