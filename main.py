import flet as ft
from typing import cast, Type
from models.base import get_registered_models, BaseModel
from components import create_sidebar, create_data_table  # 追加
from services import DatabaseService

def main(page: ft.Page):
    page.assets_dir = "assets" # type: ignore
    page.title = "Merchandise Manager"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0

    # 画面制御用コンテナ
    main_content = ft.Container(content=ft.Text("読み込み中..."), expand=True, padding=20)

    # 運用ルールを表示するコンポーネント
    def create_info_panel(model_cls: Type[BaseModel]):
        doc = getattr(model_cls, "_doc_rule", "ドキュメント未登録")
        return ft.Container(
            content=ft.Column([
                ft.Text("運用ルール", weight=ft.FontWeight.BOLD),
                ft.Text(doc, size=12),
            ]),
            bgcolor=ft.colors.GREY_900,
            padding=15,
            border_radius=10,
            margin=ft.margin.only(bottom=20)
        )

    # 画面遷移ロジック
    def navigate_to(model_cls: Type[BaseModel]):
        # コンテンツを更新
        main_content.content = ft.Column([
            ft.Text(getattr(model_cls, "_label", "画面"), size=30, weight=ft.FontWeight.BOLD),
            create_info_panel(model_cls),
            # 自動生成されたデータテーブルを配置
            ft.Container(
                content=create_data_table(model_cls),
                border=ft.border.all(1, ft.colors.GREY_800),
                border_radius=8,
                padding=10
            )
        ], scroll=ft.ScrollMode.AUTO) # 長い表に対応するためスクロール有効化
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
            spacing=0,
            vertical_alignment=ft.CrossAxisAlignment.START
        )
    )

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)
