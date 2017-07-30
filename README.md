#TweetHose

This app collects tweets containing a keyword over a user-specified amount of time, then outputs visualizations that summarize the sentiment, origin location, and most-used words of the tweets. 

In addition to the required packages, the user must have his or her own keys in order to access the Twitter Stream API. 

To run this app, simply download this repository and run the tweethose.py file in the app directory. 

The user will be prompted to input a keyword, which will be used as the search criteria for tweets. Next, the user must input the length of time (in minutes) for which the application will gather tweets. Once this amount of time is over, the app will create three visualizations, including a histogram of tweet sentiment, a pie chart of the locations that the tweets are generated from, and a wordcloud of the most-used words in the collected tweets (excluding the keyword). 
