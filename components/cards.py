# components/cards.py
import flet as ft
from typing import Callable, Optional

# --- 1. ナビゲーション用カード (ダッシュボード) ---
def create_model_card(
    title: str,
    icon: str,
    on_click: Optional[Callable[[ft.ControlEvent], None]] = None
) -> ft.Card:
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

# --- 2. 編集・表示用カード (シミュレーター) ---
def create_ingredient_card(item: dict, on_change: Callable):
    """
    材料カード：数量を変更すると on_change を通じて即時再計算へ連携
    """
    return ft.Card(
        content=ft.Container(
            content=ft.Row([
                ft.Text(item['m_name'], width=150, weight=ft.FontWeight.BOLD),
                ft.TextField(
                    value=str(item['quantity']),
                    width=80,
                    on_change=lambda e: on_change(item, e.control.value)
                ),
                ft.Text(f"単価: {item['unit_price']:,.0f}", width=100),
                ft.Text(f"小計: {item['line_cost']:,.0f}", weight=ft.FontWeight.BOLD)
            ]),
            padding=10
        )
    )
