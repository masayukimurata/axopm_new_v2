import flet as ft
from services.db import DatabaseService
from typing import Any

def create_data_table(model_cls: Any) -> ft.Control:
    """
    モデルメタデータに基づきDBからデータを取得し、DataTableを生成する。
    日本語カラム名、テーブル名に対応するためダブルクォーテーションで保護する。
    """
    table_name = getattr(model_cls, "_table_name", None)
    if not table_name:
        return ft.Text("テーブル名が定義されていません", color="red")

    # モデルクラスからフィールド名を取得（順序を維持）
    fields = list(model_cls.__annotations__.keys())

    try:
        with DatabaseService.connection() as conn:
            with conn.cursor() as cur:
                # 識別子をダブルクォーテーションで囲んで安全にクエリ
                cols_query = ", ".join([f'"{f}"' for f in fields])
                query = f'SELECT {cols_query} FROM "{table_name}" LIMIT 50'
                cur.execute(query)
                rows = cur.fetchall()
    except Exception as e:
        return ft.Text(f"データ取得エラー: {str(e)}", color="red")

    # データ表示用テーブルの構築
    return ft.DataTable(
        columns=[ft.DataColumn(ft.Text(f)) for f in fields],
        rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(val if val is not None else "")))
                    for val in row
                ]
            ) for row in rows
        ],
        border=ft.border.all(1, ft.colors.GREY_700),
        vertical_lines=ft.border.BorderSide(1, ft.colors.GREY_700),
        horizontal_lines=ft.border.BorderSide(1, ft.colors.GREY_700),
        heading_row_color=ft.colors.GREY_800,
    )
