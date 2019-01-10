import yara
import os

from core.bom import Software


class RuleManager(object):

    def __init__(self, rulepath):
        self.technique_rules, self.num_tec_rule = self.__load_rules(rulepath)
        self.software_rules, self.num_sw_rule = self.__generate_rules(Software.query.all())
        print("YARA Rules loaded (Techniques: {}, Software: {})".format(self.num_tec_rule, self.num_sw_rule))

    @staticmethod
    def __load_rules(rulepath):
        filepaths = {rulefile: os.path.join(rulepath, rulefile)
                           for rulefile in os.listdir(rulepath) if rulefile.endswith(".yar")}

        return yara.compile(filepaths=filepaths, error_on_warning=True), filepaths.__len__()

    @staticmethod
    def __generate_rules(ruledata):
        sources = {str(rule.id): "rule software" + str(rule.id) +
                                 " { meta: software = \"" + rule.name + "\" strings: $regex = /" +
                                 rule.name + "/ nocase condition: $regex }" for rule in ruledata}

        return yara.compile(sources=sources, error_on_warning=True), sources.__len__()

    def match_data(self, data):
        matches = self.software_rules.match(data=data)
        matches += self.technique_rules.match(data=data)
        return matches

    def match_file(self, file):
        matches = self.software_rules.match(file=file)
        matches += self.technique_rules.match(file=file)
        return matches
