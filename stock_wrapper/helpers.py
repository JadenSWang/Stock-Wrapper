class helpers():
    class urls():
        # authentification
        @property
        def login_url(self):
            return 'https://api.robinhood.com/oauth2/token/'

        @property
        def challenge_url(self, challenge_id):
            return 'https://api.robinhood.com/challenge/{0}/respond/'.format(challenge_id)

        # profile
        @property
        def positions(self):
            return "https://api.robinhood.com/positions/"

        # data