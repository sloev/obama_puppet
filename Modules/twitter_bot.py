import json
from  youtubeapi import YoutubeApi
from twitterapi import TwitterApi
import twitter
import psycopg2
import time

DEC2FLOAT = psycopg2.extensions.new_type(
        psycopg2.extensions.DECIMAL.values,
        'DEC2FLOAT',
        lambda value, curs: float(value) if value is not None else None)
psycopg2.extensions.register_type(DEC2FLOAT)
default_speech = "                                america                 "
class Bot():
    def __init__(self):
        self.youtube = YoutubeApi()
        self.twitter = TwitterApi()
        with open(".counter.json") as f:
            j = json.load(f)
            self.counter = j["counter"]
            self.last_id = j["last_id"]

    def loop(self):
        conn = None
        try:
            conn = psycopg2.connect("dbname='postgres' user='johannes' host='localhost'")
            self.cur = conn.cursor()
            status_tuples = []
            self.cur.execute("SELECT * FROM config_store where key = \'root\';")
            self.root_path = self.cur.fetchone()[1]

            print "root", self.root_path
            while True:
                _last_id = None
                try:
                    status_tuples = []
                    for text, sender_id, tweet_id in self.twitter.tweet_generator():
                        if tweet_id > self.last_id:
                            if not _last_id:
                                _last_id = tweet_id
                            elif _last_id < tweet_id:
                                _last_id = tweet_id
                            status_tuples += [(text, sender_id, tweet_id)]
                    if _last_id:
                        self.last_id = _last_id
                    if not status_tuples:
                        print "no statusses"
                        time.sleep(30)
                        # status_tuples = [(default_speech, None, None)]
                    for text, sender_id, tweet_id in status_tuples:
                        print "uploading!:", text, " from:", sender_id, " message_id:", tweet_id
                        self._upload_speech(text, sender_id, tweet_id)
                        time.sleep(1)
                    conn.commit()
                except  twitter.error.TwitterError,e:
                    print "twitter error", e
                    time.sleep(30)
        finally:
            with open('.counter.json', 'w') as outfile:
                json.dump({"counter": self.counter, "last_id":self.last_id}, outfile) 
            if conn:
                conn.close()

    def _upload_speech(self, speech, user_id, reply_id):
        try:
            if not speech:
                speech = default_speech
            print "speech", speech, "user_id", user_id
            self.cur.execute("SELECT * FROM create_speech(\'%s\')" % speech)
            relative_path = self.cur.fetchone()[0]
            if not relative_path.startswith(self.root_path):
                print "panic ! not root path begins"
            print relative_path
            file_path = relative_path
            title = "speech number %d" % self.counter
            description = "github.com/sloev/obama-puppet | twitter.com/obama_puppet : speech: %s" % speech
            url = self.youtube.upload_video(file_path, title=title, description=description)
            print "url: ", url
            if not url:
                print "PANIC!!!"
                return
            self.twitter.post_update(url, reply_id)
            if user_id:
                self.counter += 1
                print "user_id", user_id
                self.cur.execute("""INSERT INTO users(id)
                    SELECT %s
                    WHERE NOT EXISTS (
                    SELECT id FROM users WHERE id=%s
                    )""", [str(user_id), str(user_id)])
                self.cur.execute("""INSERT INTO tweets(user_id, speech, url) VALUES (%s, %s, %s)""", [str(user_id), speech, url])
            with open('.counter.json', 'w') as outfile:
                print "saved to json"
                json.dump({"counter": self.counter, "last_id":self.last_id}, outfile)
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    bot = Bot()
    bot.loop()


