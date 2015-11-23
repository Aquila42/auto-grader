import nltk
import string

class StructuralFeatures:
    def get_tokens_count(self, sent):
        #Returns float for division in structural features
        return float(len(nltk.word_tokenize(sent)))

    def get_punctuation_count(self,sent):
        count = 0
        for c in sent:
            if c in string.punctuation:
                count += 1
        return count
