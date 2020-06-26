# Twitter-Friend-Network-Scrape
Returns users a user is following on Twitter, for a specified amount of levels. Running these functions requires the user to have access to a Twitter API tokens.

Due to API rate limits, the function acquires user_ids. However, the optional function acquires screen_name for each unique user_id acquired in the first function (this can take multiple days). 

For reference, retrieving a follower network based on who @realDonaldTrump follows takes roughly 30-45 minutes, and retrieving their screen names takes several hours. 
