from re import sub
import praw
import datetime as dt
from psaw import PushshiftAPI

#online analysis : active user count

# check quality : stats of subreddit
# if adding 100 new posts does not skew the stats then good
# i.e. compare an image of the sub with an artificial image



class SubredditImage:

    number_of_posts = 0
    number_of_days = 0
    number_of_reposts = 0
    number_of_crossposts = 0
    number_of_images = 0
    number_of_text = 0
    number_of_videos = 0
    number_of_links = 0
    number_of_gif = 0
    number_of_title = 0
    number_of_upvotes = 0
    sum_of_upvote_ratio = 0

    # dictionary of subreddits from which there are crossposts
    # associated with the amount of crossposts for each
    crosspost_subs = {} 


    def __init__(self, profile, year, month):
	    
	    #06/2016 : month and year or the image
        self.begin_timestamp = f"{month}/{year}"
        self.profile = profile
        #post_at_date = profile.get_post_from_date(year, month)
        
        #Returns 100 posts (in exactly the time period or also after if sub is small/dead
        posts = self.get_posts_from_date(year, month, 1, 1000)

        self.do_stats(posts)
        
        
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
    

    def do_stats(self, posts):
        
        current_day = dt.fromtimestamp(posts[0].created_utc)
        les_n = [] # list of number of posts in a day
        n = 0 # number of posts for this day

        for post in posts:
            
            this_day = dt.fromtimestamp(posts.created_utc)
            if this_day.month == current_day.month and \
                this_day.day == current_day.day:

                n += 1
            
            else:
                les_n.append(n)
                n = 0
                current_day = this_day
            
            self.increment_stats(post)

        if n > 0:
            les_n.append(n)
        
        # Number of days the image is based on
        number_of_days = (dt.fromtimestamp(posts[0].created_utc) - dt.fromtimestamp(posts[-1].created_utc)).day
        self.number_of_posts = len(posts)
        self.number_posts_day = sum(les_n)/number_of_days

        end_datetime = dt.fromtimestamp(post.created_utc)
        self.end_timestamp = f"{end_datetime.month}/{end_datetime.year}"

    
    def get_keywords(self):
        """
        Returns three keywords associated with the posts
        """
        
        pass


    def get_posts_from_date(self, year, month, day, n):
        """
        Returns list of the first n posts after the given date.
        n <= 1000
        """
        
        start_epoch=int(dt.datetime(year, month, day).timestamp()) # Could be any date

        submissions_generator = self.profile.api.search_submissions(
            after=start_epoch,
            subreddit=self.profile.subreddit, 
            limit=n
        ) # Returns a generator object
        
        return list(submissions_generator) #list of submissions


    def increment_stats(self, post):
        """
        Checks if the post is a repost, crosspost, checks number of upvotes
        and increments the counters.
        """

        if hasattr(post, "crosspost_parent"):
            op = self.profile.subreddit.submission(id=post.crosspost_parent.split("_")[1])
            original_sub = op.subreddit.display_name

            number_of_crossposts += 1
            if original_sub in self.crosspost_subs:
                self.crosspost_subs[original_sub] += 1
            else:
                self.crosspost_subs[original_sub] = 1

        # always possible to know
        if post.is_self:
            self.number_of_text += 1

        # easy to know
        elif self.profile.post_hints_enabled:

            if 'image' in post.post_hint:
                self.number_of_images += 1
            elif 'video' in post.post_hint:
                self.number_of_videos += 1
            elif 'link' in post.post_hint:
                self.number_of_links += 1
            else:
                print(f"{post.title} -> type unknown")
                
        # harder to know
        elif post.is_reddit_media_domain:

            if post.domain == 'i.redd.it':
                self.number_of_images += 1
            elif post.domain == 'v.redd.it':
                self.number_of_videos += 1
            else:
                self.number_of_links += 1

        number_of_reposts = 0
        number_of_title = 0
        self.sum_of_upvote_ratio += post.upvote_ratio
        self.number_of_upvotes += post.score
        
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
        
        self.subreddit = self.reddit.subreddit(name)

        self.api = PushshiftAPI(subreddit)
        
        self.name = name #String : Name of the subreddit
        
        #Boolean : Has repost sleuth bot authorized, can check posts easily
        #self.sleuthbot_authorized = sleuthbot_authorized

        #Boolean : if post hints are enabled
        self.post_hints_enabled = self.check_post_hints()
        
        #Int : the amount of subs
        self.subscriber_count = self.subreddit.subscribers
        
        #String : the description
        self.description = self.subreddit.public_description
        
        #Boolean : If the sub has repost flairs
        self.has_repost_flairs = self.check_reposts_flairs(subreddit.flair(limit=None))
        
        #Boolean : If reposts are allowed
        self.reposts_allowed = self.check_reposts_allowed(subreddit.rules)
        
        self.can_self_assign_flair = self.subreddit.can_assign_user_flair
        self.subreddit_images = []


    def check_post_hints(self):

        submission = self.subreddit.new(limit=1)
        return 'post_hint' in vars(submission)
	

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
            
        # We parse the rules and their descriptions to check if reposts are explicitly
        # allowed
        for rule in rules:
            if any(x in str(rule).lower() for x in okay_words) or \
            any(x in rule.description.lower() for x in okay_words):
                return True
        # If they aren't explicitly allowed then the keywords are here to forbid
        # them.
        for rule in rules:
            if any(x in str(rule).lower() for x in trigger_words) or \
            any(x in rule.description.lower() for x in trigger_words):
                return False
        
        return True
	    
	
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


