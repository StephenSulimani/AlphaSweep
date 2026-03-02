import requests

from datetime import datetime, timezone


class Embed:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def set_color(self, color: str):
        self.__dict__["color"] = int(color.replace("#", ""), 16)

    def set_author(self, name, url=None, icon_url=None):
        self.__dict__["author"] = {
            "name": name,
        }
        if url:
            self.__dict__["author"]["url"] = url
        if icon_url:
            self.__dict__["author"]["icon_url"] = icon_url

    def set_footer(self, text, icon_url=None):
        self.__dict__["footer"] = {
            "text": text,
        }
        if icon_url:
            self.__dict__["footer"]["icon_url"] = icon_url

    def add_field(self, name, value, inline=False):
        if not self.__dict__.get("fields"):
            self.__dict__["fields"] = []
        self.__dict__["fields"].append({"name": name, "value": value, "inline": inline})

    def set_timestamp(self):
        self.__dict__["timestamp"] = datetime.now(timezone.utc).isoformat()

    def to_dict(self):
        return self.__dict__


class DiscordClient:
    """
    Discord Webhook Client

    Attributes:
        webhook_url: Discord Webhook URL
        webhook_name: Discord Webhook Name
        avatar_url: Discord Webhook Avatar
    """

    def __init__(self, webhook_url, webhook_name="AlphaSweep", avatar_url=""):
        self.webhook_url = webhook_url
        self.webhook_name = webhook_name
        self.avatar_url = avatar_url
        self.session = requests.session()

        self.base_body = {
            "username": self.webhook_name,
        }

        if avatar_url:
            self.base_body["avatar_url"] = self.avatar_url

    def send_embeds(self, embeds: list[Embed], content=None):
        body = {
            **self.base_body,
            "embeds": [embed.to_dict() for embed in embeds],
        }

        if content:
            body["content"] = content

        res = self.session.post(self.webhook_url, json=body)

        if res.status_code != 204:
            raise Exception(f"Failed to send webhook: {res.status_code}\n{res.text}")
