# Twitter-Friend-Network-Scrape
Returns users a user is following on Twitter, for a specified amount of levels. Running these functions requires the user to have access to a Twitter API tokens.

Make sure to remove to add your own API keys as variables, as they are imported from my own text file, otherwise the code will not run.

The starting-user is changed by editing the user_id argument in line 81.

Due to API rate limits, the function acquires user_ids. However, the optional function acquires screen_name for each unique user_id acquired in the first function (this can take multiple days). 

For reference, retrieving a follower network based on who @realDonaldTrump follows takes roughly 30-45 minutes, and retrieving their screen names takes several hours. 

Keep in mind that if you do not run the get_screen_name.py, the data in relation_array will not be exported to any useful data format. Make sure to do so yourself if you plan not to retrieve screen names.

A dataset is added as example, which contains @realDonalTrump's friends and their screen names. 
