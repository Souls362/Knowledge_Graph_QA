


class result_modify(object):

    def __init__(self):
        self.output = '你好，'

    def run(self, intent, ner, result):
        if result == None:
            self.output = '不好意思，该问题暂时无法回答，请核实输入信息'
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
            self.output = self.output + ner['product_name'] + '疾病保障范围包含' + str(result)

        # if intent == '16':
        #     self.output = self.output + ner['product_name'] + '疾病保障范围包含' + str(result)
        # if intent == '16':
        #     self.output = self.output + ner['product_name'] + '疾病保障范围包含' + str(result)
        # if intent == '16':
        #     self.output = self.output + ner['product_name'] + '疾病保障范围包含' + str(result)
        return self.output



