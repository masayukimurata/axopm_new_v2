import flet as ft
from typing import Type, cast
from models.base import get_registered_models, BaseModel
from components import create_sidebar, create_data_table, create_recipe_view
from services import DatabaseService

def main(page: ft.Page):
    page.title = "Merchandise Manager"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0

    main_content = ft.Container(expand=True, padding=20)

    # ページに要素を追加してから開始
    sidebar = create_sidebar(page, on_nav=lambda model: navigate_to(model))
    page.add(ft.Row([sidebar, main_content], expand=True, spacing=0, vertical_alignment=ft.CrossAxisAlignment.START))

    def navigate_to(model_cls: Type[BaseModel]):
        # コンテンツの初期化（cleanではなくcontent=Noneを使用）
        main_content.content = None

        if model_cls.__name__ == "Recipe":
            with DatabaseService.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT r_id, r_name FROM t_recipes")
                    rows = cur.fetchall()
                    recipes = [{"r_id": r[0], "r_name": r[1]} for r in rows]

            simulator_container = ft.Container(
                content=ft.Text("左のレシピを選択するとシミュレーターが起動します", color=ft.colors.GREY_600),
                expand=True,
                border=ft.border.all(1, ft.colors.GREY_800),
                border_radius=10,
                margin=10,
                padding=10
            )

            def on_recipe_selected(r_id: int):
                simulator_container.content = ft.Column([
                    ft.Text(f"レシピID: {r_id} の詳細シミュレーター", size=20, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    ft.Text("※材料結合クエリを実装予定", color=ft.colors.AMBER)
                ])
                page.update()

            main_content.content = ft.Row([
                create_recipe_view(page, recipes, on_select_recipe=on_recipe_selected),
                simulator_container
            ], expand=True)

        else:
            main_content.content = ft.Column([
                ft.Text(getattr(model_cls, "_label", "画面"), size=30, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=create_data_table(model_cls),
                    border=ft.border.all(1, ft.colors.GREY_800),
                    border_radius=8,
                    padding=10
                )
            ], scroll=ft.ScrollMode.AUTO)

        page.update()

    # 初期表示
    models = get_registered_models()
    if models:
        navigate_to(models[0])

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)
