import re
from datetime import time

class result_trans(object):

    def __init__(self):
        self.num_dict={"一":"1","二":'2',"三":"3","四":"4","五":"5","六":"6","七":"7","八":"8","九":"9","两":"2","俩":"2",
          '壹': '1', '贰': '2', '叁': '3', '肆': '4','伍': '5', '陆': '6', '柒': '7', '捌': '8', '玖': '9'}

        self.chs_arabic_map = {'零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
                      '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
                      '十': 10, '百': 100, '千': 10 ** 3, '万': 10 ** 4,
                      '〇': 0, '壹': 1, '贰': 2, '叁': 3, '肆': 4,
                      '伍': 5, '陆': 6, '柒': 7, '捌': 8, '玖': 9,
                      '拾': 10, '佰': 100, '仟': 10 ** 3, '萬': 10 ** 4,
                      '亿': 10 ** 8, '億': 10 ** 8, '幺': 1, '两': 2,
                      '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
                      '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}

    def convertChineseDigitsToArabic(self,chinese_digits):
        result = 0
        tmp = 0
        hnd_mln = 0
        chinese_digits = chinese_digits
        for count in range(len(chinese_digits)):
            curr_char = chinese_digits[count]
            curr_digit = self.chs_arabic_map.get(curr_char, None)
            # meet normal char
            if curr_digit is None:
                pass
            # meet 「亿」 or 「億」
            elif curr_digit == 10 ** 8:
                result = result + tmp
                result = result * curr_digit
                # get result before 「亿」 and store it into hnd_mln
                hnd_mln = hnd_mln * 10 ** 8 + result
                result = 0
                tmp = 0
            # meet 「万」 or 「萬」
            elif curr_digit == 10 ** 4:
                result = result + tmp
                result = result * curr_digit
                tmp = 0
            # meet 「十」, 「百」, 「千」 or their traditional version
            elif curr_digit >= 10:
                tmp = 1 if tmp == 0 else tmp
                result = result + curr_digit * tmp
                tmp = 0
            # meet single digit
            else:
                tmp = tmp * 10 + curr_digit

        result = result + tmp
        result = result + hnd_mln
        return str(result)

    def textwash(self,text):
        stopword = u''':!),.:;?]}¢'"、。〉》」』】〕〗〞︰︱︳﹐､﹒﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠々‖•·ˇˉ―--′’”([{£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻︽︿﹁﹃﹙﹛﹝（｛“‘-—_…'''
        for it in stopword:
            text = text.replace(it, "")
        text = text.replace("\n", "")
        text = text.replace("\r", "")
        text = text.replace(" ", "")
        return text

    def formalize(self,result):
        for k,v in result.items():
            if k == "age":
                if v == "":
                    continue
                v_list = []
                for it in v.split("@@"):
                    res = re.findall("(\d+)年", it)
                    if res:
                        num = int(res[0])
                        if num < 100: num += 1900
                        strings = time.strftime("%Y,%m,%d,%H,%M,%S")
                        t = strings.split(',')
                        cur_year = [int(x) for x in t][0]
                        age_val = cur_year - num
                        v_list.append(str(age_val))
                        continue
                    rr = self.convertChineseDigitsToArabic(it)
                    v_list.append(rr)
                result[k] = "@@".join(v_list)
            if k == "insurance":
                if v:
                    if "没" in v or "未" in v or "无" in v or "要买" in v:
                        self.result[k] = "无社保"
                        continue
                    result[k] = "有社保"
            if k == "kids":
                if v:
                    if "没" in v or "无" in v:
                        self.result[k] = "无孩"
                        continue
                    result[k] = "有孩"
            if k == "marriage":
                if v:
                    if "单身" in v or "未" in v or "没" in v or "朋友" in v:
                        self.result[k] = "未婚"
                        continue
                    if "离" in v:
                        self.result[k] = "离婚"
                        continue
                    result[k] = "已婚"
            if k == "money" and v != "":
                if v == "":
                    continue
                v_list = []
                for it in v.split("@@"):
                    it = self.pad(it)
                    nn = self.convertChineseDigitsToArabic(it)
                    w = int(nn)/10000
                    vv = str(w)+"万"
                    if "月" in it:
                        vv = "月薪是:" + vv
                    v_list.append(vv)
                result[k] = "@@".join(v_list)

        return result

    def pad(self, text):
        # 补全类似"一万二"中缺少的量词"千"
        real_pat = [(r"\d万\d", "千"), (r"\d千\d", r"百")]
        for a,b in real_pat:
            res = re.findall(a, text)
            if res:
                val = res[0] + b
                text = text.replace(res[0], val)
                break
        return text

    def run(self, ner_result):
        result = self.formalize(ner_result)
        return result

if __name__ == '__main__':
    result_trans = result_trans()
    result = result_trans.run({'age':'二十五岁','money':'五百二十'})
    print(result)