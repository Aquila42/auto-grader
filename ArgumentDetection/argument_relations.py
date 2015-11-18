from generate_syntactic_features import SyntacticFeatures
from generate_lexical_features import LexicalFeatures
from generate_indicator_features import IndicatorFeatures

file_type = "train"

input_sent = open("data/essay.all.arguments.claim.premise.4lines.1106.txt","r")
output_file = open("data/argument_relations_features_"+file_type,"w")
names = open("data/arg_rel_feature_names","w")

features = {}
feature_numbers = { "TOKENS_S":"10A", "TOKENS_T":"10B", "TOKEN_DIFFERENCE":"10" #Syntactic Features
                                 #Lexical features
                   }                                      #Indicator features

synFeat = SyntacticFeatures()
lexFeat = LexicalFeatures()
indicatorFeat = IndicatorFeatures()

input_sent.readline()
sents = []
for line in input_sent:
    sents.append(line.split("\t"))

for i in range(len(sents)):
    relation = sents[i][1]
    source = sents[i][2]
    target = sents[i][3]

    #Syntactic Features
    features["TOKENS_S"] = synFeat.get_tokens(source)
    features["TOKENS_T"] = synFeat.get_tokens(source)
    features["TOKEN_DIFFERENCE"] = abs(len(features["TOKENS_S"]) - len(features["TOKENS_T"]))

    #Lexical Features

    #Indicator Features


    output_file.write(str(relation)+"\t")
    for key in features:
        output_file.write(feature_numbers[key]+":"+str(features[key])+"\t")
    output_file.write("\n")

output_file.close()
for name in feature_numbers:
    names.write(name+":"+str(feature_numbers[name])+"\n")
names.close()