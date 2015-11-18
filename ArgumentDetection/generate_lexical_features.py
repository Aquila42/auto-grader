from nltk import bigrams,trigrams
class LexicalFeatures:
    def __init__(self):
        self.VerbList = ["VP","VB","VBD","VBG","VBN","VBP","VBZ"]
        self.AdverbList = ["ADVP","WHAVP","RB","RBR","RBS","WRB"]
        self.Modal = "MD"
        self.Unigrams = self.read_from_file("data/unigrams")
        self.Bigrams = self.read_from_file("data/bigrams")
        self.Trigrams = self.read_from_file("data/trigrams")

    def read_from_file(self,filename):
        f = open(filename,"r")
        x_grams = []
        for line in f:
            x_grams.append(line.split("\t")[0])
        f.close()
        return x_grams

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

    def check_belonging(self,x_list,y_list):
        for word in x_list:
            if word in y_list:
                return True
        return False

    def get_ngrams(self,clause):
        clause_list = clause.split()
        if self.check_belonging(clause_list,self.Unigrams) or self.check_belonging(bigrams(clause_list),self.Bigrams) or self.check_belonging(trigrams(clause_list),self.Trigrams):
            return 1
        return 0