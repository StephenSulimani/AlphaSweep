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
    created_at = DateTimeField(default=datetime.datetime.now, index=True)
