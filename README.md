# Final Year Project
<img src="logo.png" alt="LexiGrow logo" width="200"/>  

Author James Byrne    
Supervisor: Julie Berndsen    
[LexiGrow Web App](http://csi6220-3-vm3.ucd.ie)

## Folders
* data - contains data used and created at various steps
* data_collection - contains python scripts related to collecting the data
* data_preparation - contains various python scripts for data preparation
* models - contain any models used
* word_difficulty_classifier - contains jupyter notebooks and python scripts that evaluate a range of different classifiers on different data sets, creates the best classifier and evaluates that classifier on the Twinword Data set
* Context2Vec - containes altered [scripts from the original author](https://github.com/orenmel/context2vec)
* website contains the django and react web app

---

## Requirements
* Python 3.7.3
* Ensure to have the google news word2vec model with 300 hidden units - for further information https://code.google.com/archive/p/word2vec/
* Ensure to have the UkWac pre-trained model - [download](http://u.cs.biu.ac.il/~nlp/resources/downloads/context2vec/)
* Install all requirements in requirements.txt file
```
pip install -r requirements.txt
```
* For the LexiGrow Web App, an additional requirements.txt file is in the website directiory and must be installed
* To run data collection script a Reddit API access is required and further information can be found on https://www.reddit.com/wiki/api#wiki_reddit_api_access
* To obtain collect twinword data, a Twinword API key is necessary and can be obtained from https://www.twinword.com/api/language-scoring.php
* Ensure that yarn is installed for the website
* Install all packages in yarn in the website/frontend section

---

## LexiGrow Web App
This contains the LexiGrow web app made using django and react. To run locally follow the Run steps below.

#### Requirements
* Install additional requirements.txt file found in website directory.
* Ensure that the word2vec path on line 5 in [website/lexigrow/components/word2vec.py](website/lexigrow/components/word2vec.py) points to the Google News Word2Vec Model.
* Ensure that the context2vec path on line 13 in [website/lexigrow/components/context2vec/context2vec.py](website/lexigrow/components/context2vec/context2vec.py) points to the UkWac Context2Vec pre-trained model mentioned above.
* Ensure that the word difficulty classifier path on line 30 in [website/lexigrow/components/word_dfficulty_classifier_wrapper.py](website/lexigrow/components/word_dfficulty_classifier_wrapper.py) points to the word difficulty classifier
* Ensure that yarn is installed for the website
* Install all packages in yarn in the website/frontend section

#### Run 
Steps to run LexiGrow locally

From within the website folder execute the following command
```
python3 manage.py runserver
```

#### Add Similar Words based on meaning by Word2Vec
1. In the [website/lexigrow/components/word2vec.py](website/lexigrow/components/word2vec.py) uncomment the 5th line
2. In the [website/frontend/src/components/TabsMain.js](website/frontend/src/components/TabsMain.js) uncomment the 143rd to the 145th line

#### Additional Notes
Postgresql was used in the production version of LexiGrow, for ease of portability, sqlite is used in this repository.

---

## Data Collection and Preparation
This section involves all of the steps to prepare the data. However, this is not required since the data has already been processed and is included in the repository.

### [Data Collection](data_collection/reddit_data.py)
This script collects data from the reddit for specified subreddits. Any optional arguments have default parameters. The data for each subreddit is stored in a json file in the output_foler_path.

#### Requirements:
* Reddit API access
* A text file with each subreddit that you want to collect data from on a new line (default file in data/subreddit_list.txt)

#### Run
From the project root directiory run the following command from terminal. Replace reddit_client_secret, reddit_client_id and reddit_user_agent with their corresponding values
```
python3 data_collection/reddit_data.py reddit_client_secret reddit_client_id reddit_user_agent 
```

#### Argument Information
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

### [Reddit Main Data Preprocessing](data_preparation/data_preprocessing.py)
This processing steps achieve the common steps for the Word Difficuly Classifier and the Context2Vec Model. It also performs the additional steps for the Word Difficuly Classifier. It outputs the sentences at each preprocessing stage to a json file for each subreddit.

#### Requirements:
* Collected Reddit Data
* google news word2vec model with 300 hidden units - for further information https://code.google.com/archive/p/word2vec/

#### Run
From the project root directiory run the following command from terminal
```
python3 data_preparation/data_preprocessing.py
```

#### Argument Information
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
                        
### [CEFR](data_preparation/cefr.py)
This file converts the cefr levels to CEFR minimum levels for each word outlined in the report, it outputs the results in a new file.

#### Requirements
* [cefr.json](data/word_difficulty_classifier/cefr.json)

#### Run
From the project root directiory run the following command from terminal
```
python3 data_preparation/cefr.py
```
#### Argument Information
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

### [Twinword Data](data_preparation/twinword.py)
This script collects data from twinword API to evaluate the performance of the word difficulty model. It creates two files, one with the twinword scores for the words in the Oxford 5000 data set and another with words not in that data set.

#### Requirements
* Twinword API access

#### Run
From the project root directiory run the following command from terminal. Replace twinword_api_key with the key.
```
python3 data_preparation/twinword.py twinword_api_key
```

#### Argument Information
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

### [Context2Vec Preprocessing File](data_preparation/context2vec_data_cleaning.py)
This script takes as input the output from the word difficulty preprocessing and creates a text file consisting of the reddit sentences and wordnet defintions and example phrases with a sentence per line.

#### Requirements
* output from [preprocessed file](data_preparation/data_preprocessing.py)

#### Run
From the project root directiory run the following command from terminal. Replace twinword_api_key with the key.
```
python3 data_preparation/context2vec_data_cleaning.py
```

#### Argument Information
```
usage: context2vec_data_cleaning.py [-h]
                                    [--reddit_preprocessed_path REDDIT_PREPROCESSED_PATH]
                                    [--save_path SAVE_PATH]

optional arguments:
  -h, --help            show this help message and exit
  --reddit_preprocessed_path REDDIT_PREPROCESSED_PATH
                        Path to folder containing preprocessed files (the
                        output from data_preparation/data_preprocessing.py)
  --save_path SAVE_PATH
                        Path to text file to output processed sentences
```

---

## Create Word Difficulty Classifier Data Sets (WDDs)
This is a python script that creates all of the different data sets. Note that these files are in the repository.

#### Requirements
* processed data from [Reddit Word Difficulty Data Preprocessing](data_preparation/data_preprocessing.py)

#### Run
```
python3 data_preparation/word_difficulty_dataset_generator.py
```

#### Argument Information
```
usage: word_difficulty_dataset_generator.py [-h]
                                            dataset_path processed_data_path

positional arguments:
  dataset_path         output path for all data sets
  processed_data_path  path to folder with subreddit processed data

optional arguments:
  -h, --help           show this help message and exit
```

---

## Evaluate Word Difficulty Models
This section evaluates various classifiers to select the best classifier

### [Linear Regression](word_difficulty_classifier/linear_regression_evaluation.py)
This is a python file that evaluates a linear regression model and polynomial features of degree 2 and 3 on all data sets using the BAR and R^2 metrics on 5-fold Stratified Cross Validation.

#### Requirements
* Data sets from [WDDManager](common/wdd_manager.py)

#### Run
From the project root directiory run the following command from terminal. Replace twinword_api_key with the key.
```
python3 word_difficulty_classifier/linear_regression_evaluation.py
```

#### Argument Information
```
usage: linear_regression_review.py [-h] datasets_path

positional arguments:
  datasets_path  path to folder containing data sets

optional arguments:
  -h, --help     show this help message and exit
```

### [Ensembles](word_difficulty_classifier/ensembles.py)
This is a python file that evaluates multiple ensemble models on all data sets using the BAR metrics on 5-fold Stratified Cross Validation.

#### Requirements
* Data sets from [WDDManager](common/wdd_manager.py)

#### Run
From the project root directiory run the following command from terminal. Replace twinword_api_key with the key.
```
python3 word_difficulty_classifier/ensembles.py
```

#### Argument Information
```
usage: ensembles.py [-h] [--datasets_path DATASETS_PATH]

optional arguments:
  -h, --help            show this help message and exit
  --datasets_path DATASETS_PATH
                        path to folder containing data sets
```

### [Logisitic Regression](word_difficulty_classifier/logistic_regression_evaluation.ipynb)
This is a python file that evaluates logistic regression models using L1 and L2 regularization on all data sets using the BAR metrics on 5-fold Stratified Cross Validation. The Paths should be changed in the notebook to refer to the appropriate locations

#### Requirements
* Data sets from [WDDManager](common/wdd_manager.py)

### [kNN](word_difficulty_classifier/knn_evaluation.ipynb)
This is a python file that evaluates the kNN classifier using different number of neighbours [1, 10] on all data sets using the BAR metrics on 5-fold Stratified Cross Validation. The Paths should be changed in the notebook to refer to the appropriate locations

#### Requirements
* Data sets from [WDDManager](common/wdd_manager.py)

### [kNN](word_difficulty_classifier/knn_evaluation.ipynb)
This is a python file that evaluates the kNN classifier using different number of neighbours [1, 10] on all data sets using the BAR metrics on 5-fold Stratified Cross Validation. The Paths should be changed in the notebook to refer to the appropriate locations

#### Requirements
* Data sets from [WDDManager](common/wdd_manager.py)

### [Model Creation](word_difficulty_classifier/create_selected_model.ipynb)
This is where the best performing model is created and the enitre data set is prepared for model predictions.

#### Requirements
* Data sets from [WDDManager](common/wdd_manager.py)

### [Data Analysis](word_difficulty_classifier/data_analysis.ipynb)
Data analysis was performed to view the distribution and number of Oxford 5000 words in the subreddits.

#### Requirements
* Data sets from [WDDManager](common/wdd_manager.py)

---

## Context2Vec

### Training the Context2Vec Model
There are multiple steps involved in training the Context2Vec model. Code was used from the original author and more information about training the model can be found on the papers [GitHub page](https://github.com/orenmel/context2vec)

#### Requirements
* output from [preprocessed file](data_preparation/context2vec_data_cleaning.py)

#### Run
First of all, the data needs to be split into training and test sets respectively [File](context2vec/train_test_split.py). Where INPUT is the path to the preprocessed data in this sections requirements. The OUTPUT is the folder to store the training and test data.
```
python3 context2vec/train_test_split.py INPUT OUTPUT
```

further preprocessing breaks the sentences into groups. The file was adjusted to take in the input text file and and the output folder location for the groups. The input text file is the training data from the previous step.
```
python3 context2vec/context2vec/train/corpus_by_sent_length.py CORPUS_FILE OUTPUT_DIR
```
After this, the model can begin to be trained, for further information about the different hyperparameters please go to the original authors page mentioned above.
```
python3 context2vec/context2vec/train/train_context2vec.py -i CORPUS_DIR  -w  WORD_EMBEDDINGS -m MODEL  -c lstm --deep yes -t 3 --dropout 0.0 -u 300 -e 10 -p 0.75 -b 100 -g 0
```

#### Arguments Info
The arguments that need to be changed are as follows.
* CORPUS_DIR - the folder that contains the output from the previous step
* WORD_EMBEDDINGS - path for the word embeddings
* MODEL - path for the model

### Context2Vec Evaluation
This can be performed with either the MSCC data set (skip to RUN MSCC step) or the data set created from the test set (Both RUN Test Set and Run MSCC steps).

#### Run Test Set
The INPUT is the path to the test file from the train test split when the model was being trained. The output is the folder that contains the question and answer files. 
```
python3 context2vec/scc_generator.py INPUT OUTPUT_DIR
```

#### Run MSCC
Questions refer to the questions file from the previous step or the questions file of the MSCC test data. Similarly, the ANSWERS refer to the answers file from the previous step or the answers file of the MSCC test data.
Note: the MSCC test set is [here](data/context2vec/holmes).
RESULTS refer to the path to the output file
MODEL refers to the model parameters file
For further information please visit the original papers [GitHub page](https://github.com/orenmel/context2vec).
```
python3 context2vec/context2vec/eval/sentence_completion.py QUESTIONS ANSWERS RESULTS MODEL
```

#### Requirements
* Trained Context2Vec Model
* Data set to evaluate on

---

## Word Difficulty Model Evaluation
This is where the trianed model is evaluated and compared against a different data set. This is a jupyter notebook. Change directories as necessary.

#### Requirements
* Trained Word Difficulty Model
* Twinword Data sets
* cefr data sets 
