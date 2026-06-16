import os
import psycopg2
from psycopg2.pool import SimpleConnectionPool
from dotenv import load_dotenv

# .envの読み込み
load_dotenv()

class DatabaseService:
    _pool = None

    @classmethod
    def get_pool(cls):
        if cls._pool is None:
            cls._pool = SimpleConnectionPool(
                1, 10,
                dsn=os.getenv("DATABASE_URL")
            )
        return cls._pool

    @classmethod
    def get_connection(cls):
        return cls.get_pool().getconn()

    @classmethod
    def release_connection(cls, conn):
        cls.get_pool().putconn(conn)
