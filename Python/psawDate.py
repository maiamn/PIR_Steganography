import praw
from psaw import PushshiftAPI
import datetime as dt

reddit = praw.Reddit(
    user_agent="Subreddit statistics (by u/pir2022_)",
    client_id="L93ownPP-FtArtwOpikpEQ",
    client_secret="HKCzRao9EAVlKDYbHx_Sal27eqZclQ",
    username="pir2022_",
    password="steganographie",
)
api = PushshiftAPI(reddit)
import warnings

warnings.filterwarnings("ignore")

# Retrieve posts after a certain date
start_epoch = int(dt.datetime(2017, 1, 1).timestamp())
end_epoch = int(dt.datetime(2018, 1, 1).timestamp())

listID = list(api.search_submissions(after=start_epoch,
                                     subreddit='politics',
                                     filter=['url', 'author', 'title', 'subreddit'],
                                     limit=10,
                                     before=end_epoch))

for ID in listID:
    submission = reddit.submission(ID)
    print(submission.title)


def get_posts_within_range(api, subreddit, startYear, endYear, startMonth=1, endMonth=1, max_posts=100):
    ## gets up to max_posts within the specified range, using the PushShift api.
    ## month and year are integers, subreddit is an instance of Subreddit
    ## api = PushshiftAPI(reddit)
    start_epoch = int(dt.datetime(startYear, startMonth, 1).timestamp())
    end_epoch = int(dt.datetime(endYear, endMonth, 1).timestamp())
    listID = list(api.search_submissions(after=start_epoch,
                                         subreddit=subreddit.name,
                                         filter=['url', 'author', 'title', 'subreddit'],
                                         limit=max_posts,
                                         before=end_epoch))
    listSubmission = []
    for ID in listID:
        listSubmission.append(reddit.submission(ID))
    return listSubmission


# Call this function if the other returns less than 100 posts
def get_posts_after_date(api, subreddit, startYear, endYear, startMonth=1, endMonth=1, max_posts=100):
    ## gets up to max_posts after the specified date, using the PushShift api.
    ## month and year are integers, subreddit is an instance of Subreddit
    ## api = PushshiftAPI(reddit)
    start_epoch = int(dt.datetime(startYear, startMonth, 1).timestamp())
    listID = []
    listID = list(api.search_submissions(after=start_epoch,
                                         subreddit=subreddit.name,
                                         filter=['url', 'author', 'title', 'subreddit'],
                                         limit=max_posts))
    listSubmission = []
    print(listID)
    for ID in listID:
        listSubmission.append(reddit.submission(ID))
    return listSubmission


# test
sub = reddit.subreddit("MartialMemes")
# liste = get_posts_after_date(api, sub, 2020, 2021)
# liste2 = get_posts_after_date(api, sub, 2020, 2021)
liste3 = get_posts_within_range(api, sub, 2020, 2021)
