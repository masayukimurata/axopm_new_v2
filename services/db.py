import os
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv
from contextlib import contextmanager

load_dotenv()

class DatabaseService:
    _pool = None

    @classmethod
    def get_pool(cls) -> pool.ThreadedConnectionPool:
        """接続プールを初期化して返す"""
        if cls._pool is None:
            # DATABASE_URLの確認
            dsn = os.getenv("DATABASE_URL")
            if not dsn:
                raise ValueError("環境変数 DATABASE_URL が設定されていません。")

            # 最大接続数を5に制限し、接続枯渇を防ぐ
            cls._pool = pool.ThreadedConnectionPool(
                1, 5,
                dsn=dsn
            )
        return cls._pool

    @classmethod
    @contextmanager
    def connection(cls):
        """with句で確実に接続を取得し、処理後にプールへ返却する"""
        db_pool = cls.get_pool()
        conn = db_pool.getconn()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            # 正常時も例外時も必ず接続をプールに戻す
            db_pool.putconn(conn)
