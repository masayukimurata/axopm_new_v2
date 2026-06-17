import flet as ft
from models.base import get_registered_models

# 引数 on_nav を追加して定義する
def create_sidebar(page: ft.Page, on_nav):
    nav_items = []
    for model_cls in get_registered_models():
        label = getattr(model_cls, "_label", "不明")
        icon_name = getattr(model_cls, "_icon", "table_chart")

        nav_items.append(
            ft.ListTile(
                leading=ft.Icon(getattr(ft.icons, icon_name.upper(), ft.icons.TABLE_CHART)),
                title=ft.Text(label),
                # on_nav を呼び出す
                on_click=lambda e, cls=model_cls: on_nav(cls)
            )
        )

    return ft.Container(
        content=ft.Column([
            ft.Text("Merchandise", size=20, weight=ft.FontWeight.BOLD),
            ft.Text("Manager Demo", size=12, color=ft.colors.GREY_500),
            ft.Container(content=ft.Text("migration_sandbox", size=10), bgcolor=ft.colors.GREY_800, padding=5, border_radius=5),
            ft.Divider(),
            *nav_items
        ], spacing=10),
        width=250, bgcolor=ft.colors.GREY_900, padding=20
    )
