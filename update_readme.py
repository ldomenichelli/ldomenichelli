import requests

def fetch_comic():
    url = "https://xkcd.com/info.0.json"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        return response.json()  # Return the JSON response if successful
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Print HTTP errors
    except requests.exceptions.RequestException as req_err:
        print(f"Request exception: {req_err}")  # Print any request exceptions
    except Exception as e:
        print(f"An error occurred: {e}")  # Print any other exceptions
    return None  # Return None if there was an error

def update_readme(comic):
    comic_img_url = comic["img"]
    comic_title = comic["title"]
    
    # Read existing README content
    with open("README.md", "r") as file:
        readme_content = file.readlines()

    comic_section = f"""
<div align="center">
  <h3>Daily comic!</h3>
  <img src="{comic_img_url}" alt="{comic_title}" width="400"/>
  <p><em>{comic_title}</em></p>
</div>
"""

    with open("README.md", "w") as file:
        file.write( "".join(readme_content + comic_section +))

def main():
    comic = fetch_comic()  # Fetch the comic
    if comic:  # If fetching was successful
        update_readme(comic)  # Update the README file
        print("README updated with the daily comic.")
    else:
        print("Failed to fetch the comic. README was not updated.")

if __name__ == "__main__":
    main()
