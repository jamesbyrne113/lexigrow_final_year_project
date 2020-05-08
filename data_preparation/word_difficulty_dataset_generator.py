import sys
sys.path.extend(["../", "./"]);

from data_preparation.tf_idf import TfIdfGenerator
from data_preparation.word_count import WordCounter
from data_preparation.cefr import cefr_to_num, num_to_cefr

import json
import pandas as pd
import numpy as np
import pathlib

from sklearn.impute import SimpleImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import Normalizer

class WordDifficultyData:
    def __init__(self, info, processed_data_path="data/reddit_data_processed", 
                 comments_key="comment_processed_no_spell_corrections", 
                 missing_value_method=None, 
                 value_type="tf_idf", 
                 cefr_path="data/cefr.json", 
                 numeric_cefr=True,
                 is_scaled=False,
                 is_normalized=False,
        ):
        self.missing_value_method = missing_value_method
        self.info = info
        self.value_type = value_type
        
        self.cefr_path = cefr_path
        
        if value_type.startswith("tf"):
            self.is_missing_value = np.isnan
            self.missing_value = np.nan
            
            self.tf_idf_generator = TfIdfGenerator(processed_data_path, comments_key)
            
            self.docs = self.tf_idf_generator.docs
            self.all_words_set = self.tf_idf_generator.all_words_set
            
            self.tf_idf_generator.compute_tf()
            
            if value_type == "tf_idf":
                self.tf_idf_generator.compute_tf_idf()
                self.values = self.tf_idf_generator.tf_idf
            elif value_type == "tf":
                self.values = self.tf_idf_generator.tf
        elif value_type == "word_count":
            self.is_missing_value = self._is_zero
            self.missing_value = 0
            
            self.word_counter = WordCounter(processed_data_path, comments_key)
            self.word_counter.compute_word_count()
            
            self.docs = self.word_counter.docs
            self.all_words_set = self.word_counter.all_words_set
            self.values = self.word_counter.word_count
        
        self.get_dataframe(numeric_cefr)
        
        if missing_value_method == "average_class":
            self._average_class_imputer()
        elif missing_value_method == "simple":
            self._simple_imputer()
        elif missing_value_method == "iterative":
            self._iterative_imputer()
        elif missing_value_method == None:
            self.dataframe.fillna(0, inplace=True)
            
        if is_scaled:
            self.min_max_scaling()
            
        if is_normalized:
            self.normalizing()
            
            
    def _is_zero(self, x):
        return x == 0
            
            
    def _get_cefr_io(self, numeric_values=True):  
        with open(self.cefr_path, "r") as fp:
            cefr = json.load(fp)
            
        cefr_io = {}
        
        # use mean of different levels for different pos of the word
        def mean(k, v):
            values = [cefr_to_num[x] for x in v.values()]
            return sum(values)/len(values)
        
        # use minimum of all levels for different pos of the word
        def minimum(k, v):
            min_value = 6
            for value in v.values():
                if (cefr_to_num[value] < min_value):
                    min_value = cefr_to_num[value]
            return min_value if numeric_values else num_to_cefr[min_value]
        
        for k, v in cefr.items():
            cefr_io[k] = minimum(k, v)
        return cefr_io
    
    
    def get_dataframe(self, ignore_cache=False):
        if not ignore_cache and hasattr(self, 'dataframe'):
            return self.dataframe
            
        values = []
        
        cefr_io = self._get_cefr_io()

        for word in self.all_words_set:
            if word in cefr_io.keys():
                word_values = [word]
                for doc in self.values:
                    word_values.append(self.values[doc][word])
                word_values.append(cefr_io[word])
                values.append(word_values)

        self.columns = ["word"]
        self.columns.extend(self.docs)
        self.columns.append("cefr")
        
        self.dataframe = pd.DataFrame.from_records(values, columns=self.columns)
        return self.dataframe
    
    def _average_class_imputer(self, df=None, features=None):
        if df is None:
            df = self.dataframe
        
        if features == None:
            features = self.features()
           
        for col in features:
            for level in range(5):
                rows = [x for x, y in zip(df[col].to_numpy(), df["cefr"]) if y == level and not self.is_missing_value(x)]
                avg_val = sum(rows)/len(rows)
                df.loc[(self.is_missing_value(df[col])) & (df["cefr"] == level), col] = avg_val
        self.dataframe = df

    def _simple_imputer(self, df=None, features=None):
        if df is None:
            df = self.dataframe
        
        if features == None:
            features = self.features()
        
        imp = SimpleImputer(missing_values=self.missing_value, strategy='mean')
        new_df = pd.DataFrame(data=imp.fit_transform(features.to_numpy()), columns=features.columns)
        
        for col in new_df:
            df[col] = new_df[col]
            
        self.dataframe = df
        
    
    def _iterative_imputer(self, df=None, features=None):
        if df is None:
            df = self.dataframe
        
        if features == None:
            features = self.features()
            
        imp = IterativeImputer(missing_values=self.missing_value, max_iter=200)
        new_df = pd.DataFrame(data=imp.fit_transform(features), columns=features.columns)
        
        for col in new_df:
            df[col] = new_df[col]
            
        self.dataframe = df
        
    
    def _fill_nan(self, df=None, features=None):
        if df is None:
            df = self.dataframe
        
        for name, doc in df:
            for index, val in enumerate(doc):
                if val == np.nan:
                    doc[index] == 0
                    
    def min_max_scaling(self, low=0, high=1, df=None, features=None):
        if df is None:
            df = self.dataframe
        
        if features == None:
            features = self.features()
            
        scaler = MinMaxScaler() # default scale each feature between 0, 1
        scaled_data = scaler.fit_transform(features)
        new_df = pd.DataFrame(data=scaled_data, columns=features.columns)
        
        for col in new_df:
            df[col] = new_df[col]
            
        self.dataframe = df
        
    def normalizing(self, df=None, features=None):
        if df is None:
            df = self.dataframe
        
        if features == None:
            features = self.features()
            
        normalizer = Normalizer()
        normalized_data = normalizer.fit_transform(features)
        new_df = pd.DataFrame(data=normalized_data, columns=features.columns)
        
        for col in new_df:
            df[col] = new_df[col]
            
        self.dataframe = df
    
    def features(self):
        if not hasattr(self, 'dataframe'):
            self.get_dataframe()
            
        return self.dataframe[self.values]
    
    def output(self):
        if not hasattr(self, 'dataframe'):
            self.get_dataframe()
            
        return self.dataframe["cefr"]

