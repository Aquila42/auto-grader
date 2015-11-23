from generate_syntactic_features import SyntacticFeatures
from generate_lexical_features import LexicalFeatures
from generate_indicator_features import IndicatorFeatures
from generate_structural_features import StructuralFeatures

file_type = "train"

input_sent = open("data/essay.all.arguments.claim.premise.4lines.1106.txt","r")
output_file = open("data/argument_relations_features_"+file_type,"w")
names = open("data/arg_rel_feature_names","w")

features = {}
feature_numbers = { "TOKENS_S":"10A", "TOKENS_T":"10B", "TOKEN_DIFFERENCE":"10", "PUNC_S":"11A", "PUNC_T":"11B", "PUNC_DIFFERENCE":"11", "POSITION_S":"12A", "POSITION_T":"12B", "T_BEFORE_S":"13", "SENT_DIST":"14", "SAME_SENT":"15"  #Structural Features
                                 #Lexical features
                   }                                      #Indicator features

structFeat = StructuralFeatures()
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

    #Structural Features
    features["TOKENS_S"] = structFeat.get_tokens_count(source)
    features["TOKENS_T"] = structFeat.get_tokens_count(target)
    features["TOKEN_DIFFERENCE"] = abs(features["TOKENS_S"] - features["TOKENS_T"])

    features["PUNC_S"] = structFeat.get_punctuation_count(source)
    features["PUNC_T"] = structFeat.get_punctuation_count(target)
    features["PUNC_DIFFERENCE"] = abs(features["PUNC_S"] - features["PUNC_T"])

    features["POSITION_S"] = sents[i][6]
    features["POSITION_T"] = sents[i][7]

    if features["POSITION_T"] < features["POSITION_S"]:
        features["T_BEFORE_S"] = 1.0
    else:
        if features["POSITION_T"] == features["POSITION_S"]:
            features["SAME_SENT"] = 1.0
        else:
            features["SAME_SENT"] = 0.0
        features["T_BEFORE_S"] = 0.0

    features["SENT_DIST"] = abs(int(features["POSITION_S"]) - int(features["POSITION_T"]))


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