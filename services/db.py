import os
import psycopg2
from psycopg2.pool import SimpleConnectionPool
from dotenv import load_dotenv
from contextlib import contextmanager

load_dotenv()

class DatabaseService:
    _pool = None

    @classmethod
    def get_pool(cls):
        if cls._pool is None:
            # DATABASE_URLは環境変数から取得（neon等の接続文字列を想定）
            cls._pool = SimpleConnectionPool(
                1, 10,
                dsn=os.getenv("DATABASE_URL")
            )
        return cls._pool

    @contextmanager
    @classmethod
    def connection(cls):
        """with句で接続を安全に取得・解放する"""
        pool = cls.get_pool()
        conn = pool.getconn()
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            pool.putconn(conn)
