import yara
import os

from core.bom import Software


class RuleManager(object):

    def __init__(self, rulepath):
        self.technique_rules = self.__compile_rules(rulepath)
        self.software_rules = self.__generate_rules(Software.query.all())

    @staticmethod
    def __compile_rules(rulepath):

        yara_rule_files = {rulefile: os.path.join(rulepath, rulefile)
                           for rulefile in os.listdir(rulepath) if rulefile.endswith(".yar")}

        rules = yara.compile(filepaths=yara_rule_files, error_on_warning=True)
        print("YARA rules compiled successfully")

        return rules

    @staticmethod
    def __generate_rules(ruledata):

        sources = {rule.name: "rule " + rule.name +
                              " { strings: $regex = /" + rule.name + "/ nocase condition: $regex }"
                   for rule in ruledata}

        rules = yara.compile(sources=sources, error_on_warning=True)
        print("YARA rules generated successfully")

        return rules

    def match_techniques(self, data):
        return self.technique_rules.match(data=data)

    def match_software(self, data):
        return self.software_rules.match(data=data)
