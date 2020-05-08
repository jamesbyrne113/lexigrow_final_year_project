class WordDifficultyClassifier:
    num_to_cefr = {
        0: "A1",
        1: "A2",
        2: "B1",
        3: "B2",
        4: "C",
        5: "C2",
    }
    
    def __init__(self, model, all_word_values):
        self.model = model
        self.all_word_values = all_word_values
        
    def get_numeric_cefr_level(self, word):
        if word not in self.all_word_values:
            return None
        
        word_values = self.all_word_values[word]
        return int(self.model.predict([word_values])[0])
        
    def get_cefr_level(self, word):
        if word not in self.all_word_values:
            return None
        
        word_values = self.all_word_values[word]
        numeric_cefr = int(self.model.predict([word_values])[0])
        return self.num_to_cefr[numeric_cefr]