import flet as ft

def BaseTextField(label: str, hint: str = "") -> ft.TextField:
    """
    アプリ全体で統一されたデザインのテキスト入力フィールド
    """
    return ft.TextField(
        label=label,
        hint_text=hint,
        border=ft.InputBorder.OUTLINE,
        border_radius=8,
        # 今後のデザイン変更はここで一括管理可能
    )
