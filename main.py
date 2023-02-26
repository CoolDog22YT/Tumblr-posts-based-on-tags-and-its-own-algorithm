import os
import time
import pytumblr
import pandas as pd

# Get the keys and tokens from Replit secrets
consumer_key = os.environ['consumer key']
consumer_secret = os.environ['cosumer secret']
oauth_token = os.environ['oauth token']
oauth_secret = os.environ['token secret']

# Authenticate with the Tumblr API using your API key
client = pytumblr.TumblrRestClient(
    consumer_key,
    consumer_secret,
    oauth_token,
    oauth_secret,
)

# Define the tags to search for
tags = ['random', 'idk', 'funny', 'reblog', 'fox', 'art']

# Post to this side blog
side_blog_name = 'affinityrae-coding'

# Keep track of posted URLs to avoid duplicates
posted_urls = []

# Specify the interval in seconds to wait between checks
interval = 600  # check once every 10 minutes

# Get the last 20 posts from the side blog to avoid reposting them
previous_posts = client.posts(side_blog_name, limit=20)

while True:
    start_time = time.time() # Start tracking time

    # Send an API request to retrieve the most recent posts with the specified tags
    posts = []
    for tag in tags:
        posts += client.tagged(tag)

    # Extract the tags and post URLs of the most recent posts
    data = []
    for post in posts:
        if isinstance(post, dict):  # make sure post is a dictionary
            post_tags = post.get('tags', [])
            if any(tag in post_tags for tag in tags):  # make sure at least one of the specified tags is present
                tags = ', '.join(post_tags)
                url = post['post_url']
                if url in posted_urls or url in [p['post_url'] for p in previous_posts['posts']]:
                    continue  # skip already posted URLs and previous posts from the side blog
                data.append({'tags': tags, 'url': url})

    # Convert the extracted data to a pandas DataFrame
    df = pd.DataFrame(data)

    # Post the data to the specified side blog
    for _, row in df.iterrows():
        tags = row['tags']
        url = row['url']
        body = "This is an experiment using Tumblr's API. Original post: " + url
        client.create_text(side_blog_name, tags=tags, body=body)
        posted_urls.append(url)
        print(f"Posted {url} to {side_blog_name}!")

    # Calculate the time elapsed since the start of the loop
    elapsed_time = time.time() - start_time

    # If the elapsed time is less than the interval, wait for the remaining time
    if elapsed_time < interval:
        time.sleep(interval - elapsed_time)
