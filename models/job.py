import datetime
from peewee import DatabaseProxy, DateTimeField, Model, TextField

database_proxy = DatabaseProxy()


class BaseModel(Model):
    class Meta:
        database = database_proxy


class Job(BaseModel):
    title = TextField()
    url = TextField(unique=True)
    snippet = TextField()
    date = DateTimeField(default=datetime.datetime.now, index=True)
    image_url = TextField(null=True)
    created_at = DateTimeField(default=datetime.datetime.now, index=True)
    def __str__(self):
        return f"{self.title}\n{self.url}\n{self.snippet}\n{self.date}"

