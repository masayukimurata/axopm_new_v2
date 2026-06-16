import flet as ft
import time
from models import Recipe, RecipeIngredient, MerchandisePro

def main(page: ft.Page):
    page.title = "App Dashboard"
    page.theme_mode = ft.ThemeMode.LIGHT

    def create_dashboard():
        return ft.GridView(
            controls=[
                ft.Card(content=ft.Container(content=ft.Text("レシピ一覧"), padding=20)),
                ft.Card(content=ft.Container(content=ft.Text("商材マスター"), padding=20))
            ],
            runs_count=2,
            max_extent=300
        )

    page.add(
        ft.Text("ダッシュボード", size=30, weight=ft.FontWeight.BOLD),
        create_dashboard()
    )

    page.update()

# Flet実行時のキャッシュ対策クエリ付与は、外部URLアクセス時に利用
if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)
