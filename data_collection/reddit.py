import praw

def praw_reddit(reddit_client_secret, reddit_client_id, user_agent):
    reddit = praw.Reddit(client_id=reddit_client_id,
                             client_secret=reddit_client_secret,
                             user_agent=user_agent,
                            )




