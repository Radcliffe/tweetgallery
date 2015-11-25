from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import sqlite3
conn = sqlite3.connect('tweets.db')
   
#consumer key, consumer secret, access token, access secret.
ckey="Mc8uS9079DGytFkIFI1U8qmog"
csecret="834x4mRXytjxB6PPouDKUBJwVsLHwBQHo6CQ99MjEhpjT0Hy5J"
atoken="75167900-9sxfK8BB6iNFwGDJcNwsVETLe2utmKGhGuLXYV23f"
asecret="6g5AndosvD39Znrr7YXknUVXZsZpkgdxuKtHQWXxEUToO"

searchterm = '#PlutoFlyBy'

class listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
        user = all_data.get('user')
        if user and 'screen_name' in user:
            username = user["screen_name"]
            text = all_data["text"]
            if text.startswith('RT'):
                return True
            extended = all_data.get('extended_entities')
            timestamp_ms = all_data.get('timestamp_ms')
            if extended:
                media = extended.get('media', [])
                for m in media:
                    media_url = m.get('media_url_https')
                    if media_url:
                        conn.execute('insert into tweets values (?,?,?,?,?,?)',
                                 (timestamp_ms, username, 
                                  text, media_url, 0, searchterm))
                        print media_url
                        conn.commit()
                        break
        return True

    def on_error(self, status):
        print status



auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=[searchterm])
