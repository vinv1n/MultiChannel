import tweepy
import logging

logger = logging.getLogger(__name__)


class Twitter:

    def __init__(self, *args, **kwargs):

        # raises error when keys are missing
        self.auth = tweepy.OAuthHandler(kwargs.get('consumer_key'),
                                            kwargs.get('consumer_secret'))
        self.auth.set_access_token(kwargs.get('access_token'), kwargs.get('access_token_secret'))

        self.twitter_api = tweepy.Api(self.auth)

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("Twitter wrapper is initialized")

    def get_updates(self):
        pass

    def create_tweet(self, msg):
        pass

    def get_responses(self, tweet_id):
        pass
