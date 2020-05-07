# LexiGrow - Final Year Project
James byrne
Supervisor: Julie Berndsen

## Requirements
* Python 3.7.3
* Install all requirements in requirements.txt file
```
pip install -r requirements.txt
```
* To run data collection script a Reddit API access is required and further information can be found on https://www.reddit.com/wiki/api#wiki_reddit_api_access
* To obtain collect twinword data, a Twinword API key is necessary and can be obtained from https://www.twinword.com/api/language-scoring.php

## Data Collection

This script collects data from the reddit for specified subreddits.
### Requirements:
* Reddit API access
* A text file with each subreddit that you want to collect data from on a new line

from the project root directiory run the following command from terminal
```
python3 data_preparation/reddit_data.py reddit_client_secret reddit_client_id reddit_user_agent 
```

### Argument Information
```
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

