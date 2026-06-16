import flet as ft
from typing import Callable
from .base_input import BaseTextField

def create_edit_modal(title: str, on_save: Callable) -> ft.AlertDialog:
    """
    新規・編集操作用モーダルコンポーネント
    保存ボタン押下時に、入力された各フィールドの値を on_save へ渡す
    """
    # 共通デザインの入力欄を使用
    name_field = BaseTextField(label="名称")
    memo_field = BaseTextField(label="備考")

    return ft.AlertDialog(
        title=ft.Text(f"{title} 編集"),
        content=ft.Column(
            [
                name_field,
                memo_field,
            ],
            tight=True,
        ),
        actions=[
            ft.TextButton(
                "キャンセル",
                on_click=lambda e: e.control.page.close(e.control.page.dialog)
            ),
            ft.ElevatedButton(
                "保存",
                # lambda で値を明示的に渡すことで、コールバック先で値を利用可能にする
                on_click=lambda e: on_save(name_field.value, memo_field.value)
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
