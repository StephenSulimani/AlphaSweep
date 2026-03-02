from peewee import IntegrityError, SqliteDatabase
from utils import DiscordClient, Embed
from engines import SerperClient
from models import database_proxy, Job
from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from time import sleep
import random
import os

load_dotenv()

print("📈 Starting AlphaSweep...")

db = SqliteDatabase(os.getenv("DB_NAME"))

database_proxy.initialize(db)

db.connect()
db.create_tables([Job])

print("🚀 Connected to database...")

client = DiscordClient(
    os.getenv("DISCORD_WEBHOOK"),
    os.getenv("DISCORD_WEBHOOK_NAME"),
    os.getenv("DISCORD_WEBHOOK_AVATAR_URL"),
)

print("👾 Connected to Discord...")

serper = SerperClient(os.getenv("SERPER_KEY"))

print("🔗 Connected to Serper...")

queries = [
    '(site:lever.co OR site:greenhouse.io OR site:ashbyhq.com OR site:resolu.com OR site:pinpoint.hq) ("Summer" OR "Intern") (Investment OR Equities OR Quant OR Software OR SWE)'
]


def initial_search():
    print("🔎 Starting initial search")
    for query in queries:
        results = serper.search(query)

        for result in results:
            try:
                Job.create(
                    title=result.title,
                    url=result.url,
                    snippet=result.snippet,
                    date=result.date,
                )
            except IntegrityError:
                pass
            except:
                print("❌ Failed to add job to database")

        all_jobs = Job.select()

        print(f"✅ {len(all_jobs)} jobs stored in the database!")


def job_search():
    """
    Search for new jobs, add them to the database, and send them to Discord
    """
    for query in queries:
        results = serper.search(query)

        for result in results:
            try:
                with db.atomic() as txn:
                    Job.create(
                        title=result.title,
                        url=result.url,
                        snippet=result.snippet,
                        date=result.date,
                    )
                    embed = Embed(title=result.title, description=result.snippet)
                    embed.set_color("#14452F")
                    embed.set_author(client.webhook_name, icon_url=client.avatar_url)
                    embed.add_field("Link", result.url, False)
                    if result.date:
                        embed.add_field(
                            "Date", datetime.strftime(result.date, "%Y-%m-%d")
                        )
                    embed.set_timestamp()

                    try:
                        client.send_embeds([embed])
                        print("✅ Sent webhook")
                        print("==================================")
                        print(result)
                        print("==================================")
                        sleep(random.randint(3, 8))  # Sleep between 3 and 8 seconds
                    except:
                        print("❌ Failed to send webhook")
                        txn.rollback()

            except IntegrityError:
                pass
            except:
                print("❌ Failed to add job to database")
                print("==================================")
                print(result)
                print("==================================")


if __name__ == "__main__":
    initial_search()
    scheduler = BlockingScheduler()
    scheduler.add_job(job_search, "cron", hour="*/2", minute=0, id="job_search")

    print("🚀 Starting scheduler...")

    scheduler.start()
