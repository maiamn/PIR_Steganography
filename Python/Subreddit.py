import praw

#online analysis : active user count





class SubredditImage:

    number_of_posts = 0
    number_of_days = 0
    number_of_reposts = 0
    number_of_crossposts = 0
    number_of_images = 0
    number_of_text = 0
    number_of_audio = 0
    number_of_gif = 0
    number_of_title = 0
    number_of_upvotes = 0


    def __init__(self, profile, year, month):
	    
	    #06/2016 : month and year or the image
        self.timestamp = month+"/"+year
        
        #post_at_date = profile.get_post_from_date(year, month)
        
        #Returns 100 posts (in exactly the time period or also after if sub is small/dead
        posts = get_posts(big=False)
        for post in posts:
            self.factor_in_post(post)
        
        
        
        #List : The 5 keywords corresponding to the sub found by other method
        self.keywords = self.get_keywords()
        
        
        #TODO: DO THE STATS
        
        
        self.number_posts_day = number_posts_day #Int : average amount of posts each day
        self.post_repost_percent = post_repost_percent  #Float : Percentage of posts that are reposts
        self.title_repost_percent = title_repost_percent #Float : If reposted, percentage of chance that the title was the same
        
        self.post_image_percent = post_image_percent #Float : Percentage of posts that are images
        self.post_text_percent = post_text_percent #Float : Percentage of posts that are text
        self.post_title_percent = post_title_percent #Float : Percentage of posts that are a title
        self.post_gif_percent = post_gif_percent #Float : Percentage of posts that are GIFS
        self.post_link_percent = post_link_percent #Float : Percentage of posts that are Audio
        self.post_crosspost_percent = post_crosspost_percent #Float : Percentage of posts that are crossposts
	    
        self.average_upvote_count = average_upvote_count #Int : Average amount of upvotes per post

        self.average_upvote_ratio = average_upvote_ratio
    
    
    def get_keywords(self):
        """
        Returns three keywords associated with the posts
        """
        
        pass
        

    def factor_in_post(post):
        """
        Takes the given into account for the statistics.
        """
        
        #check every parameter and increment the counts
        
        pass
        





#Variable to account for the evolution
class SubredditProfile:

    reddit = praw.Reddit(
        user_agent="Subreddit statistics (by u/pir2022_)",
        client_id="L93ownPP-FtArtwOpikpEQ",
        client_secret="HKCzRao9EAVlKDYbHx_Sal27eqZclQ",
        username="pir2022_",
        password="steganographie",
    )

    def __init__(self, name):
        
        subreddit = self.reddit.subreddit(name)
        
        self.name = name #String : Name of the subreddit
        
        #Boolean : Has repost sleuth bot authorized, can check posts easily
        #self.sleuthbot_authorized = sleuthbot_authorized 
        
        #Int : the amount of subs
        self.subscriber_count = subreddit.subscribers
        
        #String : the description
        self.description = subreddit.public_description
        
        #Boolean : If the sub has repost flairs
        self.has_repost_flairs = self.check_reposts_flairs(subreddit.flair(limit=None))
        
        #Boolean : If reposts are allowed
        self.reposts_allowed = check_reposts_allowed(subreddit.rules)
        
        self.can_self_assign_flair = subreddit.can_assign_user_flair
        self.subreddit_images = []
	
    def check_reposts_allowed(rules):
        """
        Checks in the rules whether reposts are allowed.
        """
            
        trigger_words = [
            "low-quality", "reposts",
            "low quality",
            "redundant", "oc"
        ]
        
        okay_words = [
            "short-term repost", "short term repost", "reposts are ok",
            "reposts are fine", "reposts are okay", "reposts are allowed",
        ]
            
        #We parse the rules and their descriptions to check if reposts are explicitly
        #allowed
        for rule in rules:
            if any(x in str(rule).lower() for x in okay_words) or \
            any(x in rule.description.lower() for x in okay_words):
                return True
        
        for rule in rules:
            if any(x in str(rule).lower() for x in trigger_words) or \
            any(x in rule.description.lower() for x in trigger_words):
                return False
        
        return True
	    
    def get_post_from_date(subreddit, year, month):
        """
        Returns id of a post from the given year in the given sub
        subreddit object comes from reddit.subreddit("memes") for ex.
        """

        for submission in subreddit.controversial(limit=1000):
            post_year = datetime.fromtimestamp(submission.created_utc).year

            if datetime.fromtimestamp(submission.created_utc).year == year \
            and datetime.fromtimestamp(submission.created_utc).month == month:
                return submission

        return -1
	
	def check_repost_flair(flairs):
	    """
	    Checks if there exists a flair dedicated to flagging reposts.
	    """
	    
	    for flair in flairs:
            if "repost" in str(flair).lower:
                return True
        
        return False
	
	
    def append_image(self, year, month):
        
        if any(x.year == year or x.month == month for x in self.subreddit_images):
            return -1
        new_image = SubredditImage(year, month)
        self.subreddit_images.append(new_image)
        

    def get_method(self):
        return 0
        
tests = [
    "memes", "science", "math", "engineeringmemes", "pokemon", "football",
    "MartialMemes", "funny", "gaming", "music"
]

for subreddit in tests:
    test = SubredditProfile(subreddit)
    print(test.name + " : " + str(test.reposts_allowed))


