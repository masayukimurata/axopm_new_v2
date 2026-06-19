# components/cards.py
import flet as ft
from typing import Callable, Optional, Any
from decimal import Decimal

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
def create_ingredient_card(item: dict[str, Any], on_change: Callable[[dict, str], None]) -> ft.Card:
    """
    型安全性を確保した材料カード。
    DBの数値型変更に対応し、UIは文字列として値を保持しつつ、
    コールバックで適切な型変換を行う設計。
    """
    # 辞書の取得に安全策を講じる
    m_name = str(item.get('m_name', '不明'))
    quantity = item.get('quantity', 0)
    unit_price = item.get('unit_price', 0)
    line_cost = item.get('line_cost', 0)

    return ft.Card(
        content=ft.Container(
            content=ft.Row([
                ft.Text(m_name, width=150, weight=ft.FontWeight.BOLD),
                ft.TextField(
                    value=str(quantity),
                    width=80,
                    # 入力値の変化をそのままコールバックへ渡す（バリデーションはロジック側で処理）
                    on_change=lambda e: on_change(item, e.control.value)
                ),
                ft.Text(f"単価: {unit_price:,.0f}", width=100),
                ft.Text(f"小計: {line_cost:,.0f}", weight=ft.FontWeight.BOLD)
            ]),
            padding=10
        )
    )
