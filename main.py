import flet as ft
from typing import cast, Type
from models.base import get_registered_models, BaseModel
from components import create_model_card, create_edit_modal
from services import DatabaseService

def main(page: ft.Page):
    # assetsディレクトリの指定（型チェックを回避）
    page.assets_dir = "assets"  # type: ignore
    page.title = "App Dashboard"
    page.theme_mode = ft.ThemeMode.LIGHT

    # 【汎用DB登録エンジン】
    # モデルクラスを引数として受け取り、メタデータから自動的にテーブルを決定
    def save_to_db(name: str, memo: str, model_cls: Type[BaseModel]):
        table_name = getattr(model_cls, "_table_name", "t_merchandise_pro")
        try:
            with DatabaseService.connection() as conn:
                with conn.cursor() as cur:
                    # モデル定義に基づいた汎用INSERT
                    cur.execute(
                        f"INSERT INTO {table_name} (m_name, note) VALUES (%s, %s)",
                        (name, memo)
                    )
            print(f"DB Saved to {table_name}: {name}")

            # 安全にモーダルを閉じる
            if page.dialog:
                alert_dlg = cast(ft.AlertDialog, page.dialog)
                alert_dlg.open = False
                page.update()
        except Exception as ex:
            print(f"DB Error: {ex}")

    # モーダル表示処理
    def open_editor(e, model_cls: Type[BaseModel]):
        # model_cls を渡して保存時に利用可能にする
        label = getattr(model_cls, "_label", "データ")
        dlg = create_edit_modal(label, on_save=lambda n, m: save_to_db(n, m, model_cls))
        page.dialog = dlg

        # 型キャストして明示的に制御
        alert_dlg = cast(ft.AlertDialog, dlg)
        alert_dlg.open = True
        page.update()

    # レジストリから動的にカードを生成
    grid_items = []
    for model_cls in get_registered_models():
        label = getattr(model_cls, "_label", model_cls.__name__)
        icon = getattr(model_cls, "_icon", "table_chart")

        grid_items.append(
            create_model_card(
                title=label,
                icon=icon,
                # ループ変数キャプチャ問題を回避し、クラス自体を渡す
                on_click=lambda e, m=model_cls: open_editor(e, m)
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
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)
