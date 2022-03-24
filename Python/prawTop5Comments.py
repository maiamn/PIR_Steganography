import praw

reddit = praw.Reddit(
    user_agent="Subreddit statistics (by u/pir2022_)",
    client_id="L93ownPP-FtArtwOpikpEQ",
    client_secret="HKCzRao9EAVlKDYbHx_Sal27eqZclQ",
    username="pir2022_",
    password="steganographie",
)

listSubmission=[]
for submission in reddit.subreddit("prequelmemes").top(limit=10):
    listSubmission.append(submission)

#5 commentaires les plus upvotés
submission = listSubmission[0]
top_level_comments = list(submission.comments)
for i in range(5):
    print(i)
    print(top_level_comments[i].body)

