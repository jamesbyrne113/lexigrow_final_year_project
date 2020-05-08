import sys
import os
sys.path.append(os.getcwd())
from data_preparation.word_difficulty_dataset_generator import WordDifficultyData

import pickle


class WDDManager:
    wdds_info = [
        "tf_idf, no change",
        "tf_idf, min max scaled", 
        "tf_idf, normalized", 
        "tf, no change",
        "tf, min max scaled",
        "tf, normalized", 
        "word_count, no change",
        "word_count, min max scaled",
        "word_count, normalized",
    ]
    
    def __init__(self, wdd_path=None):
        if wdd_path is None:
            self.wdd_path = "data/wdds/"
        elif not wdd_path.endswith("/"):
            self.wdd_path = wdd_path + "/"
        
        self.wdds = {}
        
    def get_wdd(self, scale_type="no_change", data_type="tf_idf"):
        """scale_type = {no_change, scaled, normalized}, data_type={tf, tf_idf, word_count}"""
        
        filtered_infos = self._get_wdds_info(scale_type, data_type)
        if len(filtered_infos) > 1:
            raise Exception("More than one WDD with that criteria")
        elif len(filtered_infos) == 0:
            raise Exception("No WDD with that criteria")
        
        return self._load_wdds(filtered_infos)[0]
    
    # scale_type = {no_change, scaled, normalized}, data_type={tf, tf_idf, word_count}
    def get_wdds(self, scale_type="", data_type=""):
        
        filtered_infos = self._get_wdds_info(scale_type, data_type)
        if len(filtered_infos) == 0:
            raise Exception("No WDD with that criteria")
        
        return self._load_wdds(filtered_infos)

    def _get_wdds_info(self, scale_type="", data_type=""):
        scale_type = scale_type.replace("_", " ")
        data_type += ","

        return [info for info in self.wdds_info if scale_type in info and data_type in info]

        
    
    def _load_wdds(self, infos):
        current_wdds = []
        for info in infos:
            if info in self.wdds:
                current_wdds.append(self.wdds[info])
            else:
                print("loading {}...".format(info))
                with open(self.wdd_path + self._get_filename(info), "rb") as f:
                    current_wdd = pickle.load(f)
                current_wdds.append(current_wdd)
                self.wdds[info] = current_wdd
        print("Done!")
        return current_wdds
                
    def _get_filename(self, info):
        return info.replace(", ", "_").replace(" ", "_") + ".pickle"
            
if __name__ == "__main__":
    def test():
        wdd_manager = WDDManager()
        tf_scaled = wdd_manager.get_wdd(scale_type="scaled", data_type="tf")
        assert tf_scaled.info == "tf, min max scaled"
        tf_idf_normalized = wdd_manager.get_wdds(scale_type="normalized", data_type="tf_idf")
        assert tf_idf_normalized[0].info == "tf_idf, normalized"
        word_count_no_change = wdd_manager.get_wdd(scale_type="no_change", data_type="word_count")
        assert word_count_no_change.info == "word_count, no change"
        print("Passed All")
        
    test()    