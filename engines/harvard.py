from models.job import Job
from .engine import Engine
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime


class HarvardClient(Engine):
    def search(self):
        url = "https://careerservices.fas.harvard.edu/jobs/?ctag%5B%5D=short-term-project&ctag%5B%5D=internship&sort=date"
        res = requests.get(url)

        if res.status_code != 200:
            raise Exception(f"Failed to search: {res.status_code}")

        soup = BeautifulSoup(res.text, "html.parser")
        featured_jobs = soup.find("div", {"id": "featured-jobs-list"})

        if not featured_jobs:
            raise Exception("No featured jobs found")

        jobs = featured_jobs.find_all("div")

        if not jobs:
            raise Exception("No jobs found")

        job_list = []

        for job in jobs:
            try:
                title = job.find("h3", class_="entry-title").text.strip()
                url = job.find("h3", class_="entry-title").find("a").get("href")
                snippet = job.find("div", class_="entry-content").text.strip()
                recruitment_date = job.find("div", class_="entry-meta-item").text.strip()
                image_url = job.find("div", class_="company_logo")

                if image_url:
                    style = image_url.get("style")
                    image_url = re.search(r"url\((.*?)\)", style).group(1)

                date = re.search(r'Recruitment began on (.*)', recruitment_date).group(1)

                date = datetime.strptime(date, '%B %d, %Y')

                job_list.append(Job(title=title, url=url, snippet=snippet, date=date, image_url=image_url))
            except:
                pass
        return job_list








