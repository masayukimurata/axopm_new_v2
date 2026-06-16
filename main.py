import flet as ft
from models.base import get_registered_models
from components.cards import create_model_card
from components.modals import create_edit_modal

def main(page: ft.Page):
    page.title = "App Dashboard"
    page.theme_mode = ft.ThemeMode.LIGHT

    # モーダル表示処理
    def open_editor(e, model_label):
        dlg = create_edit_modal(model_label, on_save=lambda _: print(f"Saved {model_label}"))
        page.dialog = dlg
        dlg.open = True
        page.update()

    grid_items = []
    for model_cls in get_registered_models():
        label = getattr(model_cls, "_label", model_cls.__name__)
        icon = getattr(model_cls, "_icon", "table_chart")

        # ポイント: l=label とすることで現在のラベルを正しくキャプチャする
        grid_items.append(
            create_model_card(
                title=label,
                icon=icon,
                on_click=lambda e, l=label: open_editor(e, l)
            )
        )

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
