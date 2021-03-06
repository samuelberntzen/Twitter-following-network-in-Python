import tweepy
import pandas as pd
import time
import json
import pickle
import numpy as np

# This is my own file containing private API keys, replace your API keys in a corresponding file of your own or directly in the code
import keys


# Authentication

key = keys.api_key
key_secret = keys.api_secret
token = keys.token
token_secret = keys.token_secret


# Connect to API

auth = tweepy.OAuthHandler(key, key_secret)
auth.set_access_token(token, token_secret)
api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

# Global variables
start = time.time()
used_id = []


# Define function for retrieving friends of a user
# NOTE THAT THE INPUT MUST BE USER ID
# This website can be used for retrieving user_id: https://tweeterid.com/

def get_friends(user_id):
    print("\r Retrieving friends for:\t\t\t\t\t",user_id, end = "\r")
    ids = []
    friends_array = []
    
    used_id.append(user_id)
    
    try:
        for page in tweepy.Cursor(api.friends_ids, user_id = user_id).pages():
            ids.extend(page)
            friends_array.extend(ids)

        # friends_array returns a friends-relationship in [to, from] format
        return friends_array
    except tweepy.TweepError:
        print("Failed to run the command on that user, Skipping...", end = "\r")
        
# Define recursive function for network- retrieval
def get_friends_network(relation_array, user_id, wanted_level):
    global start
    global used_id
    
    if wanted_level == 0:
        return []
    
    # Retrieve user's friends:
    friend_list = get_friends(user_id)
    
    # Retrieve friends' friends:
    if not friend_list:
        print("Error retrieving friends", end = "\r")
    else:
        for friend in friend_list:
            if friend != user_id:
                relation_array.append([user_id,friend])
                if friend not in used_id:
                    relation_array.extend(get_friends_network([], friend, wanted_level - 1))
                
                
    # Dump data to file
    pickle.dump(relation_array, open("data/friends_relation.dat", "wb"))
    return relation_array



# TWEAK THESE INPUTS FOR CHANGING USER_ID AND LEVEL ===================================
# Example using @realDonaldTrump (25073877)
get_friends_network([], "25073877", 2)
