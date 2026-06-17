import flet as ft
from typing import cast, Type
from models.base import get_registered_models, BaseModel
from components import create_model_card, create_edit_modal, create_sidebar
from services import DatabaseService

def main(page: ft.Page):
    page.assets_dir = "assets"  # type: ignore
    page.title = "Merchandise Manager"
    page.theme_mode = ft.ThemeMode.DARK  # 画像に合わせダークモードへ
    page.padding = 0

    # 画面制御用コンテナ
    main_content = ft.Container(content=ft.Text("読み込み中..."), expand=True, padding=20)

    # 運用ルールを表示するコンポーネント
    def create_info_panel(model_cls: Type[BaseModel]):
        doc = getattr(model_cls, "_doc_rule", "ドキュメント未登録")
        return ft.Container(
            content=ft.Column([
                ft.Text("命名規則について", weight=ft.FontWeight.BOLD),
                ft.Text(doc, size=12),
            ]),
            bgcolor=ft.colors.GREY_900,
            padding=15,
            border_radius=10,
            margin=ft.margin.only(bottom=20)
        )

    # 画面遷移ロジック
    def navigate_to(model_cls: Type[BaseModel]):
        main_content.content = ft.Column([
            ft.Text(getattr(model_cls, "_label", "画面"), size=30, weight=ft.FontWeight.BOLD),
            create_info_panel(model_cls),
            # ここにモデルごとの一覧/操作画面が動的に入る
        ])
        page.update()

    # サイドバー作成
    sidebar = create_sidebar(page, on_nav=navigate_to)

    # 初期表示（ダッシュボード）
    navigate_to(get_registered_models()[0])

    # メインレイアウト
    page.add(
        ft.Row(
            [
                sidebar,
                main_content
            ],
            expand=True,
            spacing=0
        )
    )

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)
