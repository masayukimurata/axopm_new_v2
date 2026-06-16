from typing import Type, Dict, Any, List

# モデルを登録するためのグローバルレジストリ
MODEL_REGISTRY: Dict[str, Dict[str, Any]] = {}

def register_model(label: str, icon: str):
    """
    モデルを自動的に管理メニューへ登録するためのメタデコレータ
    """
    def decorator(cls: Type):
        MODEL_REGISTRY[cls.__name__] = {
            "model": cls,
            "label": label,
            "icon": icon
        }
        # クラス自体にもメタデータを付与してアクセスしやすくする
        setattr(cls, "_label", label)
        setattr(cls, "_icon", icon)
        return cls
    return decorator

def get_registered_models() -> List[Type]:
    """登録されたモデルクラスのリストを返す"""
    return [item["model"] for item in MODEL_REGISTRY.values()]

class BaseModel:
    """
    すべてのデータモデルの基底クラス
    """
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
