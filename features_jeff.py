from clpsych import store
from clpsych import data
from readability import Readability
from data import read_indices
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def get_sentiment(text):
        sid = SentimentIntensityAnalyzer()
        return sid.polarity_scores(text)['compound']

def get_readability(text):
	txt = Readability(text)
	return txt.FleschReadingEase()

def get_smog(text):
	txt = Readability(text)
	try:
		return txt.SMOGIndex()
	except ZeroDivisionError:
		return 0

#hour of post		
def get_hour(t):
	return t.hour

#Whether post was in range where we saw a difference between controls and positives
def hour_check(h):
	if h < 6:
		return 1
	else:
		return 0
	
#load data	
load = store.Store('data.h5')

### For running on all items: Make a copy of dataframe
df = load.documents.copy()

# For running on just a sample
indices = data.read_indices('SAMPLE.txt')
df = load.select(indices, df=load.documents)

#Feature: time since last post (in hours)
df.sort_values(['user_id','time'], inplace=True)
df['diff'] = [n for n in df.groupby('user_id', sort=False)['time'].diff()]
df['time_since_last_post'] = df['diff'].apply(lambda x: x.total_seconds()/3600)

#Feature: Hour of post
df = df.assign(hour=df.time.apply(get_hour))
#Feature: whether it was at night
df['night_post'] = df.hour.apply(hour_check)
#Save to csv
df[['user_id','post_id','subreddit','hour','night_post','time_since_last_post']].to_csv('timing.csv')

#Feature: readability
df = df.assign(text_readability=df.text.apply(get_readability))
df = df.assign(title_readability=df.title.apply(get_readability))

#Feature: SMOG
df = df.assign(text_smog=df.text.apply(get_smog))
df = df.assign(title_smog=df.title.apply(get_smog))
#Save to csv
df[['user_id','post_id','title_readability','text_readability','title_smog','text_smog']].to_csv('readability.csv')


#Feature: Sentiment
df = df.assign(text_sentiment=df.text.apply(get_sentiment))
df = df.assign(title_sentiment=df.title.apply(get_sentiment))
#Save to csv
df[['user_id','post_id','title_sentiment','text_sentiment']].to_csv('sentiment.csv')

load.finalize()









