import requests
from bs4 import BeautifulSoup
from collections import deque

# Define the URL of the domain to crawl
url = "https://example.com"

# Define the maximum depth to crawl
max_depth = 5

# Create a deque to store links and their corresponding depth
link_queue = deque([(url, 1)])

# Create a set to store already visited links
visited_links = set()

# Create an empty string to store the text of all pages
all_text = ""

# Loop through each link in the queue
while link_queue:
    # Get the next link and its depth
    link, depth = link_queue.popleft()
    # Check if the link has already been visited
    if link in visited_links:
        continue
    # Send a GET request to the link
    response = requests.get(link)
    # Use BeautifulSoup to parse the HTML content of the response
    soup = BeautifulSoup(response.content, "html.parser")
    # Add the text of the page to the string
    all_text += soup.get_text().replace("\n", "")
    # Add a space after each word to make the output more readable
    all_text += " "
    # Add the link to the set of visited links
    visited_links.add(link)
    # Check if the current depth is less than the maximum depth
    if depth < max_depth:
        # Find all links on the page
        links = soup.find_all("a")
        # Loop through each link and add it to the queue
        for link in links:
            href = link.get("href")
            if href is not None and href.startswith("/"):
                # Construct the absolute URL
                href = url + href
            # Add the link and its depth to the queue
            link_queue.append((href, depth + 1))

    # Output status every 10 links
    if len(visited_links) % 10 == 0:
        print(f"Crawled {len(visited_links)} links")

# Write the output text to a file
with open("output.txt", "w") as f:
    f.write(all_text)

print("Done!")
