from __future__ import annotations

import html
import json
import re
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

README = Path("README.md")
START = "<!-- DAILY-COMIC-START -->"
END = "<!-- DAILY-COMIC-END -->"
TIMEZONE = "Europe/Rome"


def fetch_json(url: str) -> dict:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "lucia-profile-readme-xkcd-updater/1.0"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def pick_comic_number(latest_num: int, day_ordinal: int) -> int:
    span = max(latest_num - 1, 1)
    num = (day_ordinal % span) + 1
    if num >= 404:
        num += 1
    return min(num, latest_num)


def render_block(comic: dict) -> str:
    title = html.escape(comic.get("safe_title") or comic["title"])
    alt = html.escape(comic["alt"])
    img = html.escape(comic["img"])
    num = comic["num"]
    published = f"{comic['year']}-{int(comic['month']):02d}-{int(comic['day']):02d}"

    return f"""{START}
<div align="center">
  <h3>📅 XKCD of the day</h3>
  <a href="https://xkcd.com/{num}/">
    <img src="{img}" alt="{title}" width="520" />
  </a>
  <p><strong>{title}</strong> · xkcd #{num} · {published}</p>
  <p><sub>{alt}</sub></p>
</div>
{END}"""


def main() -> None:
    text = README.read_text(encoding="utf-8")

    latest = fetch_json("https://xkcd.com/info.0.json")
    today = datetime.now(ZoneInfo(TIMEZONE)).date()
    num = pick_comic_number(int(latest["num"]), today.toordinal())
    comic = fetch_json(f"https://xkcd.com/{num}/info.0.json")

    pattern = re.compile(rf"{re.escape(START)}.*?{re.escape(END)}", re.DOTALL)
    if not pattern.search(text):
        raise RuntimeError("Could not find DAILY-COMIC markers in README.md")

    updated = pattern.sub(render_block(comic), text, count=1)

    if not updated.endswith("\n"):
        updated += "\n"

    README.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    main()
