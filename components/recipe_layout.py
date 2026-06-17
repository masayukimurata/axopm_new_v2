# components/recipe_layout.py
import flet as ft

def create_recipe_view(page: ft.Page, recipes: list, on_select_recipe):
    """レシピ画面：左側パネルのみを構築"""

    def create_recipe_card(recipe):
        return ft.Card(
            content=ft.Container(
                content=ft.Text(recipe['r_name'], weight=ft.FontWeight.BOLD),
                padding=10,
                on_click=lambda _: on_select_recipe(recipe['r_id'])
            )
        )

    return ft.Container(
        content=ft.Column([
            ft.TextField(hint_text="レシピ名で検索...", prefix_icon=ft.icons.SEARCH),
            ft.ListView(
                controls=[create_recipe_card(r) for r in recipes],
                expand=True,
                spacing=10
            )
        ]),
        width=350,
        padding=10
    )
