import requests
url = "https://xkcd.com/info.0.json"

response = requests.get(url)
data = response.json()
comic_img_url = data["img"]
comic_title = data["title"]
with open("README.md", "r") as file:
    readme_content = file.readlines()

comic_section = f"""
<div align="center">
  <h3>Fumetto del Giorno</h3>
  <img src="{comic_img_url}" alt="{comic_title}" width="400"/>
  <p><em>{comic_title}</em></p>
</div>

"""

with open("README.md", "w") as file:
    file.write(comic_section + "".join(readme_content))
