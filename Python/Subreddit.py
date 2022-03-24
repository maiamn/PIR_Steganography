#online analysis : active user count

class SubredditImage:

    def __init__(self, timestamp, number_posts_day, post_repost_percent,
    title_repost_percent, has_repost_flairs, keywords, post_image_percent,
    post_text_percent, post_title_percent, post_gif_percent, post_link_percent,
	post_crosspost_percent, average_upvote_count, average_upvote_ratio): 
	    
        self.timestamp = timestamp #Datetime : date of the image, all the data was gathered at that point
        self.number_posts_day = number_posts_day #Int : average amount of posts each day
        self.post_repost_percent = post_repost_percent  #Float : Percentage of posts that are reposts
        self.title_repost_percent = title_repost_percent #Float : If reposted, percentage of chance that the title was the same
        self.has_repost_flairs = has_repost_flairs #Boolean : If the sub has repost flairs
	    
        self.keywords = keywords #List : The 5 keywords corresponding to the sub found by other method
        self.post_image_percent = post_image_percent #Float : Percentage of posts that are images
        self.post_text_percent = post_text_percent #Float : Percentage of posts that are text
        self.post_title_percent = post_title_percent #Float : Percentage of posts that are a title
        self.post_gif_percent = post_gif_percent #Float : Percentage of posts that are GIFS
        self.post_link_percent = post_link_percent #Float : Percentage of posts that are Audio
        self.post_crosspost_percent = post_crosspost_percent #Float : Percentage of posts that are crossposts
	    
        self.average_upvote_count = average_upvote_count #Int : Average amount of upvotes per post

        self.average_upvote_ratio = average_upvote_ratio




#Variable to account for the evolution
class SubredditProfile:

    def __init__(self, name, subscriber_count, reposts_allowed,
    sleuthbot_authorized, description, can_self_assign_flair):
    
        self.name = name #String : Name of the subreddit
        self.sleuthbot_authorized = sleuthbot_authorized #Int : the amount of subs
        self.reposts_allowed = reposts_allowed #Boolean : If reposts are allowed
        self.subscriber_count = subscriber_count #Boolean : Has repost sleuth bot authorized, can check posts easily
        self.description = description #String : the description
        self.can_self_assign_flair = can_self_assign_flair
        self.subreddit_images = []
	
    def append_image(self):

        new_image = SubredditImage()
        self.subreddit_images.append(new_image)

    def get_method(self):
        return 0