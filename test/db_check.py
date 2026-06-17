# db_check.py (デバッグ用スクリプト)
from services import DatabaseService
from models.base import get_registered_models

def verify_db_schema():
    print("--- DB 接続確認開始 ---")
    try:
        with DatabaseService.connection() as conn:
            with conn.cursor() as cur:
                # 1. 接続確認
                cur.execute("SELECT current_schema();")
                schema = cur.fetchone()[0]
                print(f"現在接続中スキーマ: {schema}")

                # 2. モデル定義されたテーブルが存在するか確認
                for model_cls in get_registered_models():
                    table_name = getattr(model_cls, "_table_name", "unknown")
                    cur.execute("""
                        SELECT EXISTS (
                            SELECT FROM information_schema.tables
                            WHERE table_schema = %s
                            AND table_name = %s
                        );
                    """, (schema, table_name))
                    exists = cur.fetchone()[0]
                    status = "✅ OK" if exists else "❌ NOT FOUND"
                    print(f"テーブルチェック [{table_name}]: {status}")
    except Exception as e:
        print(f"接続エラー: {e}")

if __name__ == "__main__":
    verify_db_schema()
