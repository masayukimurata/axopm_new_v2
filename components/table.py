import flet as ft
from services.db import DatabaseService

def create_data_table(model_cls):
    """モデルメタデータに基づきDBからデータを取得し、DataTableを生成する"""
    table_name = getattr(model_cls, "_table_name", None)
    if not table_name:
        return ft.Text("テーブル名が定義されていません")

    try:
        with DatabaseService.connection() as conn:
            with conn.cursor() as cur:
                # 4つのマスターテーブルに絞ったため、このクエリで確実に取得可能
                cur.execute(f"SELECT * FROM {table_name} LIMIT 50")
                rows = cur.fetchall()
                cols = [desc[0] for desc in cur.description]
    except Exception as e:
        return ft.Text(f"データ取得エラー: {str(e)}")

    return ft.DataTable(
        columns=[ft.DataColumn(ft.Text(c)) for c in cols],
        rows=[
            ft.DataRow(
                cells=[ft.DataCell(ft.Text(str(val))) for val in row]
            ) for row in rows
        ],
        border=ft.border.all(1, ft.colors.GREY_700),
        vertical_lines=ft.border.BorderSide(1, ft.colors.GREY_700),
        horizontal_lines=ft.border.BorderSide(1, ft.colors.GREY_700),
    )
