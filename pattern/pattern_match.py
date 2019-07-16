import demjson
import json


class PatternConfig(object):
    def __init__(self):
        self.pattern_file = "pattern/patterns.json"
        with open(self.pattern_file, "r", encoding='utf-8') as f:
            self.pattern_dict = json.load(f)

    def get_components(self, components_type):
        return self.pattern_dict["components"][components_type]

    def get_pattern(self, ques_type_clf):
        candidate_patterns = self.pattern_dict['pattern'][ques_type_clf]
        return candidate_patterns


class PatternMatch(object):
    def __init__(self):
        self.pattern_config = PatternConfig()
        self.intent_clf_mapping = {0: "attributes", 1: "check"}

    def match(self, sentence, intent_clf, ner_type_list):
        '''
		@usage:
			match the pattern of the sentence and return the intention branch
		@param:
			sentence: (string) original sentence
			intent_clf: {0 for Attributes search, 1 for check}
		'''
        candidates = self.pattern_config.get_pattern(self.intent_clf_mapping[intent_clf])

        find_branch = False
        match_branch = None

        for branch in candidates:
            components = candidates[branch]['components']
            req_ners = candidates[branch]['ner']

            components_achived = True
            ner_achived = True

            ner_not_contain = [False for x in req_ners if x not in ner_type_list]

            if ner_not_contain:
                ner_achived = False

            for attribute in components:
                attribute_achived = False

                if attribute in ner_type_list:
                    attribute_achived = True
                else:
                    attribute_contain = [True for key_word in self.pattern_config.get_components(attribute) if
                                         key_word in sentence]
                    if attribute_contain:
                        attribute_achived = True

                components_achived = components_achived and attribute_achived

                if not attribute_achived:
                    break

            if components_achived and ner_achived:
                find_branch = True
                match_branch = branch
                break

        if find_branch:
            return candidates[match_branch]['ambiguous']
        else:
            return "null_intent"
