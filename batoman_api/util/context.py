from aiotinydb import AIOTinyDB
from tinydb import where
from .config import Config
from ..models.auth import User
from async_igdb import IGDBClient


class Context:

    def __init__(self, db: AIOTinyDB, config: Config, igdb_client: IGDBClient):
        self.db = AIOTinyDB
        self.config = config
        self.igdb_client = igdb_client

        if self.config.auth.admin and self.config.auth.admin.active:
            existing = User.query_one(
                where("username") == self.config.auth.admin.username
            )
            if existing:
                if not existing.is_admin:
                    raise RuntimeError("Desired admin user exists and is not an admin.")
            else:
                created = User.create(
                    self.config.auth.admin.username, self.config.auth.admin.password
                )
                created.is_admin = True
                created.save()
