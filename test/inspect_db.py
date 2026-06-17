import sys
import os
from pathlib import Path

# プロジェクトルート（axiom-new_v2）をパスに追加
sys.path.append(str(Path(__file__).resolve().parent.parent))

# これでインポート可能になる
from services.db import DatabaseService

def inspect_database():
    # ... (前回のスクリプトと同じ内容) ...
    query = """
    SELECT table_name, column_name
    FROM information_schema.columns
    WHERE table_schema = 'public'
    ORDER BY table_name, ordinal_position;
    """

    with DatabaseService.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            results = cur.fetchall()

    schema = {}
    for table, column in results:
        if table not in schema: schema[table] = []
        schema[table].append(column)

    for table, columns in schema.items():
        print(f"Table: {table}")
        print(f"  Columns: {', '.join(columns)}")
        print("-" * 20)

if __name__ == "__main__":
    inspect_database()
