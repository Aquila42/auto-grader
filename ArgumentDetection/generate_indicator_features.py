
class IndicatorFeatures:
    def __init__(self):
        f = open("discourse_markers","r")
        self.discourse_markers = []
        for line in f:
            self.discourse_markers.append(line.strip())
        f.close()
        self.first_person = ["i","me","mine","myself"]

    def get_discourse_marker(self,sent):
        discourse = 0
        for word in sent:
            if word in self.discourse_markers:
                discourse += 1
        return discourse

    def get_first_person(self,sent):
        count = 0
        for word in sent:
            if word.strip().lower() in self.first_person:
                count += 1
        return count
