import flet as ft
from services.db import DatabaseService
from typing import Any, Callable

def create_data_table(
    model_cls: Any,
    current_page: int = 0,
    on_page_change: Callable[[int], None] = lambda _: None
) -> ft.Control:
    """
    型安全性を確保したページネーション付きテーブル表示コンポーネント。
    on_page_change にデフォルトで何もしないラムダ関数を割り当てることでNoneエラーを回避。
    """
    table_name = getattr(model_cls, "_table_name", None)
    if not table_name:
        return ft.Text("テーブル名が定義されていません", color="red")

    fields = list(model_cls.__annotations__.keys())
    limit = 50
    offset = current_page * limit

    try:
        with DatabaseService.connection() as conn:
            with conn.cursor() as cur:
                # 1. 総件数の取得
                cur.execute(f'SELECT COUNT(*) FROM "{table_name}"')
                total_count = cur.fetchone()[0]
                total_pages = (total_count + limit - 1) // limit

                # 2. データ取得
                cols_query = ", ".join([f'"{f}"' for f in fields])
                query = f'SELECT {cols_query} FROM "{table_name}" ORDER BY 1 LIMIT {limit} OFFSET {offset}'
                cur.execute(query)
                rows = cur.fetchall()
    except Exception as e:
        return ft.Text(f"データ取得エラー: {str(e)}", color="red")

    # ページング操作ボタン
    def change_page(delta: int):
        new_page = max(0, min(current_page + delta, total_pages - 1))
        on_page_change(new_page)

    pagination_ui = ft.Row([
        ft.IconButton(ft.icons.CHEVRON_LEFT, on_click=lambda _: change_page(-1), disabled=(current_page <= 0)),
        ft.Text(f"{current_page + 1} / {max(1, total_pages)}"),
        ft.IconButton(ft.icons.CHEVRON_RIGHT, on_click=lambda _: change_page(1), disabled=(current_page >= total_pages - 1)),
    ], alignment=ft.MainAxisAlignment.CENTER)

    # テーブル構築
    table = ft.DataTable(
        columns=[ft.DataColumn(ft.Text(f)) for f in fields],
        rows=[
            ft.DataRow(
                cells=[ft.DataCell(ft.Text(str(val if val is not None else ""))) for val in row]
            ) for row in rows
        ],
        border=ft.border.all(1, ft.colors.GREY_700),
        vertical_lines=ft.border.BorderSide(1, ft.colors.GREY_700),
        horizontal_lines=ft.border.BorderSide(1, ft.colors.GREY_700),
        heading_row_color=ft.colors.GREY_800,
    )

    return ft.Column([
        ft.Container(content=ft.ListView([table], expand=True), height=500),
        pagination_ui
    ], expand=True)
