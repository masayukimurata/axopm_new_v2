import flet as ft
import os
import threading
import warnings
from typing import Type, Optional
from models.base import get_registered_models, BaseModel
from components import (
    create_sidebar,
    create_data_table,
    create_recipe_view,
    create_ingredient_card
)
from services.recipe_engine import MurataRecipeEngine
from services.db import DatabaseService

warnings.filterwarnings("ignore", category=DeprecationWarning)

engine = MurataRecipeEngine()

def main(page: ft.Page):
    page.title = "Merchandise Manager"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0

    main_content = ft.Container(expand=True, padding=20)
    current_cancel_event: Optional[threading.Event] = None

    # ページ状態を保持する変数
    current_model_cls: Optional[Type[BaseModel]] = None
    current_page: int = 0

    def navigate_to(model_cls: Type[BaseModel], page_num: int = 0):
        nonlocal current_cancel_event, current_model_cls, current_page

        current_model_cls = model_cls
        current_page = page_num

        if current_cancel_event:
            current_cancel_event.set()

        new_event = threading.Event()
        current_cancel_event = new_event

        main_content.content = ft.ProgressRing()
        page.update()

        def background_load():
            try:
                with DatabaseService.connection() as conn:
                    if new_event.is_set(): return

                    if model_cls.__name__ == "Recipe":
                        with conn.cursor() as cur:
                            cur.execute("SELECT r_id, r_name FROM t_recipes")
                            recipes = [{"r_id": r[0], "r_name": r[1]} for r in cur.fetchall()]

                        simulator_area = ft.Container(expand=True, padding=10)

                        def on_recipe_selected(r_id: int):
                            total_cost, ingredients = engine.calculate_cost_recursive(conn, r_id)
                            if new_event.is_set(): return
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
                        # ページ番号とコールバックを渡して再描画を制御
                        content = ft.Column([
                            ft.Text(getattr(model_cls, "_label", "画面"), size=30, weight=ft.FontWeight.BOLD),
                            create_data_table(
                                model_cls,
                                current_page=current_page,
                                on_page_change=lambda p: navigate_to(model_cls, p)
                            )
                        ], scroll=ft.ScrollMode.AUTO)

                if not new_event.is_set():
                    main_content.content = content
                    page.update()
            except Exception as e:
                if not new_event.is_set():
                    main_content.content = ft.Text(f"エラー: {str(e)}", color=ft.colors.RED)
                    page.update()

        threading.Thread(target=background_load, daemon=True).start()

    # サイドバーは常にページ0から開始
    sidebar = create_sidebar(page, on_nav=lambda m: navigate_to(m, 0))
    page.add(ft.Row([sidebar, main_content], expand=True, spacing=0, vertical_alignment=ft.CrossAxisAlignment.START))

    models = get_registered_models()
    if models:
        navigate_to(models[0])

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8502)
