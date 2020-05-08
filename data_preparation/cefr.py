import json
import argparse

cefr_to_num = {
    "A1": 0,
    "A2": 1,
    "B1": 2,
    "B2": 3,
    "C": 4,
    "C1": 4,
    "C2": 5,
}

num_to_cefr = {
    0: "A1",
    1: "A2",
    2: "B1",
    3: "B2",
    4: "C",
    5: "C2",
}


def get_numerical_cefr(cefr):
    if type(cefr) == str:
        return cefr_to_num[cefr]
    return cefr

def get_char_cefr(cefr):
    if type(cefr) == int:
        return num_to_cefr[cefr]
    return cefr


class CEFR:
    def __init__(self, cefr_path, level_type="min"):
        self.level_type = level_type
        self.path = cefr_path
        
    # use mean of different levels for different pos of the word
    def _mean(self, k, v):
        values = [cefr_to_num[x.upper()] for x in v.values()]
        return sum(values)/len(values)

    # use minimum of all levels for different pos of the word
    def _minimum(self, k, v):
        min_value = 6
        for value in v.values():
            if (cefr_to_num[value.upper()] < min_value):
                min_value = cefr_to_num[value.upper()]
        return min_value

    def _get_dictionary(self):  
        with open(self.path, "r") as fp:
            all_cefr = json.load(fp)
        
        cefr = {}
        for k, v in all_cefr.items():
            if self.level_type == "min":
                cefr[k] = self._minimum(k, v)
            elif self.level_type == "avg":
                cefr[k] = self._mean(k, v)
                
        return cefr
        

    def _save(self, cefr, save_path):
        with open(save_path, "w") as f:
            print("saving to:", save_path)
            json.dump(cefr, f)
        
    def dictionary(self, save_path=None):
        cefr = self._get_dictionary()
        if save_path:
            self._save(cefr, save_path)
        else:
            return cefr

                       
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "--cefr_path", 
        type=str,
        default="data/word_difficulty_classifier/cefr.json",
        help="path_to_cefr",
    )
    
    parser.add_argument(
        "--cefr_output_path", 
        type=str,
        default="data/word_difficulty_classifier/cefr_min.json",
        help="output path for cefr json file",
    )
    
    args = parser.parse_args()
    
    cefr = CEFR(args.cefr_path)
    cefr.dictionary(save_path=args.cefr_output_path)
