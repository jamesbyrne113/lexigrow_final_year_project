# LexiGrow - Final Year Project
James byrne
Supervisor: Julie Berndsen

## Folders
* data - contains data used and created at various steps
* data_collection - contains python scripts related to collecting the data
* data_preparation - contains various python scripts for data preparation
* models - contain any models used

## Requirements
* Python 3.7.3
* Install all requirements in requirements.txt file
```
pip install -r requirements.txt
```
* To run data collection script a Reddit API access is required and further information can be found on https://www.reddit.com/wiki/api#wiki_reddit_api_access
* To obtain collect twinword data, a Twinword API key is necessary and can be obtained from https://www.twinword.com/api/language-scoring.php

## Data Collection
This script collects data from the reddit for specified subreddits. Any optional arguments have default parameters. The data for each subreddit is stored in a json file in the output_foler_path.

[data collection file](data_collection/reddit_data.py)

### Requirements:
* Reddit API access
* A text file with each subreddit that you want to collect data from on a new line (default file in data/subreddit_list.txt)

### Run
From the project root directiory run the following command from terminal. Replace reddit_client_secret, reddit_client_id and reddit_user_agent with their corresponding values
```
python3 data_collection/reddit_data.py reddit_client_secret reddit_client_id reddit_user_agent 
```

### Argument Information
```
usage: reddit_data.py [-h] [--subreddit_names_file SUBREDDIT_NAMES_FILE]
                      [--output_foler_path OUTPUT_FOLER_PATH]
                      [--word_num WORD_NUM] [--max_comments MAX_COMMENTS]
                      reddit_client_secret reddit_client_id reddit_user_agent
                      
positional arguments:
  reddit_client_secret  Reddit API client secret
  reddit_client_id      User Agent for reddit API
  reddit_user_agent     reddit user agent for reddit API

optional arguments:
  -h, --help            show this help message and exit
  --subreddit_names_file SUBREDDIT_NAMES_FILE
                        path to text file containing the subreddits to collect
                        data from. Each subreddit on a new line
  --output_foler_path OUTPUT_FOLER_PATH
                        path of folder to save output files
  --word_num WORD_NUM   minimum number of words per subreddit
  --max_comments MAX_COMMENTS
                        maximum number of comments per subreddit post
```

## Reddit Main Data Processing 
This processing steps achieve the common steps for the Word Difficuly Classifier and the Context2Vec Model. It also performs the additional steps for the Word Difficuly Classifier.

[data preprocessing file](data_preparation/data_preprocessing.py)

### Requirements:
* Collected Reddit Data
* google news word2vec model with 300 hidden units - for further information https://code.google.com/archive/p/word2vec/

### Run
From the project root directiory run the following command from terminal
```
python3 data_preparation/data_preprocessing.py
```

### Argument Information
```
usage: data_preprocessing.py [-h]
                             [--reddit_collected_path REDDIT_COLLECTED_PATH]
                             [--processed_reddit_path PROCESSED_REDDIT_PATH]
                             [--word2vec_model_path WORD2VEC_MODEL_PATH]

optional arguments:
  -h, --help            show this help message and exit
  --reddit_collected_path REDDIT_COLLECTED_PATH
                        path to folder with originally collected reddit data
  --processed_reddit_path PROCESSED_REDDIT_PATH
                        output path for processed reddit files
  --word2vec_model_path WORD2VEC_MODEL_PATH
                        Path to Word2Vec model used for
```
                        
## CEFR
This file converts the cefr levels to CEFR minimum levels for each word outlined in the report.

[cefr file](data_preparation/cefr.py)

### Requirements
* [cefr.json](data/word_difficulty_classifier/cefr.json)

### Run
From the project root directiory run the following command from terminal
```
python3 data_preparation/cefr.py
```
### Argument Information
```
usage: cefr.py [-h] [--cefr_path CEFR_PATH]
               [--cefr_output_path CEFR_OUTPUT_PATH]

optional arguments:
  -h, --help            show this help message and exit
  --cefr_path CEFR_PATH
                        path_to_cefr
  --cefr_output_path CEFR_OUTPUT_PATH
                        output path for cefr json file
```

## Twinword Data
This script collects data from twinword API to evaluate the performance of the word difficulty model.

[twinword file](data_preparation/twinword.py)

### Requirements
* Twinword API access

### Run
From the project root directiory run the following command from terminal. Replace twinword_api_key with the key.
```
python3 data_preparation/twinword.py twinword_api_key
```

### Argument Information
```
usage: twinword.py [-h] [--non_cefr_save_path NON_CEFR_SAVE_PATH]
                   [--cefr_save_path CEFR_SAVE_PATH] [--cefr_path CEFR_PATH]
                   twinword_api_key

positional arguments:
  twinword_api_key      API key from twinword must be provided, visit
                        https://www.twinword.com/api/language-scoring.php for
                        further details

optional arguments:
  -h, --help            show this help message and exit
  --non_cefr_save_path NON_CEFR_SAVE_PATH
                        Save path for json file consisting of twinword words
                        not in the Oxford 5000 data set
  --cefr_save_path CEFR_SAVE_PATH
                        Save path for json file consisting of twinword words
                        that are in the Oxford 5000 data set
  --cefr_path CEFR_PATH
                        path to cefr min file
```
