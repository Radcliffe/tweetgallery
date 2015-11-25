from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import sqlite3
import sys
conn = sqlite3.connect('tweets.db')
   
#consumer key, consumer secret, access token, access secret.
ckey="Mc8uS9079DGytFkIFI1U8qmog"
csecret="834x4mRXytjxB6PPouDKUBJwVsLHwBQHo6CQ99MjEhpjT0Hy5J"
atoken="75167900-9sxfK8BB6iNFwGDJcNwsVETLe2utmKGhGuLXYV23f"
asecret="6g5AndosvD39Znrr7YXknUVXZsZpkgdxuKtHQWXxEUToO"

class listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
        user = all_data.get('user')
        if user and 'screen_name' in user:
            username = user["screen_name"]
            text = all_data["text"]
            if text.startswith('RT') or (' RT ' in text):
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
                                  text, media_url, 0, 
                                  searchterm_nohash))
                        print media_url
                        conn.commit()
                        break
        return True

    def on_error(self, status):
        print status

if __name__ == '__main__':

    args = sys.argv
    if len(args) < 2:
        sys.exit("No search term specified")
    searchterm = ' '.join(args[1:])
    searchterm_nohash = searchterm.replace('#', '').replace(' ','_')
    print searchterm, searchterm_nohash
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)

    twitterStream = Stream(auth, listener())
    while True:
        try:
            twitterStream.filter(track=[searchterm])
        except AttributeError:
            print 'Attribute Error:', sys.exc_info()[0]
            
