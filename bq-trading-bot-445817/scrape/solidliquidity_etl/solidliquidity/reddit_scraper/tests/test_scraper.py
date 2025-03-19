import pytest
from reddit_scraper.scraper import RedditScraper
import pandas as pd


@pytest.fixture
def scraper():
    return RedditScraper(client_id="test_id", client_secret="test_secret",
                         user_agent="test_agent", subreddit_name="test_subreddit")


def test_fetch_posts(scraper):
    posts = scraper.fetch_posts(limit=1)
    assert isinstance(posts, pd.DataFrame)


def test_fetch_comments(scraper):
    comments = scraper.fetch_comments("/r/test_subreddit/test_permalink")
    assert isinstance(comments, pd.DataFrame)
