import praw

reddit = praw.Reddit(
    user_agent="Subreddit statistics (by u/pir2022_)",
    client_id="L93ownPP-FtArtwOpikpEQ",
    client_secret="HKCzRao9EAVlKDYbHx_Sal27eqZclQ",
    username="pir2022_",
    password="steganographie",
)

listSubmission=[]
for submission in reddit.subreddit("nostupidquestions").top(limit=10):
    listSubmission.append(submission)

#Posts ne contenant qu'un titre
for submission in listSubmission:
    print(submission.title)
    print(submission.selftext)
    print(submission.is_self and submission.selftext=="")
    print("------")