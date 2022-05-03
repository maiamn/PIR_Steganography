# from re import sub
import praw # praw-7.5.0

import datetime as dt
from datetime import date
from datetime import timedelta

from psaw import PushshiftAPI
from prawcore.exceptions import Forbidden
import numpy as np

from sklearn.linear_model import LinearRegression

# Ignore PushShift warning ("Not all PushShift shards are active.")
import warnings
warnings.filterwarnings("ignore")

# online analysis : active user count

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
    number_of_title = 0
    number_of_upvotes = 0
    sum_of_upvote_ratio = 0
    number_of_known = 0
    number_of_unknown = 0

    # dictionary of subreddits from which there are crossposts
    # associated with the amount of crossposts for each
    crosspost_subs = {}

    def __init__(self, profile, startYear, startMonth, startDay, n):

        # 06/2016 : month and year or the image
        self.begin_timestamp = f"{startDay}/{startMonth}/{startYear}"
        self.year = startYear
        self.month = startMonth
        self.day = startDay
        # self.end_timestamp = f"{endMonth}/{endYear}"

        self.profile = profile

        #Length between creation of subreddit and today in number of days
        #the x axis for LinearRegression
        self.day_index = (date.fromtimestamp(self.profile.created_date) - date(startYear, startMonth, startDay)).days

        # Returns n posts (in exactly the time period)
        endMonth = startMonth+1
        endYear = startYear
        if startMonth == 12:
            endMonth = 1
            endYear = startYear + 1
        posts = self.get_posts_within_range(startYear, endYear, startMonth, endMonth, startDay, n)

        self.do_stats(posts)

        # List : The 5 keywords corresponding to the sub found by other method
        self.keywords = self.get_keywords()

        # Float : Percentage of posts that are reposts
        self.post_repost_percent = 100 * self.number_of_reposts / self.number_of_posts

        # Float : Percentage of posts that are images
        self.post_image_percent = 100 * self.number_of_images / self.number_of_posts

        # Float : Percentage of posts that are text
        self.post_text_percent = 100 * self.number_of_text / self.number_of_posts

        # Float : Percentage of posts that are a title
        self.post_title_percent = 100 * self.number_of_title / self.number_of_posts

        # Float : Percentage of posts that are crossposts
        self.post_crosspost_percent = 100 * self.number_of_crossposts / self.number_of_posts
        
        # Float : Percentage of posts that are a link
        self.post_link_percent = 100 * self.number_of_links / self.number_of_posts

        # Int : Average amount of upvotes per post
        self.average_upvote_count = self.number_of_upvotes / self.number_of_posts

    def do_stats(self, posts):
        current_day = date.fromtimestamp(posts[0].created_utc)
        les_n = []  # list of number of posts in a day
        n = 0  # number of posts for this day

        for i, post in enumerate(posts):

            this_day = date.fromtimestamp(post.created_utc)
            if this_day.month == current_day.month and \
                    this_day.day == current_day.day:

                n += 1

            else:
                les_n.append(n)
                n = 0
                current_day = this_day

            self.increment_stats(post)
            
            if i%5==0:
                print(f"Test n°{i}/{len(posts)}")

        if n > 0:
            les_n.append(n)

        # Number of days the image is based on
        self.number_of_days = 1 + (date.fromtimestamp(posts[0].created_utc) - date.fromtimestamp(posts[-1].created_utc)).days
        self.number_of_posts = len(posts)
        self.number_posts_day = (100 / self.number_of_days)*100

        end_datetime = date.fromtimestamp(post.created_utc)
        self.end_timestamp = f"{end_datetime.month}/{end_datetime.year}"

    def get_keywords(self):
        """
        Returns three keywords associated with the posts
        """

        return []  # TODO

    def repostInTopFiveComments(self, submission):

        top_level_comments = list(submission.comments)[:5]
        for c in top_level_comments:
            if "repost" in c.body.lower():
                return True

        return False

    def checkIsRepost(self, submission):

        # If no flair
        if submission.link_flair_text is None:
            if submission.is_original_content:
                self.number_of_known += 1
                return False
            if self.repostInTopFiveComments(submission):
                self.number_of_known += 1
                print(f"{submission.title} : {submission}")
                return True

            self.number_of_unknown += 1

            return False

        # If flair
        if submission.is_original_content or "OC" in submission.link_flair_text:
            self.number_of_known += 1
            return False

        if self.repostInTopFiveComments(submission) or "repost" in submission.link_flair_text.lower():
            self.number_of_known += 1
            print(f"{submission.title} : {submission}")
            return True

        self.number_of_unknown += 1
        # By default, post is not a repost
        return False

    def get_posts_within_range(self, startYear, endYear, startMonth, endMonth, startDay, max_posts):
        """
        Returns list of the first n posts between two given dates (Returns a generator object).
        month and year are integers
        max_posts <= 1000 (default : 100)
        """

        start_epoch = int(dt.datetime(startYear, startMonth, startDay).timestamp())  # Could be any date
        
        #startDay can be any day, end day can't be 31 (wll bug for some months)
        #putting 1 means sometimes there won't be enough posts but then it will restart
        #by adding a month so it will fix itself.
        stop_epoch = int(dt.datetime(endYear, endMonth, 1).timestamp())

        submissions_generator = self.profile.api.search_submissions(
            after=start_epoch,
            before=stop_epoch,
            subreddit=self.profile.subreddit,
            limit=max_posts
            # filter=['url','author', 'title', 'subreddit']
        )
        
        # If the list is too short, add a month and repeat
        first_list = list(submissions_generator)
        if len(first_list) < max_posts:
            
            if endMonth == 12:
                endMonth = 1
                endYear += 1
            else:
                endMonth += 1
                
            l = self.get_posts_within_range(startYear, endYear, startMonth, endMonth, startDay, max_posts)
            
            return l
        
        else:
            
            return first_list

    def increment_stats(self, post):
        """
        Checks if the post is a repost, crosspost, checks number of upvotes
        and increments the counters.
        """

        if hasattr(post, "crosspost_parent"):
            op = self.profile.reddit.submission(id=post.crosspost_parent.split("_")[1])
            original_sub = op.subreddit.display_name

            self.number_of_crossposts += 1
            if original_sub in self.crosspost_subs:
                self.crosspost_subs[original_sub] += 1
            else:
                self.crosspost_subs[original_sub] = 1


        if post.is_self:
                
                if post.selftext == "":
                    self.number_of_title += 1
                    
                else:
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
                print(f"Unkown post {post}")

        # harder to know
        else:

            if post.domain == 'i.redd.it':
                self.number_of_images += 1
            elif post.domain == 'v.redd.it':
                self.number_of_videos += 1
            
            else:
                self.number_of_links += 1


        if self.checkIsRepost(post):
            self.number_of_reposts += 1

        self.sum_of_upvote_ratio += post.upvote_ratio

        self.number_of_upvotes += post.score


