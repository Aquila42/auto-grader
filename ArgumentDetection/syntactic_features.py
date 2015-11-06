from generate_syntactic_features import SyntacticFeatures
from generate_lexical_features import LexicalFeatures
from generate_indicator_features import IndicatorFeatures

file_type = "train"

input_tree = open("data/essay.all.arguments.0617.txt."+file_type+".consttree","r")
input_sent = open("data/essay.all.arguments.0617.txt."+file_type,"r")
input_production_tree = open("data/essay.all.arguments.0617.txt."+file_type+".consttree.productions","r")

output_file = open("data/features_"+file_type,"w")
names = open("data/feature_names","w")

argument = []
input_tree.readline()
clauses = []
for line in input_tree:
    temp = line.split("\t")
    clauses.append(temp[3])
    argument.append(temp[2])

input_sent.readline()
sents = []
for line in input_sent:
    temp = line.split("\t")
    sents.append([temp[3],temp[4]])

input_production_tree.readline()
production_trees = []
for line in input_production_tree:
    production_trees.append(line.split("\t")[3][1:-2].strip().split(","))

synFeat = SyntacticFeatures()
lexFeat = LexicalFeatures()
indicatorFeat = IndicatorFeatures()

features = {}
feature_numbers = {"SUB-CLAUSES":"20", "DEPTH": "21", "PROD_TREE":"22", "PRESENT_TENSE":"23",
                   "MODAL": "30", "VERBS": "31", "ADVERBS":"32", "N-GRAMS":"33",
                   "DISCOURSE":"40","FIRST_PERSON":"41"}

if len(clauses) != len(sents):
    print "Error: consttree and file do not match"
    exit()

for i in range(len(clauses)):
    clause = clauses[i]
    sent = sents[i]
    arg = argument[i]

    #Syntactic Features
    features["SUB-CLAUSES"] = synFeat.get_subclauses(clause)

    features["DEPTH"] = synFeat.get_depth(clause)

    #Production rules

    #Present tense of the main verb
    #Dependency parser
    #without Modal verbs
    features["PRESENT_TENSE"] = synFeat.is_present_tense(clause)

    #Create unigram, bigram and trigram files - with index - frequency distribution (dictionary of word:frequency)
    #Remove stop words
    #features["N-GRAMS"] = lexFeat.get_ngrams(sent[1])


    #Lexical Features
    features["MODAL"] = lexFeat.get_modal_verbs(clause)

    features["VERBS"] = lexFeat.get_verbs(clause)

    features["ADVERBS"] = lexFeat.get_adverbs(clause)

    features["MODAL"] = lexFeat.get_modal_verbs(clause)

    #Indicator Features
    features["DISCOURSE"] = indicatorFeat.get_discourse_marker(sent[0])
    #Boolean for each discourse marker

    features["FIRST_PERSON"] = indicatorFeat.get_first_person(sent[1])

    output_file.write(str(arg)+"\t")
    for key in features:
        output_file.write(feature_numbers[key]+":"+str(features[key])+"\t")
    output_file.write("\n")

output_file.close()
for name in feature_numbers:
    names.write(name+":"+str(feature_numbers[name])+"\n")
names.close()