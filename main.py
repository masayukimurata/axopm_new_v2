import flet as ft
import os
import threading
import warnings
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

# 非推奨警告を抑制
warnings.filterwarnings("ignore", category=DeprecationWarning)

# エンジン初期化 (接続注入対応のため引数不要)
engine = MurataRecipeEngine()

def main(page: ft.Page):
    page.title = "Merchandise Manager"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0

    main_content = ft.Container(expand=True, padding=20)

    # --- UI更新をバックグラウンドで行う安定した構成 ---
    def navigate_to(model_cls: Type[BaseModel]):
        main_content.content = ft.ProgressRing()
        page.update()

        def background_load():
            """バックグラウンドで重い処理を行う"""
            try:
                # 共通の接続を使用
                with DatabaseService.connection() as conn:
                    if model_cls.__name__ == "Recipe":
                        with conn.cursor() as cur:
                            cur.execute("SELECT r_id, r_name FROM t_recipes")
                            recipes = [{"r_id": r[0], "r_name": r[1]} for r in cur.fetchall()]

                        simulator_area = ft.Container(expand=True, padding=10)

                        def on_recipe_selected(r_id: int):
                            # 既存の接続(conn)をengineに渡す（これが重要！）
                            total_cost, ingredients = engine.calculate_cost_recursive(conn, r_id)
                            cards = [create_ingredient_card(item, lambda *args: None) for item in ingredients]
                            simulator_area.content = ft.Column([
                                ft.Text(f"原価合計: {total_cost:,.0f} 円", size=24, color=ft.colors.AMBER),
                                ft.Divider(),
                                ft.ListView(controls=cards, expand=True, spacing=5)
                            ], expand=True)
                            simulator_area.update()

                        content = ft.Row([
                            create_recipe_view(page, recipes, on_select_recipe=on_recipe_selected),
                            simulator_area
                        ], expand=True)
                    else:
                        content = ft.Column([
                            ft.Text(getattr(model_cls, "_label", "画面"), size=30, weight=ft.FontWeight.BOLD),
                            ft.Container(content=create_data_table(model_cls), padding=10)
                        ], scroll=ft.ScrollMode.AUTO)

                # メインスレッドへ結果を反映
                main_content.content = content
                page.update()
            except Exception as e:
                main_content.content = ft.Text(f"エラー: {str(e)}", color=ft.colors.RED)
                page.update()

        # スレッド起動
        threading.Thread(target=background_load, daemon=True).start()

    # サイドバー構築
    sidebar = create_sidebar(page, on_nav=navigate_to)
    page.add(ft.Row([sidebar, main_content], expand=True, spacing=0, vertical_alignment=ft.CrossAxisAlignment.START))

    # 初期表示
    models = get_registered_models()
    if models:
        navigate_to(models[0])

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8502)
