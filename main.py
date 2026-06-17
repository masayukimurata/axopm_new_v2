import flet as ft
import os
from typing import Type, cast
from models.base import get_registered_models, BaseModel
from components import (
    create_sidebar,
    create_data_table,
    create_recipe_view,
    create_ingredient_card
)
from services.recipe_engine import MurataRecipeEngine
from services.db import DatabaseService

# 型安全のためのキャスト
db_url = os.getenv("DATABASE_URL") or ""
engine = MurataRecipeEngine(db_url)

def main(page: ft.Page):
    page.title = "Merchandise Manager"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0

    main_content = ft.Container(expand=True, padding=20)

    # ページ上部のキャッシュ対策用タイムスタンプ（必要に応じてクエリに使用）
    import time
    timestamp = int(time.time())

    def navigate_to(model_cls: Type[BaseModel]):
        main_content.content = None

        if model_cls.__name__ == "Recipe":
            # レシピ一覧取得
            with DatabaseService.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT r_id, r_name FROM t_recipes")
                    recipes = [{"r_id": r[0], "r_name": r[1]} for r in cur.fetchall()]

            simulator_area = ft.Container(expand=True, padding=10)

            def handle_ingredient_change(item, new_qty_str):
                """材料数量変更時の処理"""
                try:
                    new_qty = float(new_qty_str)
                    print(f"Update {item['m_name']} to {new_qty}")
                    # ここにDB更新ロジックを追記予定
                except ValueError:
                    pass

            def on_recipe_selected(r_id: int):
                """レシピ選択時の詳細表示"""
                total_cost, ingredients = engine.calculate_cost_recursive(r_id)

                # 外部コンポーネントを利用してカードリストを生成
                cards = [create_ingredient_card(item, handle_ingredient_change) for item in ingredients]

                simulator_area.content = ft.Column([
                    ft.Text(f"原価合計: {total_cost:,.0f} 円", size=24, color=ft.colors.AMBER),
                    ft.Divider(),
                    ft.ListView(controls=cards, expand=True)
                ])
                page.update()

            main_content.content = ft.Row([
                create_recipe_view(page, recipes, on_select_recipe=on_recipe_selected),
                simulator_area
            ], expand=True)

        else:
            main_content.content = ft.Column([
                ft.Text(getattr(model_cls, "_label", "画面"), size=30, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=create_data_table(model_cls),
                    border=ft.border.all(1, ft.colors.GREY_800),
                    padding=10
                )
            ], scroll=ft.ScrollMode.AUTO)
        page.update()

    # サイドバーとコンテンツの配置
    sidebar = create_sidebar(page, on_nav=navigate_to)
    page.add(ft.Row([sidebar, main_content], expand=True, spacing=0, vertical_alignment=ft.CrossAxisAlignment.START))

    # 初期表示
    models = get_registered_models()
    if models:
        navigate_to(models[0])

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)
