import sys
import os
from pathlib import Path

# プロジェクトルート（axiom-new_v2）を検索パスに追加
sys.path.append(str(Path(__file__).resolve().parent.parent))

# この後からインポートが可能になる
from services.db import DatabaseService
from dotenv import load_dotenv

load_dotenv()

print(f"DEBUG: URL is {os.getenv('DATABASE_URL')}")

try:
    with DatabaseService.connection() as conn:
        print("接続成功！")
except Exception as e:
    print(f"接続失敗: {e}")
