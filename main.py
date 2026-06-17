import flet as ft
import os
from typing import Type
from models.base import get_registered_models, BaseModel
from components import (
    create_sidebar,
    create_data_table,
    create_recipe_view,
    create_ingredient_card
)
from services.recipe_engine import MurataRecipeEngine
from services.db import DatabaseService

# エンジン初期化
db_url = os.getenv("DATABASE_URL") or ""
engine = MurataRecipeEngine(db_url)

def main(page: ft.Page):
    page.title = "Merchandise Manager"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0

    main_content = ft.Container(expand=True, padding=20)

    def navigate_to(model_cls: Type[BaseModel]):
        main_content.content = None

        if model_cls.__name__ == "Recipe":
            # レシピ一覧の取得
            try:
                with DatabaseService.connection() as conn:
                    with conn.cursor() as cur:
                        cur.execute("SELECT r_id, r_name FROM t_recipes")
                        recipes = [{"r_id": r[0], "r_name": r[1]} for r in cur.fetchall()]
            except Exception as e:
                main_content.content = ft.Text(f"DB接続エラー: {e}", color="red")
                page.update()
                return

            simulator_area = ft.Container(expand=True, padding=10)

            def handle_ingredient_change(item, new_qty_str):
                try:
                    new_qty = float(new_qty_str)
                    print(f"Update {item['m_name']} to {new_qty}")
                except ValueError:
                    pass

            def on_recipe_selected(r_id: int):
                # 再計算ロジック
                try:
                    total_cost, ingredients = engine.calculate_cost_recursive(r_id)
                    cards = [create_ingredient_card(item, handle_ingredient_change) for item in ingredients]

                    simulator_area.content = ft.Column([
                        ft.Text(f"原価合計: {total_cost:,.0f} 円", size=24, color=ft.colors.AMBER),
                        ft.Divider(),
                        ft.ListView(controls=cards, expand=True, spacing=5) # 修正: ListViewを確実に展開
                    ], expand=True)
                    simulator_area.update()
                except Exception as e:
                    simulator_area.content = ft.Text(f"計算エラー: {str(e)}", color="red")
                    simulator_area.update()

            main_content.content = ft.Row([
                create_recipe_view(page, recipes, on_select_recipe=on_recipe_selected),
                simulator_area
            ], expand=True)

        else:
            # 基本テーブル表示
            main_content.content = ft.Column([
                ft.Text(getattr(model_cls, "_label", "画面"), size=30, weight=ft.FontWeight.BOLD),
                ft.Container(content=create_data_table(model_cls), padding=10)
            ], scroll=ft.ScrollMode.AUTO)

        page.update()

    # サイドバー構築
    sidebar = create_sidebar(page, on_nav=navigate_to)
    page.add(ft.Row([sidebar, main_content], expand=True, spacing=0, vertical_alignment=ft.CrossAxisAlignment.START))

    # 初期起動時の表示
    models = get_registered_models()
    if models:
        navigate_to(models[0])

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)