def load_wdds(verbose=False):
    wdds = {}
    for path in pathlib.Path("data/wdds/").iterdir():
        if path.stem.startswith("word_count") or path.stem.startswith("tf"):
            with open(path, "rb") as f:
                wdd = pickle.load(f)
                wdds[wdd.info] = wdd
            if verbose:
                print(wdd.info)

    return wdds


if __name__ == "__main__":
    import pickle
    import argparse
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "dataset_path", 
        type=str,
        default="data/wdds/",
        help="output path for all data sets",
    )
    parser.add_argument(
        "processed_data_path",
        type=str,
        default="data/reddit_data_processed",
        help="path to folder with subreddit processed data"
    )
    
    args = parser.parse_args()
    
    wdds = [
        WordDifficultyData(info="tf_idf, no change", value_type="tf_idf"),
        WordDifficultyData(info="tf_idf, min max scaled", value_type="tf_idf", is_scaled=True),
        WordDifficultyData(info="tf_idf, normalized", value_type="tf_idf", is_normalized=True),

        WordDifficultyData(info="tf, no change", value_type="tf"),
        WordDifficultyData(info="tf, min max scaled", value_type="tf", is_scaled=True),
        WordDifficultyData(info="tf, normalized", value_type="tf", is_normalized=True),

        WordDifficultyData(info="word_count, no change", value_type="word_count"),
        WordDifficultyData(info="word_count, min max scaled", value_type="word_count", is_scaled=True),
        WordDifficultyData(info="word_count, normalized", value_type="word_count", is_normalized=True),
    ]
    
    for wdd in wdds:
        name = wdd.info.replace(", ", "_").replace(" ", "_")
        print (name)
        with open(args.dataset_path + name, "wb") as f:
            pickle.dump(wdd, f)
