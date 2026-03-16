import requests
from datetime import datetime, timedelta
from .engine import Engine
from models import Job
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


class SerperClient(Engine):
    """
    Client for Seper SERP API (serper.dev)

    Attributes:
        api_key: Serper API Key
    """

    def __init__(self, api_key: str, queries: list[str]):
        self.api_key = api_key
        self.queries = queries

        self.session = requests.session()
        self.session.headers.update(
            {"x-api-key": self.api_key, "content-type": "application/json"}
        )

    def search(self) -> list[Job]:
        jobs = []
        for query in self.queries:
            payload = {"q": query, "autocorrect": False, "tbs": "qdr:d"}

            res = self.session.post("https://google.serper.dev/search", json=payload)

            if res.status_code != 200:
                raise Exception(f"Failed to search: {res.status_code}")

            results = res.json()["organic"]

            results = [
                SearchResult(
                    result["title"], result["link"], result["snippet"], result["date"]
                )
                for result in results
            ]

            jobs.extend([Job(title=result.title, url=result.url, snippet=result.snippet, date=result.date) for result in results])
        return jobs
