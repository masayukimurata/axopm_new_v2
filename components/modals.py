import flet as ft
from typing import Callable

def create_edit_modal(title: str, on_save: Callable) -> ft.AlertDialog:
    """
    新規・編集操作用モーダルコンポーネント
    """
    return ft.AlertDialog(
        title=ft.Text(f"{title} 編集"),
        content=ft.Column(
            [
                ft.TextField(label="名称"),
                ft.TextField(label="備考"),
            ],
            tight=True,
        ),
        actions=[
            ft.TextButton("キャンセル", on_click=lambda e: e.control.page.close(e.control.page.dialog)),
            ft.ElevatedButton("保存", on_click=on_save),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
