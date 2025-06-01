import requests
import re
from pathlib import Path

README_PATH = Path("README.md")

COMIC_TAG_START = "<!-- DAILY-COMIC-START -->"
COMIC_TAG_END   = "<!-- DAILY-COMIC-END -->"

def fetch_comic() -> dict | None:
    """Fetch the latest XKCD metadata JSON."""
    url = "https://xkcd.com/info.0.json"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as exc:
        print(f"[error] {exc}")
        return None

def build_comic_section(comic: dict) -> str:
    """Return the HTML we’ll inject into the README, wrapped by markers."""
    return (
        f"{COMIC_TAG_START}\n"
        f'<div align="center">\n'
        f'  <h3>Daily comic!</h3>\n'
        f'  <img src="{comic["img"]}" alt="{comic["title"]}" width="400"/>\n'
        f'  <p><em>{comic["title"]}</em></p>\n'
        f'</div>\n'
        f"{COMIC_TAG_END}\n"
    )

def update_readme(comic: dict) -> None:
    section = build_comic_section(comic)

    readme_text = README_PATH.read_text(encoding="utf-8") if README_PATH.exists() else ""

    pattern = re.compile(
        rf"{re.escape(COMIC_TAG_START)}.*?{re.escape(COMIC_TAG_END)}",
        flags=re.DOTALL,
    )

    if pattern.search(readme_text):
        readme_text = pattern.sub(section, readme_text)
    else:
        readme_text += ("\n" if not readme_text.endswith("\n") else "") + section

    README_PATH.write_text(readme_text, encoding="utf-8")

def main() -> None:
    comic = fetch_comic()
    if comic:
        update_readme(comic)
        print("README updated with the latest comic.")
    else:
        print("Couldn’t fetch today’s comic; README left untouched.")

if __name__ == "__main__":
    main()

