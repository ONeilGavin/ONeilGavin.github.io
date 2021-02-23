import tweepy
from tweepy import Stream
import time
from datetime import datetime as dt
from datetime import timedelta
from pytz import timezone
import csv

floyd_count = 0
protest_count = 0
defund_count = 0
logged = False
filename = 'twitterstats.csv'

class Listener(tweepy.StreamListener):

    def __init__(self, api=None):
        self.api = api
        super(Listener, self).__init__()

    def on_status(self, status):
        """Listens to stream of all tweets containing the hashtags and increments respective variables"""
        now = dt.now(timezone(('US/Eastern')))

        if now.hour == 0 and now.minute == 0:
            global logged

            if not logged:
                logged = True
                log(False)
                return False

        # Check status at noon
        elif now.hour == 12 and 5 > now.minute > 0:
            print('NOON CHECK: ' + str(defund_count) + ' ' + str(floyd_count) + ' ' + str(protest_count))
            logged = False

        try:
            lower = status.text.lower()
            if not 'rt @' in lower:
                # A tweet that contains, for example, both #blm and #protest should update the counters for both of
                # those hashtags
                if '#defundthepolice' in lower:
                    update_count(1)
                if '#georgefloyd' in lower:
                    update_count(2)
                if '#protest' or '#protests' in lower:
                    update_count(3)

        except Exception as e:
            print(e)
            log(True)
            return False

    def on_error(self, status_code):
        if status_code == 420:
            # Disconnect stream
            print('Status code 420')
            log(True)
            return False


def update_count(mode):
    """1 for defundthepolice, 2 for georgefloyd, 3 for protest, and 4 to reset all"""
    global floyd_count
    global protest_count
    global defund_count

    if mode == 1:
        defund_count += 1
    elif mode == 2:
        floyd_count += 1
    elif mode == 3:
        protest_count += 1
    elif mode == 4:
        floyd_count = 0
        protest_count = 0
        defund_count = 0

def start():
    # API credentials
    consumer_key = 'XXX'
    consumer_secret = 'XXX'
    access_token = 'XXX'
    access_secret = 'XXX'

    listen = Listener()

    # API login
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    stream = Stream(auth, listen)
    print('Starting')
    try:
        stream.filter(track=['#georgefloyd', '#protest', '#defundthepolice', '#protests'])
    except Exception as error:
        print(error)
        time.sleep(5)
        print('Stream filter error')
        log(True)

def log(error):
    if error:
        now = dt.now(timezone(('US/Eastern')))
        print('Error: resuming stream @ ' + str(now.hour) + ':' + str(now.minute))
        print('Got ' + str(defund_count) + ' tweets so far')
        time.sleep(5)
        start()
    else:
        with open(filename, 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            # Write date in yyyy/mm/dd format and total number of tweets from that date
            yesterday = dt.today() - timedelta(days=1)
            yesterday_date = yesterday.strftime("%Y-%m-%d")
            csvwriter.writerow([yesterday_date, '#GeorgeFloyd', floyd_count])
            csvwriter.writerow([yesterday_date, '#Protest', protest_count])
            csvwriter.writerow([yesterday_date, '#Defundthepolice', defund_count])

        print('Logged tweets @ ' + yesterday_date)
        update_count(4)
        time.sleep(1)
        start()

print('Launching tracker')
start()
