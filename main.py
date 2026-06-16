import flet as ft
from typing import cast
from models.base import get_registered_models
from components import create_model_card, create_edit_modal
from services import DatabaseService

def main(page: ft.Page):
    page.title = "App Dashboard"
    page.theme_mode = ft.ThemeMode.LIGHT

    # モーダルで保存ボタンが押された時のDB登録ロジック
    def save_to_db(name, memo):
        try:
            with DatabaseService.connection() as conn:
                with conn.cursor() as cur:
                    # 現時点では商材マスター固定。モデルごとの動的解決は次フェーズで実装
                    cur.execute(
                        "INSERT INTO t_merchandise_pro (m_name, note) VALUES (%s, %s)",
                        (name, memo)
                    )
            print(f"DB Saved: {name}, {memo}")

            # 安全にモーダルを閉じる
            if page.dialog:
                alert_dlg = cast(ft.AlertDialog, page.dialog)
                alert_dlg.open = False
                page.update()
        except Exception as ex:
            print(f"DB Error: {ex}")

    # モーダル表示処理
    def open_editor(e, model_label):
        dlg = create_edit_modal(model_label, on_save=save_to_db)
        page.dialog = dlg
        # 型キャストして明示的に制御
        alert_dlg = cast(ft.AlertDialog, dlg)
        alert_dlg.open = True
        page.update()

    # モデル登録状況に応じたカード生成
    grid_items = []
    for model_cls in get_registered_models():
        label = getattr(model_cls, "_label", model_cls.__name__)
        icon = getattr(model_cls, "_icon", "table_chart")

        grid_items.append(
            create_model_card(
                title=label,
                icon=icon,
                # ループ変数キャプチャ問題を回避
                on_click=lambda e, l=label: open_editor(e, l)
            )
        )

    # ダッシュボード描画
    page.add(
        ft.Text("ダッシュボード", size=30, weight=ft.FontWeight.BOLD),
        ft.GridView(
            controls=grid_items,
            runs_count=2,
            max_extent=300,
            spacing=10,
        )
    )
    page.update()

if __name__ == "__main__":
    # URLクエリパラメータでのキャッシュ対策を意識したビュー起動
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)
