import praw
from prawcore.exceptions import TooManyRequests, RequestException, ServerError
from requests.exceptions import ReadTimeout
import time
import pandas as pd


class RedditScraper:
    def __init__(self, client_id, client_secret, user_agent, subreddit_name):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        self.subreddit_name = subreddit_name

    def fetch_posts(self, limit=10):
        subreddit = self.reddit.subreddit(self.subreddit_name)
        posts_data = []

        for post in subreddit.hot(limit=limit):
            while True:  # Retry loop for rate limits
                try:
                    posts_data.append({
                        "Title": post.title,
                        "Score": post.score,
                        "Upvote Ratio": post.upvote_ratio,
                        "Number of Comments": post.num_comments,
                        "Author": post.author.name if post.author else None,
                        "Created (UTC)": post.created_utc,
                        "URL": post.url,
                        "Selftext": post.selftext,
                        "Permalink": post.permalink,
                        "Flair": post.link_flair_text,
                        "Over 18": post.over_18,
                        "Spoiler": post.spoiler,
                        "Stickied": post.stickied,
                        "Total Awards": post.total_awards_received,
                    })
                    break  # Exit the retry loop if successful
                except TooManyRequests:
                    print("Rate limit exceeded. Sleeping for 60 seconds...")
                    time.sleep(60)  # Wait for 60 seconds before retrying

        return pd.DataFrame(posts_data)  # Return the DataFrame after processing all posts

    def fetch_detailed_post(self, permalink):
        submission = self.reddit.submission(
            url=f"https://www.reddit.com{permalink}")
        detailed_data = {
            "Title": submission.title,
            "Score": submission.score,
            "Upvote Ratio": submission.upvote_ratio,
            "Number of Comments": submission.num_comments,
            "Author": submission.author.name if submission.author else None,
            "Created (UTC)": submission.created_utc,
            "URL": submission.url,
            "Selftext": submission.selftext,
            "Permalink": submission.permalink,
            "Flair": submission.link_flair_text,
            "Over 18": submission.over_18,
            "Spoiler": submission.spoiler,
            "Stickied": submission.stickied,
            "Total Awards": submission.total_awards_received,
            "Edited": submission.edited,
            "Gilded": submission.gilded,
            "Distinguished": submission.distinguished,
            "View Count": submission.view_count,  # May return None
            "Subreddit": submission.subreddit.display_name,
        }

        return pd.DataFrame([detailed_data])
    
    def fetch_comments(self, permalink, max_retries=5, initial_delay=2):
        """
        Fetch comments from a Reddit submission with retry logic for timeouts and rate limits.
        
        Args:
            permalink (str): The permalink of the Reddit submission.
            max_retries (int): Maximum number of retries for failed requests.
            initial_delay (int): Initial delay (in seconds) before retrying.
        
        Returns:
            pd.DataFrame: A DataFrame containing the comments data.
        """
        submission = self.reddit.submission(url=f"https://www.reddit.com{permalink}")
        comments_data = []

        # Replace "MoreComments" objects with actual comments
        retries = 0
        while retries < max_retries:
            try:
                submission.comments.replace_more(limit=None)
                break  # Exit the loop if successful
            except (TooManyRequests, RequestException, ServerError, ReadTimeout) as e:
                retries += 1
                if retries >= max_retries:
                    print(f"Max retries reached for 'replace_more'. Error: {e}")
                    return pd.DataFrame()  # Return an empty DataFrame if max retries are reached
                delay = initial_delay * (2 ** (retries - 1))  # Exponential backoff
                print(f"Error: {e}. Retrying in {delay} seconds...")
                time.sleep(delay)

        # Fetch comments with retry logic for rate limits and timeouts
        for comment in submission.comments.list():
            retries = 0
            while retries < max_retries:
                try:
                    comments_data.append({
                        "Post Title": submission.title,
                        "Post ID": submission.id,
                        "Comment ID": comment.id,
                        "Comment Body": comment.body,
                        "Author": comment.author.name if comment.author else None,
                        "Score": comment.score,
                        "Created (UTC)": comment.created_utc,
                        "Is Submitter": comment.is_submitter,
                        "Parent ID": comment.parent_id,
                        "Permalink": comment.permalink,
                    })
                    break  # Exit the retry loop if successful
                except (TooManyRequests, RequestException, ServerError, ReadTimeout) as e:
                    retries += 1
                    if retries >= max_retries:
                        print(f"Max retries reached for comment {comment.id}. Error: {e}")
                        break  # Skip this comment if max retries are reached
                    delay = initial_delay * (2 ** (retries - 1))  # Exponential backoff
                    print(f"Error: {e}. Retrying in {delay} seconds...")
                    time.sleep(delay)

        return pd.DataFrame(comments_data)  # Return the DataFrame after processing all comments

'''
    def fetch_comments(self, permalink):
        #submission = self.reddit.submission(
        #    url=f"https://www.reddit.com{permalink}")
        #submission.comments.replace_more(limit=None)

        submission = self.reddit.submission(url=f"https://www.reddit.com{permalink}")
        
        # Replace "MoreComments" objects with actual comments
        while True:
            try:
                submission.comments.replace_more(limit=None)
                break  # Exit the loop if successful
            except TooManyRequests:
                print("Rate limit exceeded while replacing 'MoreComments'. Sleeping for 60 seconds...")
                time.sleep(60)  # Wait for 60 seconds before retrying


        comments_data = []

        # Fetch comments with retry logic for rate limits
        for comment in submission.comments.list():
            while True:  # Retry loop for rate limits
                try:
                    comments_data.append({
                        "Post Title": submission.title,
                        "Post ID": submission.id,
                        "Comment ID": comment.id,
                        "Comment Body": comment.body,
                        "Author": comment.author.name if comment.author else None,
                        "Score": comment.score,
                        "Created (UTC)": comment.created_utc,
                        "Is Submitter": comment.is_submitter,
                        "Parent ID": comment.parent_id,
                        "Permalink": comment.permalink,
                    })
                    break  # Exit the retry loop if successful
                except TooManyRequests:
                    print("Rate limit exceeded. Sleeping for 60 seconds...")
                    time.sleep(60)  # Wait for 60 seconds before retrying

        return pd.DataFrame(comments_data)  # Return the DataFrame after processing all comments
'''
