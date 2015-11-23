import nltk

class SyntacticFeatures:
    def __init__(self):
        self.POSList = ["SBAR","SBARQ","SINV","SQ","S","FRAG"]
        self.PresentList = ["VBP","VBZ"]
        self.PastList = ["VBD"]

    def get_subclauses(self,clause):
        subclause_count = 0
        pos_index = 0
        while clause.find(self.POSList[pos_index]) == -1:
            pos_index +=1
            if pos_index == len(self.POSList):
                return 0
        if pos_index < len(self.POSList):
            index = clause.find(self.POSList[pos_index])
            while index != -1:
                subclause_count += 1
                index = clause.find("("+self.POSList[pos_index],index+1)
            return float(subclause_count)

    def get_depth(self,clause):
        max_depth = 0
        depth = -1
        for char in clause:
            if char == "(":
                depth += 1
            elif char == ")":
                if max_depth < depth:
                    max_depth = depth
                depth -= 1
        return float(max_depth)

    def is_present_tense(self,clause):
        verb_index = clause.find("(VP")
        main_verb = clause.find("(V",verb_index+1)
        if main_verb > -1:
            if clause[main_verb:clause.find(" ",main_verb)] in self.PresentList:
                return 1
        return 0



