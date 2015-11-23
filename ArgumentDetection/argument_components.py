from generate_syntactic_features import SyntacticFeatures
from generate_lexical_features import LexicalFeatures
from generate_indicator_features import IndicatorFeatures
from generate_structural_features import StructuralFeatures

class EssayClassifier:

    def __init__(self):
        file_type = "train"
        self.features_list = []
        self.features = {}
        self.read_files(file_type)

    def read_files(self, file_type):
        input_tree = open("data/essay.all.arguments.0617.txt."+file_type+".consttree","r")
        input_sent = open("data/essay.all.arguments.0617.txt."+file_type,"r")
        input_production_tree = open("data/essay.all.arguments.0617.txt."+file_type+".consttree.productions","r")

        self.output_file = open("data/features_"+file_type,"w")
        self.names = open("data/feature_names","w")

        argument = []
        input_tree.readline()
        clauses = []
        for line in input_tree:
            temp = line.split("\t")
            clauses.append(temp[3])
            argument.append(temp[2])

        self.clauses = clauses
        self.argument = argument

        input_sent.readline()
        sents = []
        for line in input_sent:
            temp = line.split("\t")
            sents.append([temp[3],temp[4],temp[6]])

        self.sents = sents

        input_production_tree.readline()
        production_trees = []
        for line in input_production_tree:
            production_trees.append(line.split("\t")[3][1:-2].strip().split(","))

    def structural_features(self,sent):
        #sent = (argument component, covering sentence)
        structFeat = StructuralFeatures()
        features = ["ARG_TOKENS","COVERING_TOKENS","TOKEN_RATIO","TOKEN_STAT","PRECEDING_TOKENS","FOLLOWING_TOKENS","INTRO","COVERING_POS","ARG_PUNCT","COVERING_PUNCT","PRECEDING_PUNCT","FOLLOWING_PUNCT","QUESTION"]
        self.features_list.extend(features)
        # get_tokens_count() returns float
        self.features[features[0]] = structFeat.get_tokens_count(sent[0])
        self.features[features[1]] = structFeat.get_tokens_count(sent[1])
        #number of tokens preceding and following an argument component in the covering sentence
        self.features[features[2]] = self.features[features[1]]/self.features[features[0]]
        if self.features[features[0]] == self.features[features[1]]:
            self.features[features[3]] = 1
        else:
            index = sent[1].find(sent[0])
            if index != -1:
                preceding_sent = sent[1][:index]
                following_sent = sent[1][index+len(sent[0]):]
                self.features[features[4]] = structFeat.get_tokens_count(preceding_sent)
                self.features[features[10]] = structFeat.get_punctuation_count(preceding_sent)
                self.features[features[5]] = structFeat.get_tokens_count(following_sent)
                self.features[features[11]] = structFeat.get_punctuation_count(following_sent)
            self.features[features[3]] = 0
        if int(sent[2]) <= 5:
            self.features[features[6]] = 1
        else:
            self.features[features[6]] = 0
        self.features[features[7]] = sent[2].strip()
        self.features[features[8]] = structFeat.get_punctuation_count(sent[0])
        self.features[features[9]] = structFeat.get_punctuation_count(sent[1])
        if sent[1].strip()[-1] == "?":
            self.features[features[12]] = 1
        else:
            self.features[features[12]] = 0

    def syntactic_features(self,clause):
        #Syntactic Features
        synFeat = SyntacticFeatures()
        features = ["SUB-CLAUSES","DEPTH","PRESENT_TENSE"]
        self.features_list.extend(features)
        self.features[features[0]] = synFeat.get_subclauses(clause)
        self.features[features[1]] = synFeat.get_depth(clause)
        self.features[features[2]] = synFeat.is_present_tense(clause)

    def lexical_features(self,clause,sent):
        #Lexical Features
        lexFeat = LexicalFeatures()
        features = ["MODAL","VERBS","ADVERBS"]
        self.features_list.extend(features)
        self.features[features[0]] = lexFeat.get_modal_verbs(clause)
        self.features[features[1]] = lexFeat.get_verbs(clause)
        self.features[features[2]] = lexFeat.get_adverbs(clause)
        self.features,features = lexFeat.get_ngrams(sent[1],self.features)
        self.features_list.extend(features)

    def indicator_features(self,sent):
        #Indicator Features
        indicatorFeat = IndicatorFeatures()
        features = ["DISCOURSE","FIRST_PERSON"]
        self.features_list.extend(features)
        self.features[features[0]] = indicatorFeat.get_discourse_marker(sent[0])
        self.features[features[1]] = indicatorFeat.get_first_person(sent[1])


    def populate_features(self):

        if len(self.clauses) != len(self.sents):
            print "Error: consttree and file do not match"
            exit()

        for i in range(len(self.clauses)):
            clause = self.clauses[i]
            sent = self.sents[i]
            arg = self.argument[i]

            self.structural_features(sent)
            self.lexical_features(clause,sent)
            self.syntactic_features(clause)
            self.indicator_features(sent)

            self.output_file.write(str(arg)+"\t")
            for i in range(len(self.features_list)):
                key = self.features_list[i]
                self.output_file.write(key+":"+str(self.features[key])+"\t")
            self.output_file.write("\n")
        self.output_file.close()
        for i in range(len(self.features_list)):
            self.names.write(str(i)+":"+str(self.features_list[i])+"\n")
        self.names.close()

e = EssayClassifier()
e.populate_features()