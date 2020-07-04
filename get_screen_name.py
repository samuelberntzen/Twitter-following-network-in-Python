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

# Retrieve screen_name for each unique ID 
# (This takes a while, up to several days. An alternative is to run a custom list with a fewer number of users, i.e influential users with many more followers)

ignored_users = 0

# Read relation array as dataframe
rel_array = pickle.load(open("data/friends_relation.dat", "rb"))
df = pd.DataFrame(rel_array, columns = ["from_id", "to_id"])

# Define function for returning screen_name
def get_screen_names(id_array):
    keys = []
    global ignored_users
    
    
    # For i in id_array where intra_network_followers is higher than the follower threshold:
    for i in id_array:
        #print(i)
        try:
            user = api.get_user(i)
            name = user.screen_name
            keys.append([i, name])
            print("\r Percent completed (updates automatically): {}".format(100*np.where(id_array==i)[0]/len(id_array)), end = "\r", flush = True)
        except tweepy.TweepError:
            print("Error retrieving username, ignoring user {}...".format(i), end = "\r")
            ignored_users += 1   
            print("Users ignored: ", ignored_users, end = "\r", flush = True)
    
    pickle.dump(keys, open("data/keys_id.dat", "wb"))
    return keys


# Return uniques from "to" and "from"
def get_unique(df):
    global unique

    # Split columns
    df_from = df["from_id"]
    df_to = df["to_id"]

    # Get uniques of each
    df_from = df_from.unique()
    df_to = df_to.unique()

    # Merge columns and get unique for both (inefficient, yes)
    unique = np.append(df_from, df_to)
    unique = pd.DataFrame(unique)
    unique = unique[0].unique()

def translate_dataframe(df, translation):
    rename_dict = translation.set_index("user_id").to_dict()["screen_name"]
    df = df.replace(rename_dict)

    df.to_csv("data/df_translated.csv", index = False)


get_unique(df)
get_screen_names(unique)

#df.to_csv("relation_array.csv")

keys = pickle.load(open("data/keys_id.dat", "rb"))
keys_df = pd.DataFrame(keys, columns = ["user_id", "screen_name"])
keys_df.to_csv("data/keys_id.csv")

translate_dataframe(df, keys_df)
