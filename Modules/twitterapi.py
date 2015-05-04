import json
import twitter

class TwitterApi():
    def __init__(self):
        config = json.load(open(".apiconfig.json"))
        self.api = twitter.Api(consumer_key=config["consumer_key"],
                consumer_secret=config["consumer_secret"],
                access_token_key=config["access_key"],
                access_token_secret=config["access_secret"])
        self.twitter_id = 16575380

    def post_update(self, url, reply_id):
        self.api.PostUpdate("new address: %s" % url, in_reply_to_status_id=reply_id)

    def tweet_generator(self, user='obama_puppet'):

        for status in self.api.GetMentions():
            status_text = status.text
            status_sender = status.user.id
            status_id = status.id
            if not status_sender == self.twitter_id:
                if status_text.startswith("@obama_puppet"):
                    index = status_text.index("@obama_puppet") + len("@obama_puppet")
                    yield status_text[index:], status_sender, status_id

if __name__ == "__main__":
    t = TwitterApi()
    #t.post_update("www.lol.com")
    count = 0
    for t, i in t.tweet_generator():
        print t,i 
