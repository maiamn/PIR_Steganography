import praw
from datetime import datetime



def get_post_from_year(subreddit, year, month):
    """
    Returns id of a post from the given year in the given sub
    subreddit object comes from reddit.subreddit("martialmemes")
    """


    for submission in subreddit.controversial(limit=1000):
        post_year = datetime.fromtimestamp(submission.created_utc).year

        if datetime.fromtimestamp(submission.created_utc).year == year \
        and datetime.fromtimestamp(submission.created_utc).month == month:
            print(submission.title)
            return submission.id

    return -1

reddit = praw.Reddit(
    user_agent="Subreddit statistics (by u/pir2022_)",
    client_id="L93ownPP-FtArtwOpikpEQ",
    client_secret="HKCzRao9EAVlKDYbHx_Sal27eqZclQ",
    username="pir2022_",
    password="steganographie",
)




# Output: 10 submissions

subreddit = reddit.subreddit("prequelmemes")
post = get_post_from_year(subreddit, 2016)

if hasattr(post, "crosspost_parent"):
    op = reddit.submission(id=post.crosspost_parent.split("_")[1])


# print("\n\n")
# print(subreddit.display_name)
# # Output: redditdev
# print("\n\n")
# print(subreddit.title)
# # Output: reddit development
# print("\n\n")
# print(subreddit.description)
# # Output: a subreddit for discussion of ...
# print("\n\n")
# print(subreddit.can_assign_user_flair)
