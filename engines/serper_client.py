import requests
from datetime import datetime, timedelta
import re


def _parse_relative_time(text):
    """
    Parse relative time to datetime

    Args:
        text (): Relative date string (e.g. "1 day ago"))

    Returns:
        datetime: Datetime

    Raises:
        ValueError:
    """
    match = re.match(r"(\d+)\s+(day|days|hour|hours|minute|minutes)\s+ago", text)
    if not match:
        raise ValueError("Invalid format")

    value = int(match.group(1))
    unit = match.group(2)

    now = datetime.now()

    if "day" in unit:
        return now - timedelta(days=value)
    elif "hour" in unit:
        return now - timedelta(hours=value)
    elif "minute" in unit:
        return now - timedelta(minutes=value)


class SearchResult:
    """
    Serper search result

    Attributes:
        title: Title of search result
        link: URL of search result
        snippet: Snippet of search result
        date: Date of search result
    """

    def __init__(self, title, url, snippet, date):
        self.title = title
        self.url = url
        self.snippet = snippet
        self.date = None
        try:
            self.date = _parse_relative_time(date)
        except:
            pass

    def __str__(self):
        return f"{self.title}\n{self.url}\n{self.snippet}\n{self.date}"


class SerperClient:
    """
    Client for Seper SERP API (serper.dev)

    Attributes:
        api_key: Serper API Key
    """

    def __init__(self, api_key):
        self.api_key = api_key

        self.session = requests.session()
        self.session.headers.update(
            {"x-api-key": self.api_key, "content-type": "application/json"}
        )

    def search(self, query):
        payload = {"q": query, "autocorrect": False, "tbs": "qdr:w"}

        res = self.session.post("https://google.serper.dev/search", json=payload)

        if res.status_code != 200:
            raise Exception(f"Failed to search: {res.status_code}")

        results = res.json()["organic"]

        return [
            SearchResult(
                result["title"], result["link"], result["snippet"], result["date"]
            )
            for result in results
        ]
