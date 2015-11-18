from nltk import bigrams,trigrams
import string

def counts(list_x,dict_x):
    for word in list_x:
        if word not in dict_x:
            dict_x[word] = 1
        else:
            dict_x[word] = +1
    return dict_x

def write_to_file(file_name,dict_x):
    for word in dict_x:
        file_name.write(str(word)+"\t"+str(dict_x[word])+"\n")



unigram = open("data/unigrams","w")
bigram = open("data/bigrams","w")
trigram = open("data/trigrams","w")

file_type = "train"

input_tree = open("data/essay.all.arguments.0617.txt."+file_type,"r")

input_tree.readline()
clauses = []
for line in input_tree:
    temp = line.split("\t")
    clauses.append(temp[3])

uni = {}
bi = {}
tri = {}

for clause in clauses:
    print clause
    clause = clause.translate(string.maketrans("",""), string.punctuation)
    temp = clause.lower().split()
    counts(temp,uni)
    counts(bigrams(temp),bi)
    counts(trigrams(temp),tri)

write_to_file(unigram,uni)
write_to_file(bigram,bi)
write_to_file(trigram,tri)
