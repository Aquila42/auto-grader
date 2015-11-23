from nltk import bigrams,trigrams,word_tokenize
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
        index = clause.find("("+tag+" ")
        count = 0
        while index != -1 and index < len(clause):
            count += 1
            index = clause.find("("+tag+" ",index+1)
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
        list_x = []
        for word in x_list:
            if word in y_list:
                list_x.append(word)
        return list_x

    def get_ngrams(self,sent,features_dict):
        sent_list = word_tokenize(sent)
        features_list = []
        features_list.extend(self.check_belonging(sent_list,self.Unigrams))
        sent_list = bigrams(sent)
        features_list.extend(self.check_belonging(sent_list,self.Bigrams))
        sent_list = trigrams(sent)
        features_list.extend(self.check_belonging(sent_list,self.Trigrams))
        for word in features_list:
            features_dict[word] = 1
        return features_dict,features_list
