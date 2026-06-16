import flet as ft
from typing import Callable, Optional

def create_model_card(
    title: str,
    icon: str,
    on_click: Optional[Callable[[ft.ControlEvent], None]] = None
) -> ft.Card:
    """
    ダッシュボード用のカード型デザインコンポーネント
    """
    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Icon(name=icon, size=30),
                    ft.Text(title, weight=ft.FontWeight.BOLD),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=20,
            on_click=on_click,
        ),
        elevation=2,
    )
