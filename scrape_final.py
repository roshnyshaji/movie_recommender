import pandas as pd
import re
import asyncio
from twscrape import API, gather
import csv


def preprocess_movie_titles(movie_titles):
    preprocessed_titles = []
    for title in movie_titles:
        # Remove numbers inside parentheses
        cleaned_title = re.sub(r"\(\d+\)", "", title)
        # Remove special characters, punctuation, and spaces
        cleaned_title = re.sub(r"[^\w\s]", "", cleaned_title)
        # Convert to lowercase and append preprocessed title to the list
        preprocessed_titles.append(cleaned_title.lower())
    return preprocessed_titles


async def fetch_tweets(movie_tags, accounts):
    api = API()

    # for account in accounts:
    #     await api.pool.add_account(*account)
    # await api.pool.login_all()

    movie_tags = movie_tags[1660:]  # not all at once

    movie_tweets = {}

    for movie_tag in movie_tags:
        print(f"Fetching tweets for: {movie_tag}")

        # Exclude unwanted content
        unwanted_terms = [
            "-filter:links",
            "-filter:media",
            "-vote",
            "-game",
            "-trailer",
            "-promo",
            "-stream",
            "-series",
        ]

        # Include movie specific keyword
        include_terms = f"(#{movie_tag} movie) OR (#{movie_tag} film)"
        # Construct the query using f-string
        tag = f"{include_terms} {' '.join(unwanted_terms)} lang:en"
        tweets = await gather(api.search(tag, limit=20))
        movie_tweets[movie_tag] = [tweet.rawContent for tweet in tweets]

        # await asyncio.sleep(5)

    return movie_tweets


async def main():
    # Load movie data
    u_item = pd.read_csv(
        "u.item",
        sep="|",
        encoding="ISO-8859-1",
        header=None,
        names=["movie_id", "title", "release_date", "video_release_date", "IMDb_URL"]
        + list(range(19)),
    )
    preprocessed_titles = preprocess_movie_titles(u_item["title"])
    movie_tags = ["#" + title.replace(" ", "") for title in preprocessed_titles]

    # Twitter account credentials (add more as needed)
    accounts = [
        ("###", "###", "###", "###"),
        # Can add more accounts here for distributing load
    ]

    # Fetch tweets for movie tags
    movie_tweets = await fetch_tweets(movie_tags, accounts)

    # Dump collected Twitter data into a CSV file
    with open("movie_tweets20.csv", "a", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)

        # Write header
        # writer.writerow(["Movie_hashtag", "Tweet"])

        # Write rows
        for movie, tweets in movie_tweets.items():
            for tweet in tweets:
                writer.writerow([movie, tweet])

    print("Completed!")


if __name__ == "__main__":
    asyncio.run(main())
