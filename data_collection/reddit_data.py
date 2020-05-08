# %%

import sys
import os
ROOT_PATH = os.getcwd()
sys.path.append(ROOT_PATH)

import json
from datetime import datetime
import argparse

import pathlib
from praw.models import MoreComments

print(ROOT_PATH)
from data_collection.reddit import praw_reddit


class reddit_data:
    def __init__(self, data_path):
        # append "/" at end of path if not already there
        if data_path[-1] != "/":
            data_path += "/"
        pathlib.Path(data_path).mkdir(exist_ok=True)
        self.data_path = data_path

    def get_subreddit(self, subreddit, max_comment_count=20, max_words=10000):
        subreddit_path = self.data_path + subreddit.display_name
        pathlib.Path(subreddit_path).mkdir(exist_ok=True)

        submissions = []
        word_count = 0

        if pathlib.Path(subreddit_path + ".json").exists():
            with open(subreddit_path + ".json", "r") as f:
                subreddit_data = json.load(f)

            submissions = subreddit_data["submissions"]
            word_count = subreddit_data["word_count"]

            print("")
            print("Already have:", subreddit_path)
            print("word count:", word_count)
            print("")

            if word_count >= max_words:
                return subreddit_data

        for submission in subreddit.top(limit=10000):
            print("\t", subreddit.display_name + ":", submission.title)
            current_submission = self.get_submission_data(submission, max_words - word_count, max_comment_count)
            submissions.append(current_submission)

            try:
                word_count += current_submission.get("word_count")
            except Exception as ex:
                word_count = 0
                print("word count:", ex)

            # with open(submission_path, "w") as fp:
            #     json.dump(current_submission, fp)

            print("word count:", word_count)

            if word_count >= max_words:
                break

        subreddit_data = {
            "display_name": subreddit.display_name,
            "fullname": subreddit.fullname,
            "submissions": submissions,
            "word_count": word_count,
        }

        try:
            with open(subreddit_path + ".json", "w") as fp:
                json.dump(subreddit_data, fp)
        except Exception as ex:
            print("store subreddit", ex)

        return subreddit_data

    def get_submission_data(self, submission, max_words, max_comment_count, getComments=True):
        try:
            author = submission.author.name
        except:
            author = None
        try:
            author_fullname = submission.author.fullname
        except:
            author_fullname = None

        try:
            submission_data = {
                "author": author,
                "author_fullname": author_fullname,
                "category": submission.category,
                "created_utc": submission.created_utc,
                "fullname": None if submission.fullname is None else submission.fullname,
                "id": submission.id,
                "name": submission.name,
                "title": submission.title,
                "word_count": 0
            }
        except Exception as ex:
            print("get submission", ex)
            submission_data = submission
            submission_data["exception"] = str(ex)

        if getComments:
            try:
                comments_data = self.get_submission_comments(submission, max_words, max_comment_count)
                submission_data["comments"] = comments_data["comments"]
                submission_data["word_count"] = comments_data["total_word_count"]
            except Exception as ex:
                print("get comments:", ex)

            if "comments" not in submission_data or submission_data["comments"] is None:
                submission_data["comments"] = []

            if "word_count" not in submission_data or submission_data["word_count"] is None:
                submission_data["word_count"] = 0

        return submission_data

    def get_submission_comments(self, submission, max_words, max_count):
        comments = []
        # submission.comments.replace_more(limit=None)
        word_count = 0
        count = 0
        # for comment in submission.comments.list():
        for comment in submission.comments:
            if word_count > max_words or count > max_count:
                break
            count += 1

            if isinstance(comment, MoreComments):
                continue

            try:
                author = comment.author.name
            except:
                author = None
            try:
                author_fullname = comment.author.fullname
            except:
                author_fullname = None

            try:
                word_count += len(comment.body.split())

                comment_data = {
                    "author": author,
                    "body": comment.body,
                    "author_fullname": author_fullname,
                    "created_utc": comment.created_utc,
                    "depth": comment.depth,
                    "fullname": None if comment.fullname is None else comment.fullname,
                    "id": comment.id,
                    "parent_id": None if comment.parent_id == submission.fullname else comment.parent_id,
                    "word_count": word_count,
                    "max_words": max_words,
                }

                comments.append(comment_data)
            except Exception as ex:
                print(ex)

        return {
            "comments": comments,
            "total_word_count": word_count
        }


def get_subreddit_names(subreddit_names_path):
    with open(subreddit_names_path, "r") as f:
        return f.read().split("\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "reddit_client_secret", 
        type=str, 
        help="Reddit API client secret"
        )
    
    parser.add_argument(
        "reddit_client_id", 
        type=str, 
        help="User Agent for reddit API"
        )
    
    parser.add_argument(
        "reddit_user_agent", 
        type=str, 
        help="reddit user agent for reddit API"
        )
    
    parser.add_argument(
        "--subreddit_names_file",
        type=str,
        default="data/subreddit_list.txt",
        help="path to text file containing the subreddits to collect data from. Each subreddit on a new line"
    )
    
    parser.add_argument(
        "--output_foler_path",
        type=str,
        default="data/reddit_data",
        help="path of folder to save output files"
    )
    
    parser.add_argument(
        "--word_num",
        type=int,
        default=60000,
        help="minimum number of words per subreddit"
    )
    
    parser.add_argument(
        "--max_comments",
        type=int,
        default=20,
        help="maximum number of comments per subreddit post"
    )
    
    args = parser.parse_args()

    reddit = praw_reddit(args.reddit_client_secret, args.reddit_client_id, args.reddit_user_agent)

    subreddit_names = get_subreddit_names(args.subreddit_names_file)

    print("Min words:", args.word_num, "; Number of Subreddits:", len(subreddit_names), "; Time:", datetime.now())

    for subreddit_name in subreddit_names:
        print("Subreddit:", subreddit_name, "; Time:", datetime.now())
        subreddit = reddit.subreddit(subreddit_name)
        reddit_data(args.output_foler_path).get_subreddit(subreddit, max_words=args.word_num, max_comment_count=args.max_comments)
