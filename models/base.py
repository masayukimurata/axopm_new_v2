from typing import Type, Dict, Any

# モデルを登録するためのグローバルレジストリ
MODEL_REGISTRY: Dict[str, Dict[str, Any]] = {}

def register_model(label: str, icon: str):
    """
    モデルを自動的に管理メニューへ登録するためのメタデコレータ
    使用例: @register_model(label="レシピ一覧", icon="book")
    """
    def decorator(cls: Type):
        MODEL_REGISTRY[cls.__name__] = {
            "model": cls,
            "label": label,
            "icon": icon
        }
        return cls
    return decorator

class BaseModel:
    """
    すべてのデータモデルの基底クラス
    """
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
