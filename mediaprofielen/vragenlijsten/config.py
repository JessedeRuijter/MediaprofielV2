import os
import sys


class MailChimpConfig:
    def __init__(self):
        apikey = "3c71ef098ca8f4fc96ce89bedb940003-us12"

        parts = apikey.split('-')
        if len(parts) != 2:
            print "This doesn't look like an API Key: " + apikey
            print "The API Key should have both a key and a server name, separated by a dash, like this: abcdefg8abcdefg6abcdefg4-us1"
            sys.exit()

        self.apikey = apikey
        self.shard = parts[1]
        self.api_root = "https://" + self.shard + ".api.mailchimp.com/3.0/"
