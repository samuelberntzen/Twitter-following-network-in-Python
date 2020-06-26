import tweepy
import pandas as pd
import time
import json
import pickle
import numpy as np


# Authentication

key = "BuKfT6TiMeq9wTtHNnn9lV5FD"

key_secret = "Ut5XfMkZ5Z6RdonPsyam2MVtU7pmZST24Llz8YlLsggQB6Ly3z"


token = "883325489800196097-D4UIdsCMv9KIPgG6cu6Gs7CjIoBxVfT"
token_secret = "QNJzZL6rE9PB3VVduZNpDw3342gEdy4AmiKJdQibGv7XU"


# Connect to API

auth = tweepy.OAuthHandler(key, key_secret)
auth.set_access_token(token, token_secret)
api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

# Retrieve screen_name for each unique ID 
# (This takes a while, up to several days. An alternative is to run a custom list with a fewer number of users, i.e influential users with many more followers)

ignored_users = 0

# Read relation array as dataframe
rel_array = pickle.load(open("friends_relation.dat", "rb"))
df = pd.DataFrame(rel_array, columns = ["from_id", "to_id"])

# Define function for returning screen_name
def translate_id(id_array):
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
            print("Error retrieving username, ignoring user {}...".format(i), end = "\r", flush = True)
            ignored_users += 1   
            print("Users ignored: ", ignored_users, end = "\r", flush = True)
    
    pickle.dump(keys, open("keys_id.dat", "wb"))
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


get_unique(df)
translate_id(unique)

df.to_csv("relation_array.csv")

keys = pickle.load(open("keys_id.dat", "rb"))
keys_df = pd.DataFrame(keys, columns = ["user_id", "screen_name"])
keys_df.to_csv("keys_id.csv")
