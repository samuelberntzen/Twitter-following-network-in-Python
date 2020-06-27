# Twitter-Friend-Network-Scrape
Returns users a user is following on Twitter, for a specified amount of levels. Running these functions requires the user to have access to a Twitter API tokens.

Due to API rate limits, the function acquires user_ids. However, the optional function acquires screen_name for each unique user_id acquired in the first function (this can take multiple days). 

For reference, retrieving a follower network based on who @realDonaldTrump follows takes roughly 30-45 minutes, and retrieving their screen names takes several hours. 

Keep in mind that if you do not run the get_screen_name.py, the data in relation_array will not be exported to any useful data format. Make sure to do so yourself if you plan not to run retrieve screen names.