# Variable to account for the evolution
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

        self.api = PushshiftAPI(self.reddit)

        self.name = name  # String : Name of the subreddit
        
        self.created_date = self.subreddit.created_utc

        # Boolean : if post hints are enabled
        self.post_hints_enabled = self.check_post_hints()

        # Int : the amount of subs
        self.subscriber_count = self.subreddit.subscribers

        # String : the description
        self.description = self.subreddit.public_description

        # Boolean : If the sub has repost flairs
        try:
            self.has_repost_flairs = self.check_repost_flair(self.subreddit.flair(limit=None))
        except Forbidden:
            self.has_repost_flairs = False

        # Boolean : If reposts are allowed
        self.reposts_allowed = self.check_reposts_allowed(self.subreddit.rules)
        
        

        self.can_self_assign_flair = self.subreddit.can_assign_user_flair
        if self.can_self_assign_flair:
            req = self.subreddit.post_requirements()
            self.must_assign_flair = req["is_flair_required"]
        else:
            self.must_assign_flair = False
            
        self.subreddit_images = []
        
        self.init_n_images_spread(5, 10)

        self.parse_images()
        
    
    def init_n_images_spread(self, n_dates, sample_size):
        
        dates = self.get_n_dates(n_dates)
        
        for i, d in enumerate(dates):
            
            self.append_image(d.year, d.month, d.day, sample_size)
            
            print(f"Image {i+1}/{len(dates)} ok")
    
    def get_n_dates(self, n=5):
        
        start = date.fromtimestamp(self.created_date)
        end = date.today()
        
        n_days = (end - start).days
        day_index = np.linspace(0, n_days, n+1)
        
        return [start+timedelta(days=int(x)) for x in day_index[:-1]]
        

    def check_post_hints(self):

        submission = self.subreddit.new(limit=1)
        return 'post_hint' in vars(submission)

    def check_reposts_allowed(self, rules):
        """
        Checks in the rules whether reposts are allowed.
        """

        trigger_words = [
            "low-quality", "repost",
            "low quality",
            "redundant", " oc "
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

    def check_repost_flair(self, flairs):
        """
        Checks if there exists a flair dedicated to flagging reposts.
        """

        for flair in flairs:
            if "repost" in str(flair).lower:
                return True

        return False

    def append_image(self, year, month, day, n):

        if any(x.year == year and x.month == month for x in self.subreddit_images):
            raise ValueError("Image already exists for this month")

        new_image = SubredditImage(self, year, month, day, n)
        self.subreddit_images.append(new_image)
        
        

        return new_image


    def parse_images(self):
        """Does the calculations based on the images (average, evolution)"""
        
        
        repost_list = []
        img_list = []
        txt_list = []
        title_list = []
        crosspost_list = []
        link_list = []
        upvote_list = []
        
        n_images = len(self.subreddit_images)
                
        for img in self.subreddit_images:
            repost_list.append(img.post_repost_percent)
            img_list.append(img.post_image_percent)
            txt_list.append(img.post_text_percent)
            title_list.append(img.post_title_percent)
            crosspost_list.append(img.post_crosspost_percent)
            link_list.append(img.post_link_percent)
            upvote_list.append(img.average_upvote_count)
        
        self.post_repost_percent = 100 * sum(repost_list) / n_images
        self.post_image_percent = 100 * sum(img_list) / n_images
        self.post_text_percent = 100 * sum(txt_list) / n_images
        self.post_title_percent = 100 * sum(title_list) / n_images
        self.post_crosspost_percent = 100 * sum(crosspost_list) / n_images
        self.post_link_percent = 100 * sum(link_list) / n_images
        self.average_upvote_count = sum(upvote_list) / n_images

        print(f"AVERAGE UPVOTE COUNT : {self.average_upvote_count}")

        #TODO: https://realpython.com/linear-regression-in-python/#when-do-you-need-regression

        x = np.array([img.day_index for img in self.subreddit_images]).reshape((-1, 1))
        #y = repost_list
        model = LinearRegression()
        model.fit(x, repost_list)
        print(f"COEFFICIENT : {model.coef_}")



    def get_method(self):
        
        if len(self.subreddit_images) < 5:
            raise ValueError("Not enough samples to determine the best method.")
        
        # Whether allowed or not, we need to copy another post
        # since we can't decide accurately what flair to use
        if self.must_assign_flair:
            return "repost"
        
        #We do the stats on the images
        self.parse_images()
        
        # If reposts aren't allowed but still exist in a large enough quantity
        # if not self.reposts_allowed and self.avg_repost_percent > 15:
        #     pass

        
        return 0


# tests = [
#     "memes", "science", "math", "engineeringmemes", "pokemon", "football",
#     "MartialMemes", "funny", "gaming", "music"
# ]

tests = ["martialmemes"]

for subreddit in tests:
    test = SubredditProfile(subreddit)
    
    print(test.get_n_dates())
    
    print(f"/// {test.name} ///")
    print(f"Post hints : {test.post_hints_enabled}")
    #print(f"Sub count : {test.subscriber_count}")
    #print(f"Description : {test.description}")
    print(f"Repost flairs : {test.has_repost_flairs}")
    print(f"Repost allowed : {test.reposts_allowed}")
    print(f"Self-assign flair : {test.can_self_assign_flair}")
    print(f"Must assign flair : {test.must_assign_flair}")

    #image = test.append_image(2022, 4, 100)
    for i, img in enumerate(test.subreddit_images):
        
        print("////////////////////////")
        print(f"IMAGE N°{i}/{len(test.subreddit_images)}")
        print("////////////////////////")

        print(f"Repost% : {img.post_repost_percent}")
        print(f"Img% : {img.post_image_percent}")
        print(f"Txt% : {img.post_text_percent}")
        print(f"Title% : {img.post_title_percent}")
        print(f"Link% : {img.post_link_percent}")
        print(f"Crosspost% : {img.post_crosspost_percent}")
        print(f"Upvote avg : {img.average_upvote_count}")

        print(f"Ndays : {img.number_of_days}")

        print(f"Known nb : {img.number_of_known}")
        print(f"Unknown nb : {img.number_of_unknown}")
    
    
