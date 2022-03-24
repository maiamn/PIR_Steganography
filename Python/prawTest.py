import praw
from datetime import datetime




reddit = praw.Reddit(
    user_agent="Subreddit statistics (by u/pir2022_)",
    client_id="L93ownPP-FtArtwOpikpEQ",
    client_secret="HKCzRao9EAVlKDYbHx_Sal27eqZclQ",
    username="pir2022_",
    password="steganographie",
)
i=0
for submission in reddit.subreddit("prequelmemes").top(limit=10):
    
    timestamp = submission.created_utc
    print(timestamp)
    dt_object = datetime.fromtimestamp(timestamp)
    print(dt_object)

# Output: 10 submissions

subreddit = reddit.subreddit("martialmemes")

print("\n\n")
print(subreddit.display_name)
# Output: redditdev
print("\n\n")
print(subreddit.title)
# Output: reddit development
print("\n\n")
print(subreddit.description)
# Output: a subreddit for discussion of ...
print("\n\n")
print(subreddit.can_assign_user_flair)
