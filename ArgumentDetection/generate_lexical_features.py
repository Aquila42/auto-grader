from nltk import bigrams,trigrams
class LexicalFeatures:
    def __init__(self):
        self.VerbList = ["VP","VB","VBD","VBG","VBN","VBP","VBZ"]
        self.AdverbList = ["ADVP","WHAVP","RB","RBR","RBS","WRB"]
        self.Modal = "MD"

    def count_tag(self,tag,clause):
        index = clause.find(tag)
        count = 0
        while index != -1 and index < len(clause):
            count += 1
            index = clause.find("("+tag,index+1)
        return float(count)

    def get_verbs(self,clause):
        count = 0
        for item in self.VerbList:
            count += self.count_tag(item,clause)
        return float(count)

    def get_adverbs(self,clause):
        count = 0
        for item in self.AdverbList:
            count += self.count_tag(item,clause)
        return float(count)

    def get_modal_verbs(self,clause):
        return self.count_tag(self.Modal,clause)

    def get_ngrams(self,clause):
        print bigrams(clause)
        print trigrams(clause)
