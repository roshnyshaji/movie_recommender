# import pandas as pd
# import re
# import asyncio
# from twscrape import API, gather
# import csv
# from processing_tweets import corrected_tags  # Corrected tags that had 'the' at the end


# async def fetch_tweets(movie_tags, accounts):
#     api = API()

#     # for account in accounts:
#     #     await api.pool.add_account(*account)
#     # await api.pool.login_all()

#     movie_tags = movie_tags[280:]

#     movie_tweets = {}

#     for movie_tag in movie_tags:
#         print(f"Fetching tweets for: {movie_tag}")

#         # Exclude unwanted content
#         unwanted_terms = [
#             "-filter:links",
#             "-filter:media",
#             "-vote",
#             "-game",
#             "-trailer",
#             "-promo",
#             "-stream",
#             "-series",
#         ]

#         # Include movie specific keyword
#         include_terms = f"(#{movie_tag} movie) OR (#{movie_tag} film)"
#         # Construct the query using f-string
#         tag = f"{include_terms} {' '.join(unwanted_terms)} lang:en"
#         tweets = await gather(api.search(tag, limit=20))
#         movie_tweets[movie_tag] = [tweet.rawContent for tweet in tweets]

#         # await asyncio.sleep(5)

#     return movie_tweets


# async def main():

#     # Twitter account credentials
#     accounts = [
#         ("###", "###", "###", "###"),
#     ]

#     # Fetch tweets for movie tags
#     movie_tweets = await fetch_tweets(corrected_tags, accounts) 

#     # Dump collected Twitter data into a CSV file
#     with open("movie_tweets20.csv", "a", newline="", encoding="utf-8") as csv_file:
#         writer = csv.writer(csv_file)

#         # Write header
#         # writer.writerow(["Movie_hashtag", "Tweet"])

#         # Write rows
#         for movie, tweets in movie_tweets.items():
#             for tweet in tweets:
#                 writer.writerow([movie, tweet])

#     print("Completed!")


# if __name__ == "__main__":
#     asyncio.run(main())